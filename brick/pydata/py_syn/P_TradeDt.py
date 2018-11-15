# encoding: utf-8
"""
@author: ZhangYu
@contact: 292724306@qq.com
@site:
@software: PyCharm
@file: P_TradeDt.py
@time: 2017-12-21 15:21
"""

import MySQLdb
import pymssql
from public import *


#from brick.pydata.py_redis.py_SynRedis_pub import *
#redis_p = py_SynRedis_pub()
cf = ConfigParser.ConfigParser()
cf.read("/data/djangostack-1.9.7/apps/django/django_projects/Project/brick/pydata/py_syn/select.conf")
maxnumFetchone = cf.getint('myconfig', 'maxnumFetchone')


class P_TradeDt:
    def __init__(self, db_conn, sqlserver_conn):
        self.db_conn = db_conn
        self.sqlserver_conn = sqlserver_conn
        self.cursor = self.db_conn.cursor()

    def getPyInfo(self, TradeNIDs):
        objs = []
        i = 0
        SKUList = []
        sql = "SELECT NID,TradeNID,L_EBAYITEMTXNID,L_NAME,L_NUMBER,L_QTY,L_SHIPPINGAMT,L_HANDLINGAMT,L_CURRENCYCODE," \
              "L_AMT,L_OPTIONSNAME,L_OPTIONSVALUE,L_TAXAMT,SKU,CostPrice,AliasCnName,AliasEnName,Weight,DeclaredValue," \
              "OriginCountry,OriginCountryCode,BmpFileName,GoodsName,GoodsSKUID,StoreID,eBaySKU,L_ShipFee,L_TransFee," \
              "L_ExpressFare,BuyerNote from P_TradeDt WHERE TradeNID in (%s)"
        try:
            if self.sqlserver_conn:
                sqlcursor = self.sqlserver_conn.cursor()
            while True:
                if len(TradeNIDs) > maxnumFetchone:
                    while True:
                        TradeNIDs_tmp = TradeNIDs[:maxnumFetchone]
                        x = ','.join(['%s'] * len(TradeNIDs_tmp))
                        try:
                            selectsql = sql % x
                            sqlcursor.execute(selectsql, tuple(TradeNIDs_tmp))
                            obj = sqlcursor.fetchall()
                        except pymssql.Error, e:
                            print "pymssql Error %d: %s" % (e.args[0], e.args[1])
                        else:
                            #print "P_TradeDt存入redis"
                            #print redis_p.setArrayToHashRedis("P_TradeDt", 2, 14, obj)
                            #print "P_TradeDt存入redis结束"
                            TradeNIDs = TradeNIDs[maxnumFetchone:]
                            i += 1
                            for obj_tmp in obj:
                                objs.append(obj_tmp)
                                if obj_tmp[13] != '' and obj_tmp[13] is not None:
                                    SKUList.append(obj_tmp[13])
                            print i
                            break

                if len(TradeNIDs) <= maxnumFetchone:
                    while True:
                        x = ','.join(['%s'] * len(TradeNIDs))
                        try:
                            selectsql = sql % x
                            sqlcursor.execute(selectsql, tuple(TradeNIDs))
                            obj = sqlcursor.fetchall()
                        except pymssql.Error, e:
                            print "pymssql Error %d: %s" % (e.args[0], e.args[1])
                        else:
                            #print "P_TradeDt存入redis"
                            #print redis_p.setArrayToHashRedis("P_TradeDt", 2, 14, obj)
                            #print "P_TradeDt存入redis结束"
                            i += 1
                            for obj_tmp in obj:
                                objs.append(obj_tmp)
                                if obj_tmp[13] != '' and obj_tmp[13] is not None:
                                    SKUList.append(obj_tmp[13])
                            print i
                            break
                    break
            if sqlcursor:
                sqlcursor.close()
            # print objs
            return objs , SKUList
        except pymssql.Error, e:
            print "pymssql Error %d: %s" % (e.args[0], e.args[1])

    def update_P_TradeDt(self, TradeNIDs):
        print "开始更新{0}".format("P_TradeDt")
        objs, SKUList= self.getPyInfo(TradeNIDs)
        sql = "replace INTO py_db.P_TradeDt(NID,TradeNID,L_EBAYITEMTXNID,L_NAME,L_NUMBER,L_QTY,L_SHIPPINGAMT,L_HANDLINGAMT,L_CURRENCYCODE," \
              "L_AMT,L_OPTIONSNAME,L_OPTIONSVALUE,L_TAXAMT,SKU,CostPrice,AliasCnName,AliasEnName,Weight,DeclaredValue," \
              "OriginCountry,OriginCountryCode,BmpFileName,GoodsName,GoodsSKUID,StoreID,eBaySKU,L_ShipFee,L_TransFee," \
              "L_ExpressFare,BuyerNote) VALUES (%s,%s,%s,%s,%s,%s," \
              "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        public_obj = public(self.db_conn, self.sqlserver_conn)
        public_obj.commitmanyFun(objs, sql)
        print "结束更新{0}".format("P_TradeDt")
        return list(set(SKUList))
