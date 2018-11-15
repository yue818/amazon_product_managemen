# -*- coding: utf-8 -*-

import sys
import os
sys.path.append('/data/djangostack-1.9.7/apps/django/django_projects/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Project.settings')
'''
说明：根据事件触发调用该函数，设置redis和更新t_onlin_info_wish(goodsflag)、t_online_info(goodsstatus)
'''

from django_redis import get_redis_connection
import MySQLdb
import json
from redis import Redis
import re
import requests,traceback
class redis_aliexprss(object):
    def __init__(self):
        self.redis_conn=get_redis_connection("aliexpress_online_info")

    def __private_hmset_attr(self,name,data):
        # for key,value in data.items():
        #     # if isinstance(value,dict):
        #     #     value=json.dumps(value)
        return self.redis_conn.hmset(name,data)

    def __private_hget_attr(self,name,key):
        if self.redis_conn is not None:
            _result=self.redis_conn.hget(name,key)
            try:
                result=json.loads(_result)
            except ValueError:
                return _result
            return result

    def hset_data(self,name, key, value):
        return self.redis_conn.hset(name, key, value)

    def __private_hgetall(self,name):
        return self.redis_conn.hgetall(name)

    def _hexists(self,name, key):
        return self.redis_conn.hexists(name, key)

    def hdel(self,name,key):
        return self.redis_conn.hdel(name,key)


    def get_data(self,name,key):
        if not self._hexists(name,key):
            return {}
        return self.__private_hget_attr(name,key)

    def set_data(self,name,data):
        if isinstance(data,dict):
            return self.__private_hmset_attr(name,data)
        raise TypeError('{} must dict'.format(data))

    def hgetall_data(self,name):
        return self.__private_hgetall(name)


    def smembers(self,name):
        return self.redis_conn.smembers(name)

    def delete(self,name):
        return self.redis_conn.delete(name)

    def sadd(self,name,*values):
        return self.redis_conn.sadd(name,*values)


import json
def product_status(statuslist):
    a1 = 0
    if 1 in statuslist or '1' in statuslist or u'1' in statuslist:
        a1 = 1
    a2 = 0
    if 2 in statuslist or '2' in statuslist or u'2' in statuslist:
        a2 = 1
    a3 = 0
    if 3 in statuslist or '3' in statuslist or u'3' in statuslist:
        a3 = 1
    a4 = 0
    if 4 in statuslist or '4' in statuslist or u'4' in statuslist:
        a4 = 1
    GoodsFlag = a1 * 1000 + a2 * 100 + a3 * 10 + a4
    return GoodsFlag

from math import ceil
def run(data):
    try:
        """入参：josn格式数据（{"sku":"WF-1197-WT-S","old":"正常","new":"","used":""}）"""
        result = {}
        result['errorcode'] = 0
        result['errortext'] = "no recorde"
        db = MySQLdb.connect(host='hequskuapp.mysql.rds.aliyuncs.com', user='by15161458383', passwd='K120Esc1', db='hq',
                             charset='utf8')
        cursor = db.cursor()
        try:
            switct_dict_unicode = {u"暂停销售": 4, u"清仓": 4, u"售完下架": 2, u"正常": 1, u"临时下架": 3, u"自动创建": 1, u"组合": 4, u"售完下架4": 2, u"在售": 1,
                           u"处理库尾": 4, u"清仓（合并）": 4, "": 4, u"停售": 4, }
            switct_dict = {"暂停销售": 4, "清仓": 4, "售完下架": 2, "正常": 1, "临时下架": 3, "自动创建": 1, "组合": 4, "售完下架4": 2, "在售": 1,
                           "处理库尾": 4, "清仓（合并）": 4, "": 4, "停售": 4, }
            sku=data.get('sku')
            if not sku:
                sku=data.get(u'sku')
            old=data.get('old')
            if not old:
                old=data.get(u'old')
            new=data.get('new')
            if not new:
                new=data.get(u'new')
            digital_new=switct_dict.get(new)
            if not digital_new:
                digital_new=switct_dict_unicode.get(new)
            if new:
                if digital_new:
                    if old:
                        cursor.execute('select product_id from t_erp_aliexpress_product_sku where SKU=%s',(sku,))
                        product_ids=cursor.fetchall()
                        if not product_ids:
                            result['errorcode'] = 0
                            result['errortext'] = "not ali sku"
                            return result
                        cursor.execute('update t_erp_aliexpress_product_sku set GoodsStatus=%s where SKU=%s',(digital_new,sku))
                        db.commit()
                        ra=redis_aliexprss()
                        ra.hset_data(sku,'GoodsStatus',digital_new)
                        product_id_dict={}
                        for (product_id,) in product_ids:
                            stopsales=[]
                            notstopsales=[]
                            cursor.execute('select GoodsStatus from t_erp_aliexpress_product_sku where product_id=%s', (product_id,))
                            GoodsStatuss=cursor.fetchall()
                            GoodsStatuss_set=set()
                            for (GoodsStatus,) in GoodsStatuss:
                                GoodsStatuss_set.add(GoodsStatus)
                                if GoodsStatus in (4,'4'):
                                    stopsales.append(GoodsStatus)
                                else:
                                    notstopsales.append(GoodsStatus)
                            if len(stopsales) + len(notstopsales):
                                StopSales = ceil(len(stopsales) * 100.0 / (len(stopsales) + len(notstopsales)))
                            else:
                                StopSales = 0
                            if stopsales:
                                StopSalesFlag = 1
                            else:
                                StopSalesFlag = 0
                            GoodsFlag=product_status(GoodsStatuss_set)
                            cursor.execute('update t_erp_aliexpress_online_info set StopSales=%s,StopSalesFlag=%s,GoodsFlag=%s '
                                           'where product_id=%s',(StopSales,StopSalesFlag,GoodsFlag,product_id))

                            db.commit()
                            product_id_dict[product_id]=StopSalesFlag

                        result['errorcode']=0
                        result['errortext'] = json.dumps({sku:product_id_dict})

        except Exception:
            result['errorcode']=-1
            result['errortext']=traceback.format_exc()
        try:
            cursor.close()
            db.close()
        except Exception:
            pass
        return result
    except Exception:
        result={'errorcode':-1,'errortext':traceback.format_exc()}
        return result