# encoding: utf-8
"""
@author: ZhangYu
@contact: 292724306@qq.com
@site:
@software: PyCharm
@file: b_goods.py
@time: 2017-12-21 15:21
"""
import MySQLdb
import pymssql
from public import public
from datetime import datetime
import ConfigParser


cf = ConfigParser.ConfigParser()
cf.read("/data/djangostack-1.9.7/apps/django/django_projects/Project/brick/pydata/py_syn/select.conf")
maxnumFetchone = cf.getint('myconfig', 'maxnumFetchone')


# 联表查询供应商名称
class b_goods:
    def __init__(self, db_conn, sqlserver_conn=None):
        self.db_conn = db_conn
        self.sqlserver_conn = sqlserver_conn
        self.cursor = self.db_conn.cursor()

    def getPyInfo(self, SKUList):
        i = 0
        SupplierID = []
        b_goods_objs = []
        selectsql = "select NID,GoodsCategoryID,CategoryCode,GoodsCode,GoodsName,ShopTitle,SKU,BarCode,FitCode," \
                    "MultiStyle,Material,Class,Model,Unit,Style,Brand,LocationID,Quantity,SalePrice,CostPrice," \
                    "AliasCnName,AliasEnName,Weight,DeclaredValue,OriginCountry,OriginCountryCode,ExpressID," \
                    "Used,BmpFileName,BmpUrl,MaxNum,MinNum,GoodsCount,SupplierID,Notes,SampleFlag,SampleCount," \
                    "SampleMemo,CreateDate,GroupFlag,SalerName,SellCount,SellDays,PackFee,PackName,GoodsStatus," \
                    "DevDate,SalerName2,BatchPrice,MaxSalePrice,RetailPrice,MarketPrice,PackageCount," \
                    "StockDays,StoreID,Purchaser,LinkUrl,LinkUrl2,LinkUrl3,StockMinAmount," \
                    "MinPrice,HSCODE,ViewUser,InLong,InWide,InHigh,InGrossweight,InNetweight,OutLong,OutWide," \
                    "OutHigh,OutGrossweight,OutNetweight,ShopCarryCost,ExchangeRate,WebCost,PackWeight," \
                    "LogisticsCost,GrossRate,CalSalePrice,CalYunFei,CalSaleAllPrice,PackMsg,ItemUrl,IsCharged," \
                    "DelInFile,Season,IsPowder,IsLiquid,possessMan1,possessMan2,LinkUrl4,LinkUrl5,LinkUrl6," \
                    "isMagnetism,NoSalesDate from b_goods(nolock) where SKU in (%s)"
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
                                b_goods_objs.append(obj)
                                SupplierID.append(obj[33])
                        i += 1
                    if len(SKUList) <= maxnumFetchone:
                        x = ','.join(['%s'] * len(SKUList))
                        sql = selectsql % x
                        sqlcursor.execute(sql, tuple(SKUList))
                        objs = sqlcursor.fetchall()
                        for obj in objs:
                            if obj:
                                b_goods_objs.append(obj)
                                SupplierID.append(obj[33])
                        i += 1
                        break
                    print i
            if sqlcursor:
                sqlcursor.close()
            # print objs
            return b_goods_objs, SupplierID
        except pymssql.Error, e:
            print "pymssql Error %d: %s" % (e.args[0], e.args[1])

    def update_b_goods(self, SKUList,mainsku):
        print "Begin:{},Time:{},Count:{}".format("b_goods", datetime.now(), len(SKUList))
        SKUList = list(set(SKUList))
        objs, SupplierID = self.getPyInfo(SKUList)
        try:
            insertSQL = "replace INTO py_db.b_goods(NID,GoodsCategoryID,CategoryCode,GoodsCode,GoodsName,ShopTitle,SKU,BarCode,FitCode," \
                        "MultiStyle,Material,Class,Model,Unit,Style,Brand,LocationID,Quantity,SalePrice,CostPrice," \
                        "AliasCnName,AliasEnName,Weight,DeclaredValue,OriginCountry,OriginCountryCode,ExpressID," \
                        "Used,BmpFileName,BmpUrl,MaxNum,MinNum,GoodsCount,SupplierID,Notes,SampleFlag,SampleCount," \
                        "SampleMemo,CreateDate,GroupFlag,SalerName,SellCount,SellDays,PackFee,PackName,GoodsStatus," \
                        "DevDate,SalerName2,BatchPrice,MaxSalePrice,RetailPrice,MarketPrice,PackageCount," \
                        "StockDays,StoreID,Purchaser,LinkUrl,LinkUrl2,LinkUrl3,StockMinAmount," \
                        "MinPrice,HSCODE,ViewUser,InLong,InWide,InHigh,InGrossweight,InNetweight,OutLong,OutWide," \
                        "OutHigh,OutGrossweight,OutNetweight,ShopCarryCost,ExchangeRate,WebCost,PackWeight," \
                        "LogisticsCost,GrossRate,CalSalePrice,CalYunFei,CalSaleAllPrice,PackMsg,ItemUrl,IsCharged," \
                        "DelInFile,Season,IsPowder,IsLiquid,possessMan1,possessMan2,LinkUrl4,LinkUrl5,LinkUrl6," \
                        "isMagnetism,NoSalesDate,ChangeStatusTime,MainSKU) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                        "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                        "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                        "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'{}','{}')".format(datetime.now(),mainsku)
            public_obj = public(self.db_conn, self.sqlserver_conn)
            public_obj.commitmanyFun(objs, insertSQL)
            print "End:{},Time:{},Count:{}".format("b_goods", datetime.now(), len(SKUList))
            return SupplierID
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
