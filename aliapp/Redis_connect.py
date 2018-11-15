#-*-coding:utf-8-*-

"""  
 @author: wushiyang 
 @email:2881591222@qq.com
 @time: 2018-06-12 16:44
 @desc: 
"""

#"LOCATION": "redis://:K120Esc1@r-uf6206e9df36e854.redis.rds.aliyuncs.com:6379/10",  # 速卖通api redis

from django_redis import get_redis_connection
import MySQLdb
import json
from redis import Redis
import re

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




    def pipeline(self):
        r = Redis(host='r-uf6206e9df36e854.redis.rds.aliyuncs.com', port=6379, password='K120Esc1', db=10)
        return r.pipeline()

class redis_product(object):
    def __init__(self):
        self.redis_conn=get_redis_connection("default")
        self.db_cnxn=MySQLdb.connect(host="hequskuapp.mysql.rds.aliyuncs.com", user="by15161458383", passwd="K120Esc1",db="hq_db", charset="utf8")


    def __private_get_attr(self,name,key):
        if self.redis_conn is not None:
            return self.redis_conn.hget(name,key)



    def __private_set_attr(self,name,key,value):
        if self.redis_conn is not None and value is not None:
            self.redis_conn.hset(name, key,value)



    def __private_hmset_attr(self,name,data):
        # for key,value in data.items():
        #     # if isinstance(value,dict):
        #     #     value=json.dumps(value)
        self.redis_conn.hmset(name,data)

    def __private_hget_attr(self,name,key):
        if self.redis_conn is not None:
            _result=self.redis_conn.hget(name,key)
            try:
                result=json.loads(_result)
            except ValueError:
                return _result
            return result

    def __private_hgetall(self,name):
        return self.redis_conn.hgetall(name)

    def __private_hexists(self,name, key):
        return self.redis_conn.hexists(name, key)


    def get_data(self,name,key):
        if not self.__private_hexists(name,key):
            return {}
        return self.__private_hget_attr(name,key)

    def set_data(self,name,data):
        if isinstance(data,dict):
            return self.__private_hmset_attr(name,data)
        raise TypeError('{} must dict'.format(data))

    def hgetall_data(self,name):
        return self.__private_hgetall(name)


    def set_bemainsku_by_sku(self,sku,bemainsku):
        self.__private_set_attr(sku,'MainSKU',bemainsku)


    def get_bemainsku_by_sku(self,sku):

        bemainsku = self.__private_get_attr(sku,'MainSKU')
        if bemainsku is None and self.redis_conn is not None:
            curs = self.db_cnxn.cursor()
            curs.execute('select MainSKU from hq_db.t_product_mainsku_sku WHERE ProductSKU = %s ;', (sku,))
            obj = curs.fetchone()
            if obj:
                bemainsku = obj[0]
            if sku and bemainsku is None:
                slist = re.findall(r'[0-9]+|[a-z-]+|[A-Z-|]+', sku)
                if len(slist) >= 2:
                    bemainsku = '%s%s' % (slist[0], slist[1])
                else:
                    bemainsku = ''.join(slist)
            if bemainsku:
                self.set_bemainsku_by_sku(sku, bemainsku)
        return bemainsku



    def get_goodsstatus_by_sku(self, sku):
        goodsstatus = self.__private_get_attr(sku, 'GoodsStatus')
        if self.db_cnxn is not None:
            stacur = self.db_cnxn.cursor()
            sql = "SELECT GoodsStatus, used FROM py_db.b_goods WHERE SKU=%s;"
            stacur.execute(sql, (sku,))
            obj = stacur.fetchone()
            if obj:
                used = obj[1]
                goodsstatus = obj[0]
                if int(used) == 1:
                    goodsstatus = '4'  # 停售
                else:
                    sql = "SELECT statuscode FROM hq_db.goodsstatus_compare WHERE hq_GoodsStatus=%s;"
                    stacur.execute(sql, (goodsstatus,))
                    obj = stacur.fetchone()
                    if obj:
                        goodsstatus = obj[0]
            stacur.close()
        if goodsstatus == u'1' or goodsstatus == u'1-正常':
            goodsstatus = u'正常'
        if goodsstatus == u'2' or goodsstatus == u'2-售完下架':
            goodsstatus = u'售完下架'
        if goodsstatus == u'3' or goodsstatus == u'3-临时下架':
            goodsstatus = u'临时下架'
        if goodsstatus == u'4' or goodsstatus == u'4-停售':
            goodsstatus = u'停售'
        return goodsstatus


    def set_tort_by_mainsku(self, mainsku,tort):
        return self.__private_set_attr(mainsku,'Site',tort)

    def setSKU(self,shopsku,sku):
        return self.__private_set_attr(shopsku,'SKU',sku)


    def getskueach(self,shopsku):
        sku = self.__private_get_attr(shopsku, 'SKU')
        if sku is None and self.db_cnxn is not None:
            skusor = self.db_cnxn.cursor()
            skusor.execute("select SKU from py_db.b_goodsskulinkshop WHERE ShopSKU = %s ;", (shopsku,))
            obj = skusor.fetchone()
            if obj:
                sku = obj[0]
                self.setSKU(shopsku, sku)
            else:
                skusor.execute("select SKU from py_db.b_goods WHERE SKU = %s ;", (shopsku,))
                skuobj = skusor.fetchone()
                if skuobj:
                    sku = skuobj[0]
                    self.setSKU(shopsku, sku)
            skusor.close()
        return sku



    def set_goodsstatus_by_sku(self,sku,status):
        self.__private_set_attr(sku,'GoodsStatus',status)

    def get_goodsstatus_by_sku(self,sku):
        goodsstatus = self.__private_get_attr(sku,'GoodsStatus')
        if goodsstatus is None and self.db_cnxn is not None:
            stacur = self.db_cnxn.cursor()
            stacur.execute('select GoodsStatus,used from py_db.b_goods WHERE SKU = %s ;',(sku,))
            obj = stacur.fetchone()
            if obj:
                used = obj[1]
                goodsstatus = obj[0]
                if int(used) == 1:
                    goodsstatus = '4' # 停售
                else:
                    stacur.execute('select statuscode from goodsstatus_compare WHERE hq_GoodsStatus = %s ;', (goodsstatus,))
                    obj = stacur.fetchone()
                    if obj:
                        goodsstatus = obj[0]
                self.set_goodsstatus_by_sku(sku,goodsstatus)
            stacur.close()
        if goodsstatus == '1' or goodsstatus == u'1-正常':
            goodsstatus = u'正常'
        if goodsstatus == '2' or goodsstatus == u'2-售完下架':
            goodsstatus = u'售完下架'
        if goodsstatus == '3' or goodsstatus == u'3-临时下架':
            goodsstatus = u'临时下架'
        if goodsstatus == '4' or goodsstatus == u'4-停售':
            goodsstatus = u'停售'
        return goodsstatus



    def getSKU(self,shopsku):
        if shopsku:
            shopsku = shopsku.strip()
        sku = None
        skulist = []
        for shopskutmp in shopsku.split('+'):
            newshopsku = shopskutmp.split('*')[0].split('\\')[0]
            sku = self.getskueach(newshopsku.strip())
            if sku :
                skulist.append(sku)
        if skulist:
            sku = '+'.join(skulist)
        return sku



    def get_tort_by_mainsku(self, mainsku):
        tort = self.__private_get_attr(mainsku, 'Site')
        if tort in (None,'None') and self.db_cnxn is not None:
            percur = self.db_cnxn.cursor()
            percur.execute('select IPForbiddenSite from hq_db.t_tort_info where MainSKU = %s and OperationState = "Y";', (mainsku,))
            objs = percur.fetchall()
            percur.close()
            tortlist = []
            for obj in objs:
                if obj and obj[0] is not None and obj[0].strip() != '':
                    if obj[0].strip() == 'All':
                        tortlist = tortlist + ['Wish', 'Aliexpress', 'eBay', 'Amazon']
                    else:
                        tortlist = tortlist + obj[0].strip().split(',')

            tortlist = set(tortlist)
            if len(tortlist) >= 1:
                tort = '|'.join(tortlist)
                self.set_tort_by_mainsku(mainsku, tort)
        if tort is not None:
            tort = tort.split('|')
        return tort

    def InfringingAliexpress(self,mainsku,platform=u'Aliexpress'):
        skutort = None
        if mainsku is not None and mainsku.strip() != '':
            skutort = self.get_tort_by_mainsku(mainsku)
        if skutort is not None and platform in skutort:
            return False
        else:
            return True

    def InfringingAll(self,mainsku):
        skutort = []
        if mainsku is not None and mainsku.strip() != '':
            skutort = self.get_tort_by_mainsku(mainsku)
        return skutort


    def judgeskuableornotAliexpress(self,sku,platform=u'Aliexpress'):
        #判断子SKU状态
        goodsstatus = self.get_goodsstatus_by_sku(sku)
        if goodsstatus is None or goodsstatus.strip() != u'正常':
            return False

        #判断是否侵权
        mainsku = self.get_bemainsku_by_sku(sku)
        skutort = None
        if mainsku is not None and mainsku.strip() != '':
            skutort = self.get_tort_by_mainsku(mainsku)
        if skutort is not None and platform in skutort:
            print sku,mainsku,skutort
            return False
        else:
            return True


    # get 侵权状态  add by wangzy 20180525
    def get_tortstatus_by_mainsku(self, mainsku):
        tortInfo = self.__private_get_attr(mainsku, 'TortInfo')
        return tortInfo