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
from b_goodscats import *
from b_supplier import *
from gs_compared import *
import pymssql
import mainSKU


#from brick.pydata.py_redis.py_SynRedis_pub import *
#redis_p = py_SynRedis_pub()
class t_product_b_goods():
    # 根据传入的MainSKU来从普源获取同步信息  暂时从b_goods表同步

    def __init__(self, db_conn, sqlserver_conn):
        self.db_conn = db_conn
        self.sqlserver_conn = sqlserver_conn
        self.cursor = self.db_conn.cursor()


    def getPyInfo(self, SKU):
        try:
            if self.sqlserver_conn:
                sqlcursor = self.sqlserver_conn.cursor()
            selectsql = "select NID,GoodsCategoryID,CategoryCode,GoodsCode,GoodsName," \
                        "ShopTitle,SKU,BarCode,FitCode,MultiStyle,Material,Class,Model,Unit,Style,Brand,LocationID," \
                        "Quantity,SalePrice,CostPrice,AliasCnName,AliasEnName,Weight,DeclaredValue,OriginCountry," \
                        "OriginCountryCode,ExpressID,Used,BmpFileName,BmpUrl,MaxNum,MinNum,GoodsCount,SupplierID,Notes," \
                        "SampleFlag,SampleCount,SampleMemo,CreateDate,GroupFlag,SalerName,SellCount,SellDays,PackFee," \
                        "PackName,GoodsStatus,DevDate,SalerName2,BatchPrice,MaxSalePrice,RetailPrice,MarketPrice," \
                        "PackageCount,ChangeStatusTime,StockDays,StoreID,Purchaser,LinkUrl,LinkUrl2,LinkUrl3," \
                        "StockMinAmount,MinPrice,HSCODE,ViewUser,InLong,InWide,InHigh,InGrossweight,InNetweight," \
                        "OutLong,OutWide,OutHigh,OutGrossweight,OutNetweight,ShopCarryCost,ExchangeRate,WebCost," \
                        "PackWeight,LogisticsCost,GrossRate,CalSalePrice,CalYunFei,CalSaleAllPrice,PackMsg,ItemUrl," \
                        "IsCharged,DelInFile,Season,IsPowder,IsLiquid,possessMan1,possessMan2,LinkUrl4,LinkUrl5," \
                        "LinkUrl6,isMagnetism,NoSalesDate from b_goods WHERE SKU='%s'" % SKU
            if sqlcursor:
                sqlcursor.execute(selectsql)
                obj = sqlcursor.fetchone()
                #redis_p.setToListRedis("t_product_b_goods_all_productsku_{0}".format(SKU), obj)
                sqlcursor.close()
            # print obj
            return obj
        except:
            print "普源数据获取失败"

    # 添加 t_product_b_goods_all_productsku数据    ==》   作为子SKU展示
    def update_all_productsku(self, SKU):
        cursor = self.db_conn.cursor()
        MainSKU = mainSKU.getMainSKU(SKU)
        obj = self.getPyInfo(SKU)
        try:
            insertSQL = "replace INTO t_product_b_goods_all_productsku(NID,GoodsCategoryID,CategoryCode,GoodsCode,GoodsName," \
                        "ShopTitle,SKU,BarCode,FitCode,MultiStyle,Material,Class,Model,Unit,Style,Brand,LocationID," \
                        "Quantity,SalePrice,CostPrice,AliasCnName,AliasEnName,Weight,DeclaredValue,OriginCountry," \
                        "OriginCountryCode,ExpressID,Used,BmpFileName,BmpUrl,MaxNum,MinNum,GoodsCount,SupplierID,Notes," \
                        "SampleFlag,SampleCount,SampleMemo,CreateDate,GroupFlag,SalerName,SellCount,SellDays,PackFee," \
                        "PackName,GoodsStatus,DevDate,SalerName2,BatchPrice,MaxSalePrice,RetailPrice,MarketPrice," \
                        "PackageCount,ChangeStatusTime,StockDays,StoreID,Purchaser,LinkUrl,LinkUrl2,LinkUrl3," \
                        "StockMinAmount,MinPrice,HSCODE,ViewUser,InLong,InWide,InHigh,InGrossweight,InNetweight," \
                        "OutLong,OutWide,OutHigh,OutGrossweight,OutNetweight,ShopCarryCost,ExchangeRate,WebCost," \
                        "PackWeight,LogisticsCost,GrossRate,CalSalePrice,CalYunFei,CalSaleAllPrice,PackMsg,ItemUrl," \
                        "IsCharged,DelInFile,Season,IsPowder,IsLiquid,possessMan1,possessMan2,LinkUrl4,LinkUrl5," \
                        "LinkUrl6,isMagnetism,NoSalesDate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                        "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                        "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                        "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cursor.execute(insertSQL, obj)
            self.cursor.execute('commit')

            updateSQL = "UPDATE t_product_b_goods_all_productsku SET MainSKU=%s WHERE SKU=%s"
            self.cursor.execute(updateSQL, (MainSKU, SKU))
            self.cursor.execute('commit')

            # 更新  停售  状态
            sqlUsed = u"update t_product_b_goods_all_productsku set GoodsStatus='停售' WHERE Used=1 AND SKU='%s'" % SKU
            self.cursor.execute(sqlUsed)
            # print "Used状态已更新"

            # 更新  状态  6种
            SqlGoodsStatus_compare = "select GoodsStatus from t_product_b_goods_all_productsku WHERE SKU='%s'" % SKU
            self.cursor.execute(SqlGoodsStatus_compare)
            hq_statusTmp = self.cursor.fetchone()
            if hq_statusTmp:
                hq_status = hq_statusTmp[0].encode("utf-8")
                gs_compare = gs_compared(self.db_conn)
                py_statusTmp = gs_compare.getPy_status(hq_status)
                if py_statusTmp:
                    py_status = py_statusTmp[0].encode("utf-8")
                    SqlGoodsStatus = "update t_product_b_goods_all_productsku set GoodsStatus=%s WHERE SKU=%s"
                    self.cursor.execute(SqlGoodsStatus, (py_status, SKU))
                    # print u"GoodsStatus已更新"

            SqlTortInfo = "select Site from t_tort_aliexpress where MainSKU='%s'" % MainSKU
            self.cursor.execute(SqlTortInfo)
            TortSite = self.cursor.fetchone()
            if TortSite:
                SqlTortInfoUpdate1 = "update t_product_b_goods_all_productsku set tortinfo='%s' WHERE MainSKU='%s'" % (
                    TortSite[0], MainSKU)
                self.cursor.execute(SqlTortInfoUpdate1)
                # print u"已侵权，状态更新"
            else:
                SqlTortInfoUpdate2 = "update t_product_b_goods_all_productsku set tortinfo='1' WHERE MainSKU='%s'" % MainSKU
                self.cursor.execute(SqlTortInfoUpdate2)
                # print u"未侵权"

            self.cursor.execute('commit')


        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
