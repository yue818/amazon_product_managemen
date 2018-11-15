#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@desc:数据一致性事件触发实时进程
@author: dingjun
@software: PyCharm
@file:t_event_class.py
@time: 2018/5/20
@数据一致性事件触发实时进程对象
"""
import sys
import os
sys.path.append('/data/djangostack-1.9.7/apps/django/django_projects/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Project.settings')
import MySQLdb
import datetime
import simplejson as json
from brick.classredis.classsku import classsku
from brick.classredis.classmainsku import classmainsku
from django_redis import get_redis_connection
connRedis = get_redis_connection(alias='product')
#from redis import Redis
#connRedis = Redis(host='192.168.105.223', port=6379,db=0)
from django.db import  connection
#connection = MySQLdb.Connect('192.168.105.111', 'root','root123','hq',port=3306, charset='utf8')

classsku_obj = classsku()

class t_event_class():
    def __init__(self,db_conn = connection):
        self.db_conn   = db_conn
        self.event_max_num = 5000

    def get_event_functions(self):
        try:
            result = {}
            cursor =self.db_conn.cursor()
            sql = "select a.id,a.event_id,a.event_type," \
                "a.event_key,a.event_time," \
                "b.function_id,c.function_path,c.params,c.result "  \
                "from hq_db.t_event a," \
                "hq_db.t_event_function b," \
                "hq_db.t_function c " \
                "where a.event_id = b.event_id " \
                "and a.event_type = b.event_type " \
                "and b.function_id=c.function_id " \
                "order by a.id limit %s;" %(self.event_max_num)
            cursor.execute(sql)
            result['result']=cursor.fetchall()
            cursor.close()
            result['errorcode'] = 0
        except MySQLdb.Error, e:
            result['errorcode'] = 26666
        except Exception,ex:
            result['errorcode'] = -1
            print 'Exception = %s ex=%s  __LINE__=%s'%(Exception,ex,sys._getframe().f_lineno)
        return result

    def format_params(self,obj):
        params = {}
        params = json.loads(obj)
        return params

    def move_event_to_his(self,obj,status,code,errinfo):
        try:
            result = {}
            cursor =self.db_conn.cursor()
            sql_1 = "insert into t_event_his (id,event_id,event_type,event_key,event_time,deal_time,deal_status,result,errinfo) " \
            "values (%s,'%s','%s','%s','%s','%s','%s','%s','%s');" %(int(obj[0]),obj[1],obj[2],obj[3],obj[4],datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),status,code,errinfo)
            sql_2 = "delete from t_event where id= %s ;" %(int(obj[0]))
            cursor.execute(sql_1)
            cursor.execute(sql_2)
            cursor.execute('commit;')
            cursor.close()
            result['errorcode'] = 0
        except MySQLdb.Error, e:
            result['errorcode'] = 26666
        except Exception,ex:
            result['errorcode'] = -1
            print 'Exception = %s ex=%s  __LINE__=%s'%(Exception,ex,sys._getframe().f_lineno)
        return result

    def insert_t_event(self,strEventID,opType,strEventKey):
        try:
            result = {}
            cursor =self.db_conn.cursor()
            sql_1 = "insert into t_event (event_id,event_type,event_key,event_time) " \
            "values ('%s','%s','%s','%s');" %(strEventID,opType,strEventKey,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            cursor.execute(sql_1)
            cursor.execute('commit;')
            cursor.close()
            result['errorcode'] = 0
        except MySQLdb.Error, e:
            result['errorcode'] = 26666
        except Exception,ex:
            result['errorcode'] = -1
            print 'Exception = %s ex=%s  __LINE__=%s'%(Exception,ex,sys._getframe().f_lineno)
        return result
    '''
    说明:商品状态insert触发事件
    '''
    def b_goods_status_insert_trigger(self,sku):
        sStatus = classsku_obj.get_goodsstatus_by_sku(sku)
        result = {}
        if sStatus is None:
            result['errorcode'] = 0
            return result
        strEventKey = '{"sku":"' + sku + '","old":"","new":"' + sStatus + '","used":"0"}'
        result = self.insert_t_event('b_goods_goodsstatus','I',strEventKey)
        return result

    '''
        说明:商品状态update触发事件
    '''
    def b_goods_status_update_trigger(self,sku):
        sStatus = classsku_obj.get_goodsstatus_by_sku(sku)
        result = {}
        if sStatus is None:
            result['errorcode'] = 0
            return result
        strEventKey = '{"sku":"' + sku + '","old":"","new":"' + sStatus + '","used":"0"}'
        result = self.insert_t_event('b_goods_goodsstatus','U', strEventKey)
        return result

    '''
        说明:商品状态delete触发事件
     '''
    def b_goods_status_delete_trigger(self,sku):
        sStatus = classsku_obj.get_goodsstatus_by_sku(sku)
        result = {}
        if sStatus is None:
            result['errorcode'] = 0
            return result
        strEventKey =  '{"sku":"' + sku + '","old":"' + sStatus + '","new":"","used":"0"}'
        result = self.insert_t_event('b_goods_goodsstatus','D', strEventKey)
        return result

    '''
        说明:侵权状态insert触发事件
    '''
    def t_tort_info_status_insert_trigger(self,sku):
        classmainsku_obj = classmainsku(self.db_conn, connRedis)
        sStatus = classmainsku_obj.get_tortstatus_by_mainsku(sku)
        result = {}
        if sStatus is None:
            result['errorcode'] = 0
            return result
        strEventKey = '{"MainSKU":"' + sku + '","old":"","new":"' + sStatus + '","used":"0"}'
        result = self.insert_t_event('t_tort_info_tortstatus','I',strEventKey)
        return result

    '''
        说明:侵权状态update触发事件
    '''
    def t_tort_info_status_update_trigger(self,sku):
        classmainsku_obj = classmainsku(self.db_conn, connRedis)
        sStatus = classmainsku_obj.get_tortstatus_by_mainsku(sku)
        result = {}
        if sStatus is None:
            result['errorcode'] = 0
            return result
        strEventKey = '{"MainSKU":"' + sku + '","old":"","new":"' + sStatus + '","used":"0"}'
        result = self.insert_t_event('t_tort_info_tortstatus', 'U', strEventKey)
        return result

    '''
       说明:侵权状态delete触发事件
    '''
    def t_tort_info_status_delete_trigger(self,sku):
        classmainsku_obj = classmainsku(self.db_conn, connRedis)
        sStatus = classmainsku_obj.get_tortstatus_by_mainsku(sku)
        result = {}
        if sStatus is None:
            result['errorcode'] = 0
            return result
        strEventKey =  '{"MainSKU":"' + sku + '","old":"' + sStatus + '","new":"","used":"0"}'
        result = self.insert_t_event('t_tort_info_tortstatus','D', strEventKey)
        return result

