# encoding: utf-8
"""
@author: ZhangYu
@contact: 292724306@qq.com
@site:
@software: PyCharm
@file: P_TradeDtUn.py
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


class P_TradeDtUn:
    def __init__(self, db_conn, sqlserver_conn):
        self.db_conn = db_conn
        self.sqlserver_conn = sqlserver_conn
        self.cursor = self.db_conn.cursor()

    def getPyInfo(self, NIDs):
        objs = []
        i = 0
        sql = "SELECT NID,TradeNID,L_EBAYITEMTXNID,L_NAME,L_NUMBER,L_QTY,L_SHIPPINGAMT,L_HANDLINGAMT,L_CURRENCYCODE," \
              "L_AMT,L_OPTIONSNAME,L_OPTIONSVALUE,L_TAXAMT,SKU,CostPrice,AliasCnName,AliasEnName,Weight,DeclaredValue," \
              "OriginCountry,OriginCountryCode,BmpFileName,GoodsName,GoodsSKUID,StoreID,eBaySKU,L_ShipFee,L_TransFee," \
              "L_ExpressFare,BuyerNote from P_TradeDtUn WHERE TradeNID in (%s)"
        try:
            if self.sqlserver_conn:
                sqlcursor = self.sqlserver_conn.cursor()
            while True:
                if len(NIDs) > maxnumFetchone:
                    while True:
                        NIDs_tmp = NIDs[:maxnumFetchone]
                        x = ','.join(['%s'] * len(NIDs_tmp))
                        try:
                            selectsql = sql % x
                            sqlcursor.execute(selectsql, tuple(NIDs_tmp))
                            obj = sqlcursor.fetchall()
                            #print "P_TradeDtUn存入redis"
                            #print redis_p.setArrayToHashRedis("P_TradeDtUn", 2, 14, obj)
                            #print "P_TradeDtUn存入redis结束"
                        except pymssql.Error, e:
                            print "pymssql Error %d: %s" % (e.args[0], e.args[1])
                        else:
                            NIDs = NIDs[maxnumFetchone:]
                            i += 1
                            for obj_tmp in obj:
                                objs.append(obj_tmp)
                            print i
                            break

                if len(NIDs) <= maxnumFetchone:
                    while True:
                        x = ','.join(['%s'] * len(NIDs))
                        try:
                            selectsql = sql % x
                            sqlcursor.execute(selectsql, tuple(NIDs))
                            obj = sqlcursor.fetchall()
                            #print "P_TradeDtUn存入redis"
                            #redis_p.setArrayToHashRedis("P_TradeDtUn", 2, 14, obj)
                            #print "P_TradeDtUn存入redis结束"
                        except pymssql.Error, e:
                            print "pymssql Error %d: %s" % (e.args[0], e.args[1])
                        else:
                            i += 1
                            for obj_tmp in obj:
                                objs.append(obj_tmp)
                            print i
                            break
                    break
            if sqlcursor:
                sqlcursor.close()
            # print objs
            return objs
        except pymssql.Error, e:
            print "pymssql Error %d: %s" % (e.args[0], e.args[1])

    def update_P_TradeDtUn(self, NIDs):
        print "开始更新{0}".format("P_TradeDtUn")
        objs = self.getPyInfo(NIDs)
        sql = "REPLACE into py_db.P_TradeDtUn(NID,TradeNID,L_EBAYITEMTXNID,L_NAME,L_NUMBER,L_QTY,L_SHIPPINGAMT,L_HANDLINGAMT,L_CURRENCYCODE," \
              "L_AMT,L_OPTIONSNAME,L_OPTIONSVALUE,L_TAXAMT,SKU,CostPrice,AliasCnName,AliasEnName,Weight,DeclaredValue," \
              "OriginCountry,OriginCountryCode,BmpFileName,GoodsName,GoodsSKUID,StoreID,eBaySKU,L_ShipFee,L_TransFee," \
              "L_ExpressFare,BuyerNote) VALUES (%s,%s,%s,%s,%s,%s," \
              "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        public_obj = public(self.db_conn, self.sqlserver_conn)
        public_obj.commitmanyFun(objs, sql)
        print "结束更新{0}".format("P_TradeDtUn")
