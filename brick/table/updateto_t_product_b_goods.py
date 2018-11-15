# encoding: utf-8
"""
@author: ZhangYu
@contact: 292724306@qq.com
@site:
@software: PyCharm
@file: updateto_t_product_b_goods.py
@time: 2017-12-19 19:16
"""
import logging
import MySQLdb
from b_goodscats import *
from b_supplier import *
from gs_compared import *
import pymssql
import mainSKU

# DBCONN = '192.168.105.111'
# DBUSR = 'root'
# DBPASSWD = 'root123'
# DBNAME = 'hq'
#
# DEBUG = 'ON'
# DATABASES = {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'hq_db',
#         'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
#         'PORT': '3306',
#         'USER': 'by15161458383',
#         'PASSWORD': 'K120Esc1',
#         'CHARSET': 'utf8'
#             }

class updateto_t_product_b_goods():
    #根据传入的MainSKU来从普源获取同步信息  暂时从b_goods表同步

    def __init__(self, db_conn,sqlserver_conn):
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
                sqlcursor.close()
            return obj
        except:
            print "普源数据获取失败"

    # #删除t_product_b_goods_all_productsku表中已有SKU
    # def delete_all_productsku(self, SKU):
    #     try:
    #         deleteSKUSQL = "DELETE FROM t_product_b_goods_all_productsku WHERE SKU='%s'" % SKU
    #         self.cursor.execute(deleteSKUSQL)
    #         self.cursor.execute('commit')
    #     except MySQLdb.Error, e:
    #         print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    #添加 t_product_b_goods_all_productsku数据    ==》   作为子SKU展示
    def update_all_productsku(self,MainSKU,SKU,obj):
        try:
            # 删除t_product_b_goods_all_productsku表中已有SKU
            deleteSKUSQL = "DELETE FROM t_product_b_goods_all_productsku WHERE NID='%s'" % obj[0]
            self.cursor.execute(deleteSKUSQL)
            self.cursor.execute('commit')
            insertSQL = "INSERT INTO t_product_b_goods_all_productsku(NID,GoodsCategoryID,CategoryCode,GoodsCode,GoodsName," \
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
            print "Used状态已更新"

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
                    print u"GoodsStatus已更新"

            SqlTortInfo = "select Site from t_tort_aliexpress where MainSKU='%s'" % MainSKU
            self.cursor.execute(SqlTortInfo)
            TortSite = self.cursor.fetchone()
            if TortSite:
                SqlTortInfoUpdate1 = "update t_product_b_goods_all_productsku set tortinfo='%s' WHERE MainSKU='%s'" % (TortSite[0],MainSKU)
                self.cursor.execute(SqlTortInfoUpdate1)
                print u"已侵权，状态更新"
            else:
                SqlTortInfoUpdate2 = "update t_product_b_goods_all_productsku set tortinfo='1' WHERE MainSKU='%s'" % MainSKU
                self.cursor.execute(SqlTortInfoUpdate2)
                print u"未侵权"

            self.cursor.execute('commit')
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])


    #目的 更新t_product_b_goods表 ==》 一个MainSKU只更新一条数据  我选择一个笨方法  每次都添加通过replace into来使它唯一
    def update_b_goods(self, objSKU):

        print objSKU
        cursor = self.db_conn.cursor()
        SKU = objSKU
        MainSKU = mainSKU.getMainSKU(SKU)
        obj = self.getPyInfo(SKU)
        # self.delete_all_productsku(SKU)
        self.update_all_productsku(MainSKU,SKU,obj)
        try:
            sql = "replace into t_product_b_goods (SKU, MainSKU,Name2, Material, LWH, Weight, SourcePicPath, ArtPicPath, UnitPrice, Unit, " \
                  "MinPackNum, MinOrder, SupplierID,SupplierArtNO,OrderDays,StockAlarmDays,Remark,Category2," \
                  "Category3,Electrification,Powder,Liquid,Magnetism,Buyer,Storehouse,NumBought,possessMan2,ReportName," \
                  "ReportName2,CreateTime,KFTime,ShopTitle,BarCode,FitCode,MultiStyle,Style,Brand,LocationID,Quantity," \
                  "SalePrice,CostPrice,DeclaredValue,OriginCountry,OriginCountryCode,ExpressID,Used,MaxNum,MinNum," \
                  "GoodsCount,SampleFlag,SampleCount,SampleMemo,GroupFlag,SellCount,SellDays,PackFee," \
                  "PackName,GoodsStatus,BatchPrice,MaxSalePrice,RetailPrice,MarketPrice,PackageCount," \
                  "LinkUrl,LinkUrl2,LinkUrl3,MinPrice,HSCODE,ViewUser,InLong,InWide,InHigh," \
                  "InGrossweight,InNetweight,OutLong,OutWide,OutHigh,OutGrossweight,OutNetweight,ShopCarryCost," \
                  "ExchangeRate,WebCost,PackWeight,LogisticsCost,GrossRate,CalSalePrice,CalYunFei,CalSaleAllPrice," \
                  "PackMsg,ItemUrl,DelInFile,Season,possessMan1,LinkUrl4,LinkUrl5,LinkUrl6,NoSalesDate,KFStaffName,JZLStaffName,UpdateTime,tortinfo) " \
                  "select SKU,MainSKU, GoodsName, Material, Class, Weight, BmpUrl, BmpFileName, CalSalePrice, Unit, PackageCount, " \
                  "StockMinAmount,SupplierID, Model, StockDays, SellDays, Notes, GoodsCategoryID, CategoryCode, IsCharged, " \
                  "IsPowder, IsLiquid, isMagnetism, Purchaser,StoreID, GoodsCount, possessMan2, AliasEnName, AliasCnName, " \
                  "CreateDate, DevDate ,ShopTitle,BarCode,FitCode,MultiStyle,Style,Brand,LocationID,Quantity," \
                  "SalePrice,CostPrice,DeclaredValue,OriginCountry,OriginCountryCode,ExpressID,Used,MaxNum,MinNum," \
                  "GoodsCount,SampleFlag,SampleCount,SampleMemo,GroupFlag,SellCount,SellDays,PackFee," \
                  "PackName,GoodsStatus,BatchPrice,MaxSalePrice,RetailPrice,MarketPrice,PackageCount," \
                  "LinkUrl,LinkUrl2,LinkUrl3,MinPrice,HSCODE,ViewUser,InLong,InWide,InHigh," \
                  "InGrossweight,InNetweight,OutLong,OutWide,OutHigh,OutGrossweight,OutNetweight,ShopCarryCost," \
                  "ExchangeRate,WebCost,PackWeight,LogisticsCost,GrossRate,CalSalePrice,CalYunFei,CalSaleAllPrice," \
                  "PackMsg,ItemUrl,DelInFile,Season,possessMan1,LinkUrl4,LinkUrl5,LinkUrl6,NoSalesDate,SalerName,SalerName2,ChangeStatusTime,tortinfo from t_product_b_goods_all_productsku WHERE MainSKU='%s'" % MainSKU

            self.cursor.execute(sql)
            self.cursor.execute('commit')

            # 联表查询商品种类名称
            selectCategory3Sql = "select Category3 from t_product_b_goods WHERE SKU='%s'" % SKU
            self.cursor.execute(selectCategory3Sql)
            Category3 = self.cursor.fetchone()
            if Category3:
                b_goodscat = b_goodscats(self.db_conn)
                LargeCategoryTmp = b_goodscat.selectCategoryName(Category3)
                if LargeCategoryTmp:
                    LargeCategory = LargeCategoryTmp[0].encode("utf-8")
                    sql3 = "update t_product_b_goods a set a.LargeCategory=%s WHERE a.SKU=%s"
                    self.cursor.execute(sql3, (LargeCategory, SKU))
                    print u"LargeCategory已更新"
                else:
                    print u"无对应的LargeCategory"
            else:
                print u"无对应Category3或者SKU"

            # 联表查询供应商名称
            selectSupplierIDSql = "select SupplierID from t_product_b_goods where SKU='%s'" % SKU
            self.cursor.execute(selectSupplierIDSql)
            SupplierID = self.cursor.fetchone()
            if SupplierID:
                b_supplier_obj = b_supplier(self.db_conn)
                SupplierNameTmp = b_supplier_obj.selectSupplierName(SupplierID)
                if SupplierNameTmp:
                    SupplierName = SupplierNameTmp[0].encode("utf-8")
                    sql4 = "UPDATE t_product_b_goods a SET a.SupplierID=%s WHERE a.SKU=%s"
                    self.cursor.execute(sql4, (SupplierName, SKU))
                    print u"SupplierID已更新"
                else:
                    print u"SupplierID无对应SupplierName"
            else:
                print u"无SupplierID值或者SKU"

            self.cursor.execute('commit')

        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])