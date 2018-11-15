# encoding: utf-8
"""
@author: ZhangYu
@contact: 292724306@qq.com
@site:
@software: PyCharm
@file: t_product_b_goods.py
@time: 2017-12-19 19:16
"""
import logging
import MySQLdb
from b_supplier import *
import pymssql
from b_goodsSKULocation import *
import ConfigParser
from public import public
from datetime import datetime

cf = ConfigParser.ConfigParser()
cf.read("/data/djangostack-1.9.7/apps/django/django_projects/Project/brick/pydata/py_syn/select.conf")
maxnumFetchone = cf.getint('myconfig', 'maxnumFetchone')


class b_goodsSKU():
    # 根据传入的MainSKU来从普源获取同步信息  暂时从b_goods表同步

    def __init__(self, db_conn, sqlserver_conn):
        self.db_conn = db_conn
        self.sqlserver_conn = sqlserver_conn
        self.cursor = self.db_conn.cursor()

    def getPyInfo(self, SKUList):
        i = 0
        b_goodsSKU_objs = []
        goodsSKUIDs = []
        selectsql = "select NID,GoodsID,SKU,property1,property2,property3,SKUName,LocationID," \
                    "BmpFileName,SellCount,Remark,SellCount1,SellCount2,SellCount3,Weight,CostPrice,RetailPrice," \
                    "MaxNum,MinNum,GoodsSKUStatus,ChangeStatusTime,ASINN,UPC,ModelNum,ChangeCostTime,linkurl " \
                    "from B_GoodsSKU(nolock) where SKU in (%s)"
        try:
            if self.sqlserver_conn:
                sqlcursor = self.sqlserver_conn.cursor()
                while True:
                    if len(SKUList) > maxnumFetchone:
                        SKUList_tmp = SKUList[:maxnumFetchone]
                        SKUList = SKUList[maxnumFetchone:]
                        x = ','.join(['%s'] * len(SKUList_tmp))
                        sql = selectsql % x
                        sqlcursor.execute(sql, tuple(SKUList_tmp))
                        objs = sqlcursor.fetchall()
                        for obj in objs:
                            if obj:
                                b_goodsSKU_objs.append(obj)
                                goodsSKUIDs.append(obj[0])
                        i += 1
                    if len(SKUList) <= maxnumFetchone:
                        x = ','.join(['%s'] * len(SKUList))
                        sql = selectsql % x
                        sqlcursor.execute(sql, tuple(SKUList))
                        objs = sqlcursor.fetchall()
                        for obj in objs:
                            if obj:
                                b_goodsSKU_objs.append(obj)
                                goodsSKUIDs.append(obj[0])
                        i += 1
                        break
                    print i
            if sqlcursor:
                sqlcursor.close()
            return b_goodsSKU_objs, goodsSKUIDs
        except pymssql.Error, e:
            print "pymssql Error %d: %s" % (e.args[0], e.args[1])

    def update_b_goodsSKU(self, SKUList):
        print "Begin:{},Time:{},Count:{}".format("b_goodsSKU", datetime.now(), len(SKUList))
        SKUList = list(set(SKUList))
        cursor = self.db_conn.cursor()
        objs, goodsSKUIDs = self.getPyInfo(SKUList)
        try:
            insertSQL = "REPLACE INTO py_db.b_goodssku(NID,GoodsID,SKU,property1,property2,property3,SKUName,LocationID," \
                        "BmpFileName,SellCount,Remark,SellCount1,SellCount2,SellCount3,Weight,CostPrice,RetailPrice," \
                        "MaxNum,MinNum,GoodsSKUStatus,ChangeStatusTime,ASINN,UPC,ModelNum,ChangeCostTime,linkurl" \
                        ") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                        "%s,%s,%s,%s,%s,%s,%s,%s)"
            public_obj = public(self.db_conn, self.sqlserver_conn)
            public_obj.commitmanyFun(objs, insertSQL)
            print "End:{},Time:{},Count:{}".format("b_goodsSKU", datetime.now(), len(SKUList))

            # 更新B_GoodsSKULocation 表
            b_goodsSKULocation_obj = b_goodsSKULocation(self.db_conn, self.sqlserver_conn)
            b_goodsSKULocation_obj.update_b_goodsSKULocation(goodsSKUIDs)
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
