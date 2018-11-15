# coding:utf-8
"""
@author: ZhangYu
@contact: 292724306@qq.com
@site:
@software: PyCharm
@time: 2017-12-30 13:27
"""

import ConfigParser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pymssql
import MySQLdb
from datetime import datetime
import calendar
import time
import pandas as pd

class public:
    def __init__(self,db_conn=None, sqlserver_conn=None):
        cf = ConfigParser.ConfigParser()
        cf.read("brick/pydata/py_syn/select.conf")
        self.maxnum = cf.getint('myconfig', 'maxnum')
        self.logMaxnum = cf.getint('myconfig', 'logMaxnum')
        self.db_conn = db_conn
        self.sqlserver_conn = sqlserver_conn
        if self.db_conn:
            self.cursor = self.db_conn.cursor()

    def fetchmanyFun(self, sqlcursor):
        objs = []
        maxnum = self.logMaxnum
        while True:
            objsTmps = sqlcursor.fetchmany(maxnum)
            for objsTmp in objsTmps:
                objs.append(objsTmp)
            if len(objsTmps) < maxnum:
                for objsTmp in objsTmps:
                    objs.append(objsTmp)
                break
        return objs

    def getSKU(self, GoodsSKUIDs):
        SKUList = []
        try:
            x = ','.join(['%s'] * len(GoodsSKUIDs))
            SKUSql = 'select SKU from py_db.b_goods where NID in (%s)' % x
            self.cursor.execute(SKUSql, tuple(GoodsSKUIDs))
            SKUtmp = self.cursor.fetchall()
            if SKUtmp:
                for SKU in SKUtmp:
                    SKUList.append(SKU[0])
            return SKUList
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def getGoodsSKUIDs(self, SKUList):
        GoodsSKUIDs = []
        try:
            x = ','.join(['%s'] * len(SKUList))
            SKUIDSql = 'select NID from py_db.b_goodssku where SKU in (%s)' % x
            self.cursor.execute(SKUIDSql, tuple(SKUList))
            SKUIDtmp = self.cursor.fetchall()
            if SKUIDtmp:
                for SKUID in SKUIDtmp:
                    GoodsSKUIDs.append(SKUID[0])
            else:
                return ''
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            return ''
        else:
            return GoodsSKUIDs

    def setNumEmpty(self,strNumber):
        try:
            float(strNumber)
            return 0 if strNumber == "" or strNumber is None  else strNumber
        except Exception, ex:
            return 0

    def getSKUList(self):
        SKUList = []
        ids = []
        try:
            sql = "SELECT SKU, status,Op_time from t_product_puyuan_op where `status` in (1,2,3)"
            self.cursor.execute(sql)
            objs = self.cursor.fetchall()
            if objs:
                for obj in objs:
                    SKUList.append(obj[0])
            else:
                return ''
            NIDSql = "SELECT id from t_product_puyuan_op where `status` in (1,2,3)"
            self.cursor.execute(NIDSql)
            idObjs = self.cursor.fetchall()
            if idObjs:
                for idObj in idObjs:
                    ids.append(idObj[0])
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            return ''
        else:
            return objs, SKUList, ids


    def commitmanyFun(self, objs, sql):
        if objs and sql:
            i = 0
            while True:
                i += 1
                print i
                if len(objs) > self.maxnum:
                    objs_tmp = objs[:self.maxnum]
                    try:
                        # print datetime.now()
                        insertSql = sql
                        self.cursor.executemany(insertSql, objs_tmp)
                        print "大于"
                        # print datetime.now()
                    except MySQLdb.Error, e:
                        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                    else:
                        objs = objs[self.maxnum:]
                else:
                    try:
                        # print datetime.now()
                        insertSql = sql
                        self.cursor.executemany(insertSql, objs)
                        self.cursor.execute('commit')
                        print "小于"
                        break
                        # print datetime.now()
                    except MySQLdb.Error, e:
                        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                        self.db_conn.rollback()

    def setStatus(self, task, status):
        cursor = self.db_conn.cursor()
        try:
            sql = "update py_db.t_celery_task_status set status='{0}',optime='{1}' where task='{2}'".format(status, datetime.now(), task)
            cursor.execute(sql)
            cursor.execute("commit")
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def get_CG_StockOrderCount(self, report_date, pyuanConn, onlineConn):
        # 计算report_date月初和月末
        result = {}
        try:
            # 格式化入参日期
            day_now = time.localtime()
            report_date_format = time.strptime(report_date, "%Y-%m")
            day_begin = '%d-%02d-01' % (report_date_format.tm_year, report_date_format.tm_mon)
            wday, monthRange = calendar.monthrange(report_date_format.tm_year, report_date_format.tm_mon)
            day_end = '%d-%02d-%02d' % (report_date_format.tm_year, report_date_format.tm_mon, monthRange)
            month_yyyymm = '%d%02d' % (report_date_format.tm_year, report_date_format.tm_mon)
            cur_date = '%d-%02d-%02d' % (day_now.tm_year, day_now.tm_mon, day_now.tm_mday)
            optime = '%d-%02d-%02d-%02d-%02d-%02d' % (
            day_now.tm_year, day_now.tm_mon, day_now.tm_mday, day_now.tm_hour, day_now.tm_min, day_now.tm_sec)
            # 入参日期月末是否小于当前时间，用于标识当前生成的报表是完整月还是非完整月 1：完整月 0：非完整
            if day_end < cur_date:
                flag = 1
            else:
                flag = 0
            sqlcursor = pyuanConn.cursor()
            cur_conn = onlineConn.cursor()
            # 删除历史报表数据
            sql = " delete from t_report_supplier_sku_m where yyyymm = '%s'" % month_yyyymm
            print sql
            cur_conn.execute(sql)
            cur_conn.execute("commit;")
            sql = "exec P_CG_StockOrderCount_hq '%s','%s','','','','','',6" % (day_begin, day_end)
            # sql = "exec P_CG_StockOrderCount_hq '2018-06-26','2018-06-27','','','','','',6"
            sqlcursor.execute(sql)
            objs = sqlcursor.fetchall()
            for obj in objs:
                if obj:
                    # 计算sku占用率
                    if obj[8] == 0:
                        skuoccupancy = -1
                    else:
                        skuoccupancy = float(obj[7]) / float(obj[8])
                    sql = "insert into t_report_supplier_sku_m (yyyymm,SupplierID,SupplierName,CGAllcount,CGALLmoney,INAllcount,INALLmoney,CGOrdercount,CGSKUcount,SupplierSKUcount,SupplierCreateDate,optime,flag,sku_occupancy,alibabasellername) " \
                          "VALUES (%s,'%s','%s',%s,%s,%s,%s,%s,%s,%s,'%s','%s','%s',%s,'%s')" % (month_yyyymm, obj[0], obj[1], obj[2], obj[3], obj[4], obj[5], obj[6], obj[7], obj[8], obj[9],optime, flag, skuoccupancy, obj[10])
                    cur_conn.execute(sql)
            cur_conn.execute("commit;")
            result['errorcode'] = 0
        except Exception, ex:
            result['errorcode'] = -1
            result['errortext'] = 'Exception = %s ex=%s  __LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)
            #return result['errortext']
        cur_conn.close()
        sqlcursor.close()
        return result['errorcode']

    def sku_info_to_pydb(self, b_goods_data_list, sqlserverInfo, mainsku, pydb_connect):
        from brick.pydata.py_syn.b_goods import b_goods

        result = {'errorcode': 0,'errortext':""}
        existsSKU = []
        id_list = []
        sqlcursor = sqlserverInfo['py_cursor']
        SKUList = []
        for b_goods_data in b_goods_data_list:
            if len(b_goods_data) > 0:
                try:
                    strSelectSql = "select NID from B_Supplier where SupplierName='%s'" % (b_goods_data['SupplierName'])
                    sqlcursor.execute(strSelectSql)
                    supplierID = sqlcursor.fetchone()
                    if supplierID is None:
                        result['errorcode'] = -1
                        result['errortext'] = u'供应商:%s,未查找到供应商信息'%(b_goods_data['SupplierName'])
                        break
                    #判断SKU是否存在
                    strSelectSql = "select count(1) from b_goods where sku='%s'"%(b_goods_data['SKU'])
                    sqlcursor.execute(strSelectSql)
                    nCount = sqlcursor.fetchone()
                    if nCount[0] > 0:
                        existsSKU.append(b_goods_data['SKU'])
                        continue
                    MultiStyle = 1 if b_goods_data['MultiStyle'] == u'是' else 0
                    # 库位信息默认：657897
                    b_goods_data['LocationID'] = 657897
                    SKUList.append(b_goods_data['SKU'])
                    # sql1 = " insert into b_goods (GoodsCode,GoodsName," \
                    #        "SKU,MultiStyle," \
                    #        "Material,Model," \
                    #        "Unit,Brand,LocationID," \
                    #        "CostPrice,AliasCnName," \
                    #        "AliasEnName,Weight," \
                    #        "DeclaredValue,OriginCountry," \
                    #        "OriginCountryCode,Notes," \
                    #        "CreateDate,SalerName," \
                    #        "SellDays,PackFee,GoodsStatus,DevDate," \
                    #        "PackName,SalerName2," \
                    #        "PackageCount,StockDays," \
                    #        "Purchaser,LinkUrl," \
                    #        "LinkUrl2,StockMinAmount," \
                    #        "possessMan2,LinkUrl4) VALUES " \
                    #        "('%s','%s'," \
                    #        "'%s','%s'," \
                    #        "'%s','%s'," \
                    #        "'%s','%s','%s'," \
                    #        "'%s','%s'," \
                    #        "'%s','%s'," \
                    #        "'%s','%s'," \
                    #        "'%s','%s'," \
                    #        "'%s','%s'," \
                    #        "'%s','%s','%s','%s'," \
                    #        "'%s','%s'," \
                    #        "'%s','%s'," \
                    #        "'%s','%s'," \
                    #        "'%s','%s'," \
                    #        "'%s','%s')" \
                    #        % (b_goods_data['GoodsCode'], b_goods_data['GoodsName'],
                    #           b_goods_data['SKU'], MultiStyle,
                    #           b_goods_data['Material'], b_goods_data['Model'],
                    #           b_goods_data['Unit'], b_goods_data['Brand'], b_goods_data['LocationID'],
                    #           b_goods_data['CostPrice'], b_goods_data['AliasCnName'],
                    #           b_goods_data['AliasEnName'], b_goods_data['Weight'],
                    #           b_goods_data['DeclaredValue'], b_goods_data['OriginCountry'],
                    #           b_goods_data['OriginCountryCode'], b_goods_data['Notes'].replace("\n", ""),
                    #           b_goods_data['CreateDate'], b_goods_data['SalerName'],
                    #           b_goods_data['SellDays'], b_goods_data['PackFee'], b_goods_data['GoodsStatus'],
                    #           b_goods_data['CreateDate'],
                    #           b_goods_data['PackName'], b_goods_data['SalerName2'],
                    #           b_goods_data['PackageCount'], b_goods_data['StockDays'],
                    #           b_goods_data['Purchaser'], b_goods_data['LinkUrl'],
                    #           b_goods_data['LinkUrl2'], b_goods_data['StockMinAmount'],
                    #           b_goods_data['possessMan2'], b_goods_data['LinkUrl4'])
                    sql1 = " insert into b_goods (GoodsCode,GoodsName,ShopTitle,SKU,BarCode,FitCode,MultiStyle,Material,Class,Model," \
                           "Unit,Style,Brand,LocationID,Quantity,SalePrice, CostPrice, AliasCnName, AliasEnName,Weight," \
                           "DeclaredValue,OriginCountry,OriginCountryCode, ExpressID, Used, BmpFileName, BmpUrl, MaxNum, MinNum,GoodsCount," \
                           "SupplierID,Notes,SampleFlag, SampleCount, SampleMemo,CreateDate,GroupFlag,SalerName,SellCount,SellDays," \
                           "PackFee,PackName,GoodsStatus,DevDate,SalerName2,BatchPrice, MaxSalePrice, RetailPrice, MarketPrice, PackageCount," \
                           "ChangeStatusTime,StockDays,StoreID, Purchaser, LinkUrl, LinkUrl2, LinkUrl3, StockMinAmount, MinPrice, HSCODE, " \
                           "ViewUser, InLong, InWide, InHigh, InGrossweight, InNetweight, OutLong, OutWide, OutHigh, OutGrossweight, " \
                           "OutNetweight, ShopCarryCost, ExchangeRate, WebCost, PackWeight, LogisticsCost, GrossRate, CalSalePrice, CalYunFei, CalSaleAllPrice, " \
                           "PackMsg, ItemUrl, IsCharged, DelInFile, Season, IsPowder, IsLiquid, possessMan1, possessMan2, LinkUrl4, " \
                           "LinkUrl5, LinkUrl6, isMagnetism, NoSalesDate, NotUsedReason, PackingRatio, shippingType, FreightRate) " \
                           "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                           "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                           "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                           "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                           "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    param1 = (
                        b_goods_data['GoodsCode'], b_goods_data['GoodsName'], b_goods_data['ShopTitle'], b_goods_data['SKU'],b_goods_data['BarCode'],
                        b_goods_data['FitCode'],MultiStyle,b_goods_data['Material'],b_goods_data['Class'],b_goods_data['Model'],
                        b_goods_data['Unit'], b_goods_data['Style'], b_goods_data['Brand'], self.setNumEmpty(b_goods_data['LocationID']),self.setNumEmpty(b_goods_data['Quantity']),
                        self.setNumEmpty(b_goods_data['SalePrice']),self.setNumEmpty(b_goods_data['CostPrice']), b_goods_data['AliasCnName'],b_goods_data['AliasEnName'], self.setNumEmpty(b_goods_data['Weight']),
                        self.setNumEmpty(b_goods_data['DeclaredValue']),b_goods_data['OriginCountry'], b_goods_data['OriginCountryCode'],self.setNumEmpty(b_goods_data['ExpressID']), self.setNumEmpty(b_goods_data['Used']),
                        b_goods_data['BmpFileName'], b_goods_data['BmpUrl'], self.setNumEmpty(b_goods_data['MaxNum']),self.setNumEmpty(b_goods_data['MinNum']), self.setNumEmpty(b_goods_data['GoodsCount']),
                        self.setNumEmpty(b_goods_data['SupplierID']),b_goods_data['Notes'].replace("\n", ""), self.setNumEmpty(b_goods_data['SampleFlag']),self.setNumEmpty(b_goods_data['SampleCount']),b_goods_data['SampleMemo'],
                        b_goods_data['CreateDate'], self.setNumEmpty(b_goods_data['GroupFlag']),b_goods_data['SalerName'],self.setNumEmpty(b_goods_data['SellCount']),self.setNumEmpty(b_goods_data['SellDays']),
                        self.setNumEmpty(b_goods_data['PackFee']), b_goods_data['PackName'],b_goods_data['GoodsStatus'],b_goods_data['CreateDate'],b_goods_data['SalerName2'],
                        self.setNumEmpty(b_goods_data['BatchPrice']), self.setNumEmpty(b_goods_data['MaxSalePrice']), self.setNumEmpty(b_goods_data['RetailPrice']),self.setNumEmpty(b_goods_data['MarketPrice']), self.setNumEmpty(b_goods_data['PackageCount']),
                        datetime.now(), self.setNumEmpty(b_goods_data['StockDays']),self.setNumEmpty(b_goods_data['StoreID']), b_goods_data['Purchaser'],b_goods_data['LinkUrl'],
                        b_goods_data['LinkUrl2'], b_goods_data['LinkUrl3'], self.setNumEmpty(b_goods_data['StockMinAmount']),self.setNumEmpty(b_goods_data['MinPrice']),b_goods_data['HSCODE'],
                        b_goods_data['ViewUser'], self.setNumEmpty(b_goods_data['InLong']),self.setNumEmpty(b_goods_data['InWide']), self.setNumEmpty(b_goods_data['InHigh']),self.setNumEmpty(b_goods_data['InGrossweight']),
                        self.setNumEmpty(b_goods_data['InNetweight']), self.setNumEmpty(b_goods_data['OutLong']), self.setNumEmpty(b_goods_data['OutWide']),self.setNumEmpty(b_goods_data['OutHigh']), self.setNumEmpty(b_goods_data['OutGrossweight']),
                        self.setNumEmpty(b_goods_data['OutNetweight']), self.setNumEmpty(b_goods_data['ShopCarryCost']), self.setNumEmpty(b_goods_data['ExchangeRate']),self.setNumEmpty(b_goods_data['WebCost']), self.setNumEmpty(b_goods_data['PackWeight']),
                        self.setNumEmpty(b_goods_data['LogisticsCost']), self.setNumEmpty(b_goods_data['GrossRate']), self.setNumEmpty(b_goods_data['CalSalePrice']),self.setNumEmpty(b_goods_data['CalYunFei']), self.setNumEmpty(b_goods_data['CalSaleAllPrice']),
                        b_goods_data['PackMsg'], b_goods_data['ItemUrl'], self.setNumEmpty(b_goods_data['IsCharged']),self.setNumEmpty(b_goods_data['DelInFile']), b_goods_data['Season'],
                        self.setNumEmpty(b_goods_data['IsPowder']), self.setNumEmpty(b_goods_data['IsLiquid']), b_goods_data['possessMan1'],b_goods_data['possessMan2'], b_goods_data['LinkUrl4'],
                        b_goods_data['LinkUrl5'], b_goods_data['LinkUrl6'], self.setNumEmpty(b_goods_data['isMagnetism']),datetime.now(), b_goods_data['NotUsedReason'],
                        self.setNumEmpty(b_goods_data['PackingRatio']), self.setNumEmpty(b_goods_data['shippingType']), self.setNumEmpty(b_goods_data['FreightRate'])
                    )
                    sql7 = "select top 1 categorycode from B_GoodsCats WHERE CategoryName = '%s'" % b_goods_data['SmallCategoryName']
                    sqlcursor.execute(sql7)
                    objs = sqlcursor.fetchall()
                    CategoryName = b_goods_data['LargeCategoryName']
                    if len(objs) > 0:
                        CategoryName = b_goods_data['SmallCategoryName']
                    sql4 = "update b_goods set GoodsStatus = '在售', GoodsCategoryID = (select top 1 nid from B_GoodsCats where CategoryName = '%s'),CategoryCode=(select top 1 categorycode from B_GoodsCats " \
                               "where CategoryName = '%s'),supplierid=(select top 1 nid from B_Supplier where SupplierName = '%s'),storeid=(SELECT top 1 nid from b_store(nolock) where storename ='%s') where sku = '%s'" \
                               %(CategoryName,CategoryName,b_goods_data['SupplierName'],b_goods_data['Storehouse'],b_goods_data['SKU'])
                    sql2 = "update b_goodssku set BmpFileName = '%s',goodsskustatus = '正常',ChangeStatusTime = getdate() where goodsid = (select top 1 nid from b_goods(nolock) where sku = '%s')" % (
                    b_goods_data['BmpFileName'], b_goods_data['SKU'])
                    sql3 = "insert into KC_CurrentStock (storeid,goodsskuid,goodsid) VALUES ((SELECT top 1 nid from b_store(nolock) where storename ='%s')," \
                           "(SELECT top 1 nid from b_goodssku(nolock) where sku ='%s'),(select top 1 nid from b_goods(nolock) where sku ='%s'))" % (
                           b_goods_data['Storehouse'], b_goods_data['SKU'], b_goods_data['SKU'])
                    sql5 = "delete from b_GoodsAttribute where goodsid = (select top 1 nid from b_goods(nolock) where sku = '%s')" % \
                           b_goods_data['SKU']
                    sql6 = "insert into b_GoodsAttribute (goodsid,Attributename) VALUES ((select top 1 nid from b_goods(nolock) where sku = '%s'),'%s')" % (
                    b_goods_data['SKU'], b_goods_data['ProductAttr'])
                    sqlcursor.execute(sql1, param1)
                    id_list.append(int(sqlcursor.lastrowid))
                    sqlcursor.execute(sql2)
                    sqlcursor.execute(sql3)
                    sqlcursor.execute(sql4)
                    sqlcursor.execute(sql5)
                    sqlcursor.execute(sql6)

                    if b_goods_data.get('AI_FLAG') == '1':
                        sql7 = "update KC_CurrentStock set WarningCats='wradvanceStock' WHERE goodsskuid=(SELECT top 1 nid from b_goodssku(nolock) where sku ='%s')" \
                               % b_goods_data['SKU']
                        sqlcursor.execute(sql7)  # 如果是精准调研的产品，直接是 提前备货的商品
                except Exception, ex:
                    result['errorcode'] = -1
                    if 'duplicate key' in str(ex):
                        result['errortext'] = u'普源已有SKU：%s' % b_goods_data['SKU']
                    else:
                        result['errortext'] = 'Exception = %s ex=%s  __LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)
                    break
            else:
                result['errorcode'] = -1
                result['errortext'] = u'入参data为空'
        if result['errorcode'] == -1:
            sqlserverInfo['py_conn'].rollback()
            #for id_no in id_list:
            #    sql = "delete from b_goods where nid = %s" % id_no
            #    sqlcursor.execute(sql)
        else:
            sqlserverInfo['py_conn'].commit()
            if existsSKU:
                result['errorcode'] = -1
                result['errortext'] = str(existsSKU) + u'SKU重复，其他已录入成功'
            b_goods_obj = b_goods(pydb_connect, sqlserverInfo['py_conn'])
            if SKUList:
                b_goods_obj.update_b_goods(SKUList,mainsku)
        #sqlcursor.close()
        return result


    '''
    说明:ShopSKU 绑定，操作普源新增、修改、删除绑定关系
    入参:shopsku字典信息(包含:SKU、ShopSKU、memo、personcode)，普源链接
    出参:结果按字典格式返回(包含:错误码、错误信息)
    '''
    def goodsskulinkshop_info_to_pydb(self, b_goodsskulinkshop_data_list, sqlserverInfo):
        result = {'errorcode': 0}
        id_list = []
        notExistsSKU = []
        sqlcursor = sqlserverInfo['py_cursor']
        if sqlcursor is None or sqlcursor == "":
            result['errorcode'] = -1
            result['errortext'] = 'sqlserver_conn can not conn'
            return result
        #b_goodsskulinkshop_data["flag"] add :新建  delete:解绑
        for b_goodsskulinkshop_data in b_goodsskulinkshop_data_list:
            if len(b_goodsskulinkshop_data) > 0:
                try:
                    selectSql = ""
                    InsertUpdateSql = ""
                    deleteSql = ""
                    if b_goodsskulinkshop_data["opflag"] == "add":
                        # 判断SKU是否存在
                        if b_goodsskulinkshop_data['SKU'][:2] == 'ZH':
                            strSelectSql = "select count(1) from b_goods where sku='%s'" % (b_goodsskulinkshop_data['SKU'])
                            sqlcursor.execute(strSelectSql)
                            nCount = sqlcursor.fetchone()
                            if nCount[0] == 0:
                                notExistsSKU.append(b_goodsskulinkshop_data['SKU'])
                                continue
                        selectSql = "select count(1) from B_GoodsSKULinkShop where ShopSKU=%s;"
                        param1 = (b_goodsskulinkshop_data['ShopSKU'])
                        sqlcursor.execute(selectSql,param1)
                        nCount = sqlcursor.fetchone()
                        if nCount[0] > 0:
                            InsertUpdateSql = "update B_GoodsSKULinkShop set memo=%s,PersonCode=%s,ShopName=%s where ShopSKU=%s"
                            param2 = (b_goodsskulinkshop_data['Memo'], b_goodsskulinkshop_data['PersonCode'],b_goodsskulinkshop_data['ShopName'], b_goodsskulinkshop_data['ShopSKU'])
                            sqlcursor.execute(InsertUpdateSql,param2)
                        else:
                            InsertUpdateSql = "INSERT INTO B_GoodsSKULinkShop(SKU,ShopSKU,memo,PersonCode,ShopName)  VALUES(%s,%s,%s,%s,%s)"
                            param2 = (b_goodsskulinkshop_data['SKU'], b_goodsskulinkshop_data['ShopSKU'], b_goodsskulinkshop_data['Memo'], b_goodsskulinkshop_data['PersonCode'],b_goodsskulinkshop_data['ShopName'])
                            sqlcursor.execute(InsertUpdateSql,param2)
                    elif b_goodsskulinkshop_data["opflag"] == "delete":
                        deleteSql = "delete from B_GoodsSKULinkShop where SKU=%s and ShopSKU=%s"
                        param3 = (b_goodsskulinkshop_data['SKU'], b_goodsskulinkshop_data['ShopSKU'])
                        sqlcursor.execute(deleteSql,param3)
                    elif b_goodsskulinkshop_data["opflag"] == 'update':
                        # 仅在合并SKU时，批量修改商品SKU绑定关系时使用
                        updateSql = "update B_GoodsSKULinkShop set SKU=%s WHERE SKU=%s"
                        param4 = (b_goodsskulinkshop_data['retain_sku'], b_goodsskulinkshop_data['delete_sku'])
                        sqlcursor.execute(updateSql, param4)
                    else:
                        result['errorcode'] = -1
                        result['errortext'] = 'SKU和ShopSKU：%s,%s;opflag is error  __LINE__=%s' % (
                        b_goodsskulinkshop_data['SKU'], b_goodsskulinkshop_data['ShopSKU'],sys._getframe().f_lineno)
                        break
                except Exception, ex:
                    result['errorcode'] = -1
                    if 'duplicate key' in str(ex):
                        result['errortext'] = u'普源已有SKU和ShopSKU：%s,%s' % (b_goodsskulinkshop_data['SKU'], b_goodsskulinkshop_data['ShopSKU'])
                    else:
                        result['errortext'] = 'Exception = %s ex=%s;  __LINE__=%s' % (Exception, ex,sys._getframe().f_lineno)
                    break
            else:
                result['errorcode'] = -1
                result['errortext'] = '入参data为空'
                break
            if result['errorcode'] == -1:
                sqlserverInfo['py_conn'].rollback()
            else:
                sqlserverInfo['py_conn'].commit()
        if len(notExistsSKU) > 0 :
            result['errorcode'] = -1
            result['errortext'] = '以下商品SKU:%s不存在,请同步后再做绑定'%(str(notExistsSKU))
        return result

    '''
        说明:普源商品信息修改
        入参:shopsku字典信息(包含:SKU、ShopSKU、memo、personcode)，普源链接
        出参:结果按字典格式返回(包含:错误妈、错误信息)
        '''
    def b_goods_modify_to_pydb(self, b_goods_data_list, sqlserverInfo, pydb_connect):
        result = {'errorcode': 0}
        sqlcursor = sqlserverInfo['py_cursor']
        if sqlcursor is None or sqlcursor == "":
            result['errorcode'] = -1
            result['errortext'] = 'sqlserver_conn can not conn'
            return result
        for b_goods_data in b_goods_data_list:
            if len(b_goods_data) > 0:
                try:
                    #采购等级修改
                    if b_goods_data['columnname'] == "WarningCats":
                        # 判断SKU是否存在
                        UpdateSql = "update kc_currentstock set "+ b_goods_data['columnname'] +"='%s' where GoodsID = (select nid from B_Goods(nolock) where sku='%s') and " \
                                    "storeID = (select top 1 storeID from B_Goods(nolock) where SKU='%s');"%(b_goods_data['columnvalue'],b_goods_data['SKU'],b_goods_data['SKU'])
                        sqlcursor.execute(UpdateSql)
                    elif b_goods_data['columnname'] == "SupplierName":  #供应商修改
                        strSelectSql = "select NID from B_Supplier where SupplierName='%s'"%(b_goods_data['columnvalue'])
                        sqlcursor.execute(strSelectSql)
                        supplierID = sqlcursor.fetchone()
                        if supplierID:
                            strSelectSql = "select top 1 possessMan2 from b_goods where SupplierID=%s and possessMan2 != '' and possessMan2 is not null  and GoodsStatus != '停售'"
                            sqlcursor.execute(strSelectSql,supplierID[0])
                            possessMan2 = sqlcursor.fetchone()
                            strPossessMan2  = possessMan2[0] if possessMan2 else ""
                            UpdateSql = "update b_goods set SupplierID=%s,possessMan2=%s where SKU=%s"
                            parm3 = (supplierID[0],strPossessMan2, b_goods_data['SKU'])
                            sqlcursor.execute(UpdateSql, parm3)
                        else:
                            result['errorcode'] = -1
                            result['errortext'] = '未查找到对应供应商信息！'
                    elif b_goods_data['columnname'] == "GoodsStatus" :
                        use = 1 if b_goods_data['columnvalue'] == u"停售" else 0
                        UpdateSql = "update b_goods set " + b_goods_data['columnname'] + "=%s,Used=%s where SKU=%s"
                        parm2 = (b_goods_data['columnvalue'],use, b_goods_data['SKU'])
                        sqlcursor.execute(UpdateSql, parm2)
                    elif b_goods_data['columnname'] == "AttributeName" :
                        strSelectSql = "select top 1 nid from b_goods where SKU='%s'" % (b_goods_data['SKU'])
                        sqlcursor.execute(strSelectSql)
                        GoodsNid = sqlcursor.fetchone()
                        if GoodsNid:
                            strSelectSql = "select NID from B_GoodsAttribute where GoodsID='%s'"%(GoodsNid[0])
                            sqlcursor.execute(strSelectSql)
                            GoodsAttribute = sqlcursor.fetchone()
                            if GoodsAttribute:
                                UpdateSql = "update B_GoodsAttribute set " + b_goods_data['columnname'] + "=%s where GoodsID=%s"
                                parm2 = (b_goods_data['columnvalue'], GoodsNid[0])
                                sqlcursor.execute(UpdateSql, parm2)
                            else:
                                insertSql = "insert into B_GoodsAttribute(GoodsID,AttributeName) values(%s,%s)"
                                parm2 = (GoodsNid[0],b_goods_data['columnvalue'])
                                sqlcursor.execute(insertSql, parm2)
                        else:
                            result['errorcode'] = -1
                            result['errortext'] = 'SKU普元不存在'
                    else:
                        UpdateSql = "update b_goods set "+ b_goods_data['columnname'] +"=%s where SKU=%s"
                        parm2 = (b_goods_data['columnvalue'],b_goods_data['SKU'])
                        sqlcursor.execute(UpdateSql,parm2)

                    UpdateSql = ""
                    value = b_goods_data['columnvalue']
                    if  b_goods_data['columnname'] == "CostPrice":
                        UpdateSql = "update b_goodssku set " + b_goods_data['columnname'] + "=%s,ChangeCostTime=getdate() where SKU=%s"
                    elif b_goods_data['columnname'] == "Weight":
                        UpdateSql = "update b_goodssku set " + b_goods_data['columnname'] + "=%s where SKU=%s"
                    elif b_goods_data['columnname'] == "GoodsName" :
                        UpdateSql = "update b_goodssku set SKUName=%s where SKU=%s"
                    elif b_goods_data['columnname'] == "GoodsStatus" :
                        if b_goods_data['columnvalue'] == u"在售":
                            value = u"正常"
                        UpdateSql = "update b_goodssku set GoodsSKUStatus=%s,ChangeStatusTime=getdate() where SKU=%s"
                    if UpdateSql != "":
                        parm2 = (value, b_goods_data['SKU'])
                        sqlcursor.execute(UpdateSql, parm2)
                except Exception, ex:
                    result['errorcode'] = -1
                    result['errortext'] = 'Exception = %s ex=%s;  __LINE__=%s,%s,%s,%s' % (Exception, ex, sys._getframe().f_lineno,b_goods_data['SKU'],b_goods_data['columnname'],b_goods_data['columnvalue'])
            else:
                result['errorcode'] = -1
                result['errortext'] = '入参data为空'
                break
        if result['errorcode'] == -1:
            sqlserverInfo['py_conn'].rollback()
        else:
            sqlserverInfo['py_conn'].commit()
            #online 系统修改
            hqdb_cursor = pydb_connect.cursor()
            for b_goods_data in b_goods_data_list:
                if len(b_goods_data) > 0:
                    try:
                        UpdateSql == ""
                        # 成本价修改后记录，后期财务查看
                        if b_goods_data['columnname'] == "CostPrice":
                            selectSql = "select CostPrice,SupplierID from py_db.b_goods where SKU='%s'"%(b_goods_data['SKU'])
                            hqdb_cursor.execute(selectSql)
                            costprice = hqdb_cursor.fetchone()
                            costprice,supplierID = (costprice[0],costprice[1]) if costprice else (0,'')
                            insertCostPrice = "insert into b_costprice_modify(SKU,oriPrice,curPrice,applyMan,supplierID,modifyTime,remark) values(%s,%s,%s,%s,%s,%s,%s)"
                            parm1 = (b_goods_data['SKU'],costprice,b_goods_data['columnvalue'],b_goods_data['apply_name'],supplierID,datetime.now(),b_goods_data['describe'])
                            hqdb_cursor.execute(insertCostPrice, parm1)
                        if b_goods_data['columnname'] == "WarningCats": #采购等级修改
                            UpdateSql = "update py_db.kc_currentstock set "+ b_goods_data['columnname'] +"='%s' where " \
                                        "GoodsID = (select nid from py_db.b_goods where SKU='%s' limit 1) and " \
                                        "storeID = (select storeID from py_db.b_goods where SKU='%s' limit 1)"\
                                        %(b_goods_data['columnvalue'], b_goods_data['SKU'],b_goods_data['SKU'])
                            hqdb_cursor.execute(UpdateSql)
                        elif b_goods_data['columnname'] == "SupplierName":  # 供应商修改
                            strSelectSql = "select NID from B_Supplier where SupplierName='%s'" % (b_goods_data['columnvalue'])
                            sqlcursor.execute(strSelectSql)
                            supplierID = sqlcursor.fetchone()
                            UpdateSql = ""
                            if supplierID:
                                strSelectSql = "select top 1 possessMan2 from b_goods where SupplierID=%s and possessMan2 != '' and possessMan2 is not null and GoodsStatus != '停售'"
                                sqlcursor.execute(strSelectSql,supplierID[0])
                                possessMan2 = sqlcursor.fetchone()
                                strPossessMan2 = ""
                                if possessMan2:
                                    strPossessMan2 = possessMan2[0] if possessMan2 else ""
                                UpdateSql = "update py_db.b_goods set SupplierID=%s,possessMan2=%s where SKU=%s"
                                parm2 = (supplierID[0],strPossessMan2, b_goods_data['SKU'])
                                hqdb_cursor.execute(UpdateSql, parm2)
                        elif b_goods_data['columnname'] == "GoodsStatus":
                            use = 1 if b_goods_data['columnvalue'] == u"停售" else 0
                            UpdateSql = "update py_db.b_goods set " + b_goods_data['columnname'] + "=%s,Used=%s where SKU=%s"
                            parm2 = (b_goods_data['columnvalue'], use, b_goods_data['SKU'])
                            hqdb_cursor.execute(UpdateSql, parm2)
                        else:
                            UpdateSql = "update py_db.b_goods set "+ b_goods_data['columnname'] + "=%s where SKU=%s"
                            parm2 = (b_goods_data['columnvalue'], b_goods_data['SKU'])
                            hqdb_cursor.execute(UpdateSql, parm2)

                        UpdateSql = ""
                        value = b_goods_data['columnvalue']
                        if b_goods_data['columnname'] == "CostPrice":
                            UpdateSql = "update py_db.b_goodssku set " + b_goods_data['columnname'] + "=%s,ChangeCostTime=now() where SKU=%s"
                        elif b_goods_data['columnname'] == "Weight":
                            UpdateSql = "update py_db.b_goodssku set " + b_goods_data['columnname'] + "=%s where SKU=%s"
                        elif b_goods_data['columnname'] == "GoodsName":
                            UpdateSql = "update py_db.b_goodssku set SKUName=%s where SKU=%s"
                        elif b_goods_data['columnname'] == "GoodsStatus":
                            if b_goods_data['columnvalue'] == u"在售":
                                value = u"正常"
                            UpdateSql = "update py_db.b_goodssku set GoodsSKUStatus=%s,ChangeStatusTime=now() where SKU=%s"
                        if UpdateSql != "":
                            parm2 = (value, b_goods_data['SKU'])
                            hqdb_cursor.execute(UpdateSql, parm2)
                        hqdb_cursor.execute("commit")

                    except Exception, ex:
                        result['errorcode'] = -1
                        result['errortext'] = 'Exception = %s ex=%s;__LINE__=%s,%s,%s,%s' % (Exception, ex, sys._getframe().f_lineno,b_goods_data['SKU'],b_goods_data['columnname'],b_goods_data['columnvalue'])
                        break
                else:
                    result['errorcode'] = -1
                    result['errortext'] = '入参data为空'
                    break
            hqdb_cursor.close()
        #sqlcursor.close()
        return result


    def syn_supplier_info(self, supplier_info):
        """同步供应商信息"""
        try:
            from brick.pydata.py_syn.py_conn import py_conn
            pyconn_obj = py_conn()
            conn_result = pyconn_obj.py_conn_database()
            sqlserver_cursor = conn_result['py_cursor']

            select_sql = 'select count(1) from B_Supplier WHERE SupplierName=%s'
            sqlserver_cursor.execute(select_sql, (supplier_info['SupplierName'].strip(), ))
            count = sqlserver_cursor.fetchone()
            if count[0] > 0:
                result = {'error_code': -1, 'error_info': u'普源已有此供应商: "%s"' % supplier_info['SupplierName']}
            else:
                insert_sql = 'insert into B_Supplier(CategoryID, SupplierCode, SupplierName, FitCode, LinkMan, Address, ' \
                             'OfficePhone, Mobile, Used, Recorder, InputDate, Modifier, ModifyDate, Email, QQ, MSN, ' \
                             'ArrivalDays, URL, Memo, Account, CreateDate, SupPurchaser, supplierLoginId, paytype, SalerNameNew) ' \
                             'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)' \
                             'SELECT SCOPE_IDENTITY()'
                param = (
                    supplier_info['CategoryID'], supplier_info['SupplierCode'],
                    supplier_info['SupplierName'], supplier_info['FitCode'], supplier_info['LinkMan'],
                    supplier_info['Address'], supplier_info['OfficePhone'], supplier_info['Mobile'], supplier_info['Used'],
                    supplier_info['Recorder'], supplier_info['InputDate'], supplier_info['Modifier'],
                    supplier_info['ModifyDate'], supplier_info['Email'], supplier_info['QQ'], supplier_info['MSN'],
                    supplier_info['ArrivalDays'], supplier_info['URL'], supplier_info['Memo'], supplier_info['Account'],
                    supplier_info['CreateDate'], supplier_info['SupPurchaser'], supplier_info['supplierLoginId'],
                    supplier_info['paytype'], supplier_info['SalerNameNew']
                )
                sqlserver_cursor.execute(insert_sql, param)
                exe_result = sqlserver_cursor.fetchone()
                return_id = int(exe_result[0])
                conn_result['py_conn'].commit()
                result = {'error_code': 0, 'return_id': return_id}
            pyconn_obj.py_close_conn_database()
        except Exception, e:
            error_info = u'ex=%s; 供应商=%s; __LINE__=%s;' % (e, sys._getframe().f_lineno, supplier_info['SupplierName'])
            result = {'error_code': -1, 'error_info': error_info}
        return result

    def modify_py_purchaser(self, supplier_id, new_purchaser_id, category, modify_name, new_purchaser=None):
        """修改采购员"""
        from brick.pydata.py_syn.py_conn import py_conn
        pyconn_obj = py_conn()
        conn_result = pyconn_obj.py_conn_database()
        sqlserver_cursor = conn_result['py_cursor']

        clothing = ('0|1|', '0|2|', '0|170|', '0|174|', '0|174|175|', '0|176|', '0|176|177|', '0|176|178|', '0|176|180|', '0|176|183|')

        result = {'error_code': 0}
        if not new_purchaser:
            sql1 = 'select PersonName from B_Person WHERE NID=%s'
            sqlserver_cursor.execute(sql1, (new_purchaser_id, ))
            info1 = sqlserver_cursor.fetchone()
            if info1:
                new_purchaser = info1[0]
            else:
                result = {'error_code': -1, 'error_code': u'采购员ID: "%s"在普源不存在' % new_purchaser_id}

        if new_purchaser:
            if category == 0:
                sql2 = "update b_goods set Purchaser = \'%s\' WHERE SupplierID = %s AND GoodsStatus != '停售' AND CategoryCode in %s;" % (new_purchaser, supplier_id, str(clothing))
            else:
                sql2 = "update b_goods set Purchaser = \'%s\' WHERE SupplierID = %s AND GoodsStatus != '停售' AND CategoryCode not in %s;" % (new_purchaser, supplier_id, str(clothing))

            sqlserver_cursor.execute(sql2)

            sql3 = "update b_supplier set Suppurchaser=(select stuff((select '/'+ b.Purchaser from (select supplierid,purchaser from b_goods WHERE supplierid=%s and GoodsStatus != '停售' AND Purchaser != '' AND Purchaser is not null  group by supplierid, purchaser) b for xml path('') ),1,1,'')), Modifier=%s, ModifyDate=GETDATE() WHERE nid=%s;"
            sqlserver_cursor.execute(sql3, (supplier_id, modify_name, supplier_id))

            conn_result['py_conn'].commit()

        pyconn_obj.py_close_conn_database()
        return result


    def modify_py_supplier(self, supplier_info):
        """修改普源供应商信息"""
        try:
            from brick.pydata.py_syn.py_conn import py_conn
            pyconn_obj = py_conn()
            conn_result = pyconn_obj.py_conn_database()
            sqlserver_cursor = conn_result['py_cursor']

            sql = 'update b_supplier set ' + supplier_info['column_name'] +'=%s WHERE NID=%s; '
            sqlserver_cursor.execute(sql, (supplier_info['column_value'], supplier_info['nid']))
            conn_result['py_conn'].commit()
            pyconn_obj.py_close_conn_database()

            result = {'error_code': 0}
        except Exception, e:
            error_info = u'ex=%s; __LINE__=%s;' % (e, sys._getframe().f_lineno)
            result = {'error_code': -1, 'error_info': error_info}
        return result


    def modify_py_possessman2(self, possessman2_info):
        try:
            from brick.pydata.py_syn.py_conn import py_conn
            pyconn_obj = py_conn()
            conn_result = pyconn_obj.py_conn_database()
            sqlserver_cursor = conn_result['py_cursor']

            sql = "update b_goods set PossessMan2 = %s WHERE SupplierID = %s; "
            sqlserver_cursor.execute(sql, (possessman2_info['PossessMan2'], possessman2_info['nid']))
            conn_result['py_conn'].commit()
            pyconn_obj.py_close_conn_database()

            result = {'error_code': 0}
        except Exception, e:
            error_info = u'ex=%s; __LINE__=%s;' % (e, sys._getframe().f_lineno)
            result = {'error_code': -1, 'error_info': error_info}
        return result