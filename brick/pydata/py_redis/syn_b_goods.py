# coding: utf-8
"""
@author: wangzy
@contact: 15205512335
@site:普元b_goods同步到online系统py_db.b_goods
@software: PyCharm
@file: syn_b_goods.py
@time: 2018-06-29 15:21
"""
import datetime, time, calendar
import sys
from py_SynRedis_pub import py_SynRedis_pub,connRedis
import MySQLdb
from django.db import  connection
import pymssql
import ConfigParser


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hq',
        'HOST': '192.168.105.111',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'root123'
    },
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hq',
        'HOST': '192.168.105.111',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'root123'
    },
    'sqlserver': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ShopElf',
        'HOST': '122.226.216.10',
        'PORT': '18793',
        'USER': 'fancyqube',
        'PASSWORD': 'K120Esc1'
    },
}


class syn_b_goods():
    def __init__(self):
        self.db_conn = ''
        self.sqlcursor = ''
        self.db_conn_py = ''
        self.sqlcursor_py = ''
        self.cf = ConfigParser.ConfigParser()
        self.cf.read("py_Config.conf")
        # cf.read("/data/djangostack-1.9.7/apps/django/django_projects/Project/brick/pydata/py_redis/py_Config.conf")
        self.strCurrentDate = time.strftime("%Y%m%d")
        self.logPath = self.cf.get("SynB_Goods", "log_path")
        self.fileHead = self.cf.get("SynB_Goods", "fileHead")
        self.strFileName = self.logPath + self.fileHead + self.strCurrentDate + '.log'


    def Recordlog(self, message, logLevel, nLine):
        strTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        strInfo = "[" + strTime + "][" + str(__file__) + "," + str(nLine) + "," + str(logLevel) + "]:" + str(
            message) + "\n"
        with open(self.strFileName, 'a+') as f:
            f.write(strInfo)
        f.close()

    '''
        说明：如果本地数据库连接，需要关闭数据库
    '''

    def connSql(self, flag=0):
        if flag == 111:
            # 个人测试库环境(192.168.105.111)
            self.db_conn = MySQLdb.Connect(DATABASES['default']['HOST'], DATABASES['default']['USER'],
                                           DATABASES['default']['PASSWORD'],
                                           DATABASES['default']['NAME'], charset='utf8')
            self.sqlcursor = self.db_conn.cursor()
            # 正式环境
            '''
            self.db_conn = connection
            self.sqlcursor = self.db_conn.cursor()
            '''
        if flag == 10:
            # 个人测试库环境(192.168.105.111)
            #self.db_conn_py = MySQLdb.Connect(DATABASES['default']['HOST'], DATABASES['default']['USER'],DATABASES['default']['PASSWORD'],DATABASES['syn']['NAME'], charset='utf8')
            # 正式环境
            self.db_conn_py = pymssql.connect(host=DATABASES['sqlserver']['HOST'], user=DATABASES['sqlserver']['USER'],
                                              password=DATABASES['sqlserver']['PASSWORD'],
                                              database=DATABASES['sqlserver']['NAME'],
                                              port=DATABASES['sqlserver']['PORT'], charset='utf8')
            self.sqlcursor_py = self.db_conn_py.cursor()

    '''
    说明：如果本地数据库连接，需要关闭数据库
    '''

    def closeSql(self, flag=0):
        if flag == 111:
            self.sqlcursor.close()
            self.db_conn.close()
        if flag == 10:
            self.sqlcursor_py.close()
            self.db_conn_py.close()

    def get_py_b_goods_maxnid(self):
        try:
            strPYSql = "select max(NID) from b_goods(nolock)"
            n = self.sqlcursor_py.execute(strPYSql)
            maxNid = self.sqlcursor_py.fetchone()
            return maxNid[0]
        except Exception as e:
            self.Recordlog(e.message + ";get_py_b_goods error", "error", sys._getframe().f_lineno)

    def get_py_B_GoodsSKUWith1688_maxnid(self):
        try:
            strPYSql = "select max(NID) from B_GoodsSKUWith1688(nolock)"
            n = self.sqlcursor_py.execute(strPYSql)
            maxNid = self.sqlcursor_py.fetchone()
            return maxNid[0]
        except Exception as e:
            self.Recordlog(e.message + ";get_py_B_GoodsSKUWith1688_maxnid error", "error", sys._getframe().f_lineno)

    def get_py_b_supplier_maxnid(self):
        try:
            strPYSql = "select max(NID) from b_supplier(nolock)"
            n = self.sqlcursor_py.execute(strPYSql)
            maxNid = self.sqlcursor_py.fetchone()
            return maxNid[0]
        except Exception as e:
            self.Recordlog(e.message + ";get_py_b_goods error", "error", sys._getframe().f_lineno)

    def get_py_b_goods(self,minRange,MaxRange):
        try:
            strPYSql = "select NID,GoodsCategoryID,CategoryCode,GoodsCode,GoodsName,ShopTitle,SKU,BarCode,FitCode,MultiStyle,Material,Class,Model,Unit,Style,Brand,LocationID," \
                           "Quantity,SalePrice,CostPrice,AliasCnName,AliasEnName,Weight,DeclaredValue,OriginCountry,OriginCountryCode,ExpressID,Used,BmpFileName,BmpUrl,MaxNum,MinNum,GoodsCount,SupplierID," \
                           "Notes,SampleFlag,SampleCount,SampleMemo,CreateDate,GroupFlag,SalerName,SellCount,SellDays,PackFee,PackName,GoodsStatus,DevDate,SalerName2,BatchPrice,MaxSalePrice,RetailPrice," \
                           "MarketPrice,PackageCount,ChangeStatusTime,StockDays,StoreID,Purchaser,LinkUrl,LinkUrl2,LinkUrl3,StockMinAmount,MinPrice,HSCODE,ViewUser,InLong,InWide,InHigh,InGrossweight," \
                           "InNetweight,OutLong,OutWide,OutHigh,OutGrossweight,OutNetweight,ShopCarryCost,ExchangeRate,WebCost,PackWeight,LogisticsCost,GrossRate,CalSalePrice,CalYunFei,CalSaleAllPrice," \
                           "PackMsg,ItemUrl,IsCharged,DelInFile,Season,IsPowder,IsLiquid,possessMan1,possessMan2,LinkUrl4,LinkUrl5,LinkUrl6,isMagnetism,NoSalesDate," \
                           "(SELECT AttributeName + ';' FROM B_GoodsAttribute(nolock) WHERE GoodsID = b_goods.nid FOR XML PATH ('')) AS 'ATTRIBUTENAME'" \
                           "from b_goods(nolock) where NID >=%s and NID < %s and GoodsStatus is not NULL"%(minRange,MaxRange)
            n = self.sqlcursor_py.execute(strPYSql)
            sSKUArray = self.sqlcursor_py.fetchall()

            return sSKUArray
        except Exception as e:
            self.Recordlog(e.message + ";get_py_b_goods error", "error", sys._getframe().f_lineno)

    def set_online_b_goods(self):
        try:
            reload(sys)
            sys.setdefaultencoding('utf8')
            self.connSql(111)
            self.connSql(10)
            updateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self.Recordlog("start b_goods syn dealtime:%s" % (updateTime), "info", sys._getframe().f_lineno)
            maxNid = self.get_py_b_goods_maxnid()
            nidRange = 0
            nCount = 3000
            while nidRange < maxNid:
                try:
                    tupperPY_b_goods = self.get_py_b_goods(nidRange,nidRange+nCount)
                    strOnlineSql = "insert into py_db.b_goods(NID,GoodsCategoryID,CategoryCode,GoodsCode,GoodsName,ShopTitle,SKU,BarCode,FitCode,MultiStyle,Material,Class,Model,Unit,Style,Brand,LocationID," \
                                   "Quantity,SalePrice,CostPrice,AliasCnName,AliasEnName,Weight,DeclaredValue,OriginCountry,OriginCountryCode,ExpressID,Used,BmpFileName,BmpUrl,MaxNum,MinNum,GoodsCount,SupplierID," \
                                   "Notes,SampleFlag,SampleCount,SampleMemo,CreateDate,GroupFlag,SalerName,SellCount,SellDays,PackFee,PackName,GoodsStatus,DevDate,SalerName2,BatchPrice,MaxSalePrice,RetailPrice," \
                                   "MarketPrice,PackageCount,ChangeStatusTime,StockDays,StoreID,Purchaser,LinkUrl,LinkUrl2,LinkUrl3,StockMinAmount,MinPrice,HSCODE,ViewUser,InLong,InWide,InHigh,InGrossweight," \
                                   "InNetweight,OutLong,OutWide,OutHigh,OutGrossweight,OutNetweight,ShopCarryCost,ExchangeRate,WebCost,PackWeight,LogisticsCost,GrossRate,CalSalePrice,CalYunFei,CalSaleAllPrice," \
                                   "PackMsg,ItemUrl,IsCharged,DelInFile,Season,IsPowder,IsLiquid,possessMan1,possessMan2,LinkUrl4,LinkUrl5,LinkUrl6,isMagnetism,NoSalesDate,AttributeName) " \
                                   "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                                   "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update " \
                                   "SKU=values(SKU),GoodsCategoryID=values(GoodsCategoryID),CategoryCode=values(CategoryCode),GoodsCode=values(GoodsCode),GoodsName=values(GoodsName),ShopTitle=values(ShopTitle)," \
                                   "BarCode=values(BarCode),FitCode=values(FitCode),MultiStyle=values(MultiStyle),Material=values(Material),Class=values(Class),Model=values(Model),Unit=values(Unit)," \
                                   "Style=values(Style),Brand=values(Brand),LocationID=values(LocationID),Quantity=values(Quantity),SalePrice=values(SalePrice),CostPrice=values(CostPrice)," \
                                   "AliasCnName=values(AliasCnName),AliasEnName=values(AliasEnName),Weight=values(Weight),DeclaredValue=values(DeclaredValue),OriginCountry=values(OriginCountry)," \
                                   "OriginCountryCode=values(OriginCountryCode),ExpressID=values(ExpressID),Used=values(Used),BmpFileName=values(BmpFileName),BmpUrl=values(BmpUrl),MaxNum=values(MaxNum)," \
                                   "MinNum=values(MinNum),GoodsCount=values(GoodsCount),SupplierID=values(SupplierID),Notes=values(Notes),SampleFlag=values(SampleFlag),SampleCount=values(SampleCount)," \
                                   "SampleMemo=values(SampleMemo),CreateDate=values(CreateDate),GroupFlag=values(GroupFlag),SalerName=values(SalerName),SellCount=values(SellCount),SellDays=values(SellDays)," \
                                   "PackFee=values(PackFee),PackName=values(PackName),GoodsStatus=values(GoodsStatus),DevDate=values(DevDate),SalerName2=values(SalerName2),BatchPrice=values(BatchPrice)," \
                                   "MaxSalePrice=values(MaxSalePrice),RetailPrice=values(RetailPrice),MarketPrice=values(MarketPrice),PackageCount=values(PackageCount)," \
                                   "ChangeStatusTime=values(ChangeStatusTime),StockDays=values(StockDays),StoreID=values(StoreID),Purchaser=values(Purchaser),LinkUrl=values(LinkUrl)," \
                                   "LinkUrl2=values(LinkUrl2),LinkUrl3=values(LinkUrl3),StockMinAmount=values(StockMinAmount),MinPrice=values(MinPrice),HSCODE=values(HSCODE),ViewUser=values(ViewUser)," \
                                   "InLong=values(InLong),InWide=values(InWide),InHigh=values(InHigh),InGrossweight=values(InGrossweight),InNetweight=values(InNetweight),OutLong=values(OutLong)," \
                                   "OutWide=values(OutWide),OutHigh=values(OutHigh),OutGrossweight=values(OutGrossweight),OutNetweight=values(OutNetweight),ShopCarryCost=values(ShopCarryCost)," \
                                   "ExchangeRate=values(ExchangeRate),WebCost=values(WebCost),PackWeight=values(PackWeight),LogisticsCost=values(LogisticsCost),GrossRate=values(GrossRate)," \
                                   "CalSalePrice=values(CalSalePrice),CalYunFei=values(CalYunFei),CalSaleAllPrice=values(CalSaleAllPrice),PackMsg=values(PackMsg),ItemUrl=values(ItemUrl)," \
                                   "IsCharged=values(IsCharged),DelInFile=values(DelInFile),Season=values(Season),IsPowder=values(IsPowder),IsLiquid=values(IsLiquid),possessMan1=values(possessMan1)," \
                                   "possessMan2=values(possessMan2),LinkUrl4=values(LinkUrl4),LinkUrl5=values(LinkUrl5),LinkUrl6=values(LinkUrl6),isMagnetism=values(isMagnetism)," \
                                   "NoSalesDate=values(NoSalesDate),AttributeName=values(AttributeName)"
                    strSQL = strOnlineSql
                    self.sqlcursor.executemany(strSQL,tupperPY_b_goods)
                    self.db_conn.commit()
                    nidRange = nidRange + nCount
                    self.Recordlog("nid:%s" % (nidRange), "success", sys._getframe().f_lineno)
                except Exception as e:
                    self.Recordlog(str(e) + ";nid:%s"%(nidRange), "error", sys._getframe().f_lineno)
                    nidRange = nidRange + 10
                    continue
            self.closeSql(111)
            self.closeSql(10)
            updateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self.Recordlog("end b_goods syn dealtime:%s" % (updateTime), "info", sys._getframe().f_lineno)
        except Exception as e:
            self.closeSql(111)
            self.closeSql(10)
            self.Recordlog(str(e) + ";set_online_b_goods error", "error", sys._getframe().f_lineno)

    def update_b_goods_mainsku(self):
        try:
            reload(sys)
            sys.setdefaultencoding('utf8')
            self.connSql(111)
            updateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self.Recordlog("start update_b_goods_mainsku syn dealtime:%s" % (updateTime), "info", sys._getframe().f_lineno)
            strHQSql = "UPDATE py_db.b_goods set MainSKU=getMainSKU(SKU) where MainSKU is NULL or MainSKU=''; "
            self.sqlcursor.execute(strHQSql)
            self.db_conn.commit()
            self.closeSql(111)
            updateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self.Recordlog("end update_b_goods_mainsku syn dealtime:%s" % (updateTime), "info", sys._getframe().f_lineno)
        except Exception as e:
            self.Recordlog(e.message + ";update_b_goods_mainsku error", "error", sys._getframe().f_lineno)

    def get_py_b_supplier(self,minRange,MaxRange):
        try:
            strPYSql = "select NID,CategoryID,SupplierCode,SupplierName,FitCode,LinkMan,Address,OfficePhone,Mobile,Used,Recorder,InputDate,Modifier,ModifyDate,Email,QQ,MSN,ArrivalDays,URL,Memo," \
                       "Account,CreateDate,SupPurchaser,supplierLoginId  from b_supplier(nolock) where NID >=%s and NID < %s"%(minRange,MaxRange)
            n = self.sqlcursor_py.execute(strPYSql)
            sSupplierArray = self.sqlcursor_py.fetchall()
            return sSupplierArray
        except Exception as e:
            self.Recordlog(e.message + ";get_py_b_supplier error", "error", sys._getframe().f_lineno)

    def set_online_b_supplier(self):
        try:
            reload(sys)
            sys.setdefaultencoding('utf8')
            self.connSql(111)
            self.connSql(10)
            updateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self.Recordlog("start b_supplier syn dealtime:%s" % (updateTime), "info", sys._getframe().f_lineno)
            maxNid = self.get_py_b_supplier_maxnid()
            nidRange = 0
            nCount = 3000
            while nidRange < maxNid:
                try:
                    tupperPY_b_supplier = self.get_py_b_supplier(nidRange,nidRange+nCount)
                    strOnlineSql = "insert into py_db.b_supplier(NID,CategoryID,SupplierCode,SupplierName,FitCode,LinkMan,Address,OfficePhone,Mobile,Used,Recorder,InputDate,Modifier,ModifyDate," \
                                   "Email,QQ,MSN,ArrivalDays,URL,Memo,Account,CreateDate,SupPurchaser,supplierLoginId) " \
                                   "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update " \
                                   "SupplierCode=values(SupplierCode),SupplierName=values(SupplierName),FitCode=values(FitCode),LinkMan=values(LinkMan),Address=values(Address)," \
                                   "OfficePhone=values(OfficePhone),Mobile=values(Mobile),Used=values(Used),Recorder=values(Recorder),InputDate=values(InputDate),Modifier=values(Modifier)," \
                                   "ModifyDate=values(ModifyDate),Email=values(Email),QQ=values(QQ),MSN=values(MSN),ArrivalDays=values(ArrivalDays),URL=values(URL)," \
                                   "Memo=values(Memo),Account=values(Account),CreateDate=values(CreateDate),SupPurchaser=values(SupPurchaser),supplierLoginId=values(supplierLoginId)"

                    strSQL = strOnlineSql
                    self.sqlcursor.executemany(strSQL,tupperPY_b_supplier)
                    self.db_conn.commit()
                    nidRange = nidRange + nCount
                    self.Recordlog("nid:%s" % (nidRange), "success", sys._getframe().f_lineno)
                except Exception as e:
                    self.Recordlog(str(e) + ";nid:%s"%(nidRange), "error", sys._getframe().f_lineno)
                    nidRange = nidRange + 10
                    continue
            self.closeSql(111)
            self.closeSql(10)
            updateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self.Recordlog("end b_supplier syn dealtime:%s" % (updateTime), "info", sys._getframe().f_lineno)
        except Exception as e:
            self.closeSql(111)
            self.closeSql(10)
            self.Recordlog(str(e) + ";set_online_b_supplier error", "error", sys._getframe().f_lineno)

    def get_py_b_dictionary(self):
        try:
            strPYSql = "select NID,CategoryID,DictionaryName,FitCode,Used,Memo,tradeType from B_Dictionary(nolock) "
            n = self.sqlcursor_py.execute(strPYSql)
            sDictionaryArray = self.sqlcursor_py.fetchall()
            return sDictionaryArray
        except Exception as e:
            self.Recordlog(e.message + ";get_py_b_dictionary error", "error", sys._getframe().f_lineno)

    def set_py_b_dictionary(self):
        try:
            reload(sys)
            sys.setdefaultencoding('utf8')
            self.connSql(111)
            self.connSql(10)
            updateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self.Recordlog("start b_dictionary syn dealtime:%s" % (updateTime), "info", sys._getframe().f_lineno)
            try:
                tupperPY_b_dictionary = self.get_py_b_dictionary()
                strOnlineSql = "insert into py_db.b_dictionary(NID,CategoryID,DictionaryName,FitCode,Used,Memo,tradeType) " \
                               "values(%s,%s,%s,%s,%s,%s,%s) on duplicate key update " \
                               "CategoryID=values(CategoryID),DictionaryName=values(DictionaryName),FitCode=values(FitCode),Used=values(Used),Memo=values(Memo)," \
                               "tradeType=values(tradeType)"
                self.sqlcursor.executemany(strOnlineSql,tupperPY_b_dictionary)
                self.db_conn.commit()
                self.Recordlog("nid:0", "success", sys._getframe().f_lineno)
            except Exception as e:
                self.Recordlog(str(e), "error", sys._getframe().f_lineno)
            self.closeSql(111)
            self.closeSql(10)
            updateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self.Recordlog("end b_dictionary syn dealtime:%s" % (updateTime), "info", sys._getframe().f_lineno)
        except Exception as e:
            self.closeSql(111)
            self.closeSql(10)
            self.Recordlog(str(e) + ";set_py_b_dictionary error", "error", sys._getframe().f_lineno)

    def get_py_B_GoodsSKUWith1688(self,minNid,maxNid):
        try:
            strPYSql = "select bg1688.nid,bg1688.GoodsSKUID,bg1688.offerid,bg1688.specId,bg1688.supplierLoginId,bg1688.companyName,bg1688.isDefault,bgsku.SKU,bgsku.GoodsID " \
                       "from B_GoodsSKUWith1688(nolock) bg1688 left join B_GoodsSKU(nolock) bgsku on bg1688.GoodsSKUID=bgsku.NID where bg1688.NID >=%s and bg1688.NID < %s "%(minNid,maxNid)
            n = self.sqlcursor_py.execute(strPYSql)
            sGoodsSKUWith1688 = self.sqlcursor_py.fetchall()
            return sGoodsSKUWith1688
        except Exception as e:
            self.Recordlog(e.message + ";get_py_B_GoodsSKUWith1688 error", "error", sys._getframe().f_lineno)

    def set_py_B_GoodsSKUWith1688(self):
        try:
            reload(sys)
            sys.setdefaultencoding('utf8')
            self.connSql(111)
            self.connSql(10)
            updateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self.Recordlog("start set_py_B_GoodsSKUWith1688 syn dealtime:%s" % (updateTime), "info", sys._getframe().f_lineno)
            maxNid = self.get_py_B_GoodsSKUWith1688_maxnid()
            nidRange = 0
            nCount = 3000
            while nidRange < maxNid:
                try:
                    tupperPY_B_GoodsSKUWith1688 = self.get_py_B_GoodsSKUWith1688(nidRange,nidRange+nCount)
                    strOnlineSql = "insert into py_db.B_GoodsSKUWith1688(nid,GoodsSKUID,offerid,specId,supplierLoginId,companyName,isDefault,SKU,GoodsID) " \
                                   "values(%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update " \
                                   "GoodsSKUID=values(GoodsSKUID),offerid=values(offerid),specId=values(specId),supplierLoginId=values(supplierLoginId),companyName=values(companyName)," \
                                   "isDefault=values(isDefault),SKU=values(SKU),GoodsID=values(GoodsID)"
                    strSQL = strOnlineSql
                    self.sqlcursor.executemany(strSQL,tupperPY_B_GoodsSKUWith1688)
                    self.db_conn.commit()
                    nidRange = nidRange + nCount
                    self.Recordlog("nid:%s" % (nidRange), "success", sys._getframe().f_lineno)
                except Exception as e:
                    self.Recordlog(str(e) + ";nid:%s"%(nidRange), "error", sys._getframe().f_lineno)
                    nidRange = nidRange + 1
                    continue
            self.closeSql(111)
            self.closeSql(10)
            updateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self.Recordlog("end set_py_B_GoodsSKUWith1688 syn dealtime:%s" % (updateTime), "info", sys._getframe().f_lineno)
        except Exception as e:
            self.closeSql(111)
            self.closeSql(10)
            self.Recordlog(str(e) + ";set_py_B_GoodsSKUWith1688 error", "error", sys._getframe().f_lineno)

    def syn_py_table(self):
        #self.set_py_b_dictionary()
        #self.set_online_b_supplier()
        #self.set_online_b_goods()
        #self.update_b_goods_mainsku()
        self.set_py_B_GoodsSKUWith1688()
tt = syn_b_goods()
tt.syn_py_table()
