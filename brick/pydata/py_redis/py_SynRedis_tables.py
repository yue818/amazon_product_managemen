# coding: utf-8
"""
@author: wangzy
@contact: 15205512335
@site:
@software: PyCharm
@file: py_SynRedis_pub.py
@time: 2018-01-25 15:21
"""
import copy
import datetime, time, calendar
import sys
from py_SynRedis_pub import py_SynRedis_pub,connRedis
import MySQLdb
import decimal
import array
import logging
from py_redis_log import py_redis_log
import ConfigParser
from django.db import  connection
import pymssql

DATABASES = {
	'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hq',
        'HOST': '192.168.105.111',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'root123'
    },
    'syn': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'py_db',
        'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
        'PORT': '3306',
        'USER': 'by15161458383',
        'PASSWORD': 'K120Esc1'
    },
    'default1': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hq_db',
        'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
        'PORT': '3306',
        'USER': 'by15161458383',
        'PASSWORD': 'K120Esc1'
    },
}


class py_SynRedis_tables():
    synPub = py_SynRedis_pub()
    tLog = py_redis_log()
    cf = ConfigParser.ConfigParser()
    cf.read("/data/djangostack-1.9.7/apps/django/django_projects/Project/brick/pydata/py_redis/py_Config.conf")
    db_conn = ''
    sqlcursor = ''
    db_conn_py = ''
    sqlcursor_py = ''

    def Recordlog(self,message,logLevel):
        strCurrentDate = time.strftime("%Y%m%d")
        logPath = self.cf.get("LOG", "log_path")
        fileHead = self.cf.get("LOG", "fileHead")
        strFileName = logPath + fileHead + strCurrentDate + '.log'
        '''
        logging.basicConfig(filename = strFileName,datefmt = '%Y-%m-%d %H:%M:%S',level=logLevel, filemode='a',format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
        #logger = logging.getLogger(__name__)
        logging.info(str(message))
        '''
        strTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        strInfo = "[" + strTime + "][" + str(__file__) + "," + str(logLevel) + "]:" + str(message) +"\n"
        with open(strFileName, 'a+') as f:
            f.write(strInfo)
        f.close()


    def getCurTimeOneYear(self, months):
        strTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        other = strTime[10:]
        dt = datetime.date(int(strTime[0:4]), int(strTime[5:7]), int(strTime[8:10]))
        month = dt.month - 1 + months
        year = dt.year + month / 12
        month = month % 12 + 1
        day = min(dt.day, calendar.monthrange(year, month)[1])
        newTime = str(dt.replace(year=year, month=month, day=day)) + other

        return newTime

    '''
    说明：获取b_goodssku 表数据
    入参：
    出参：元组 数据格式sku和nid
    where sku in ('HDR0128PK','HDR0128BL')
    '''
    def get_B_GoodsSKU_Data(self,allNid):

        self.connSql(111)
        strAllNid = "(" + (str(allNid))[1:-1] + ")"
        strTmp = strAllNid.replace('L','').replace('u','')
        #print(strAllNid)
        strSql ="select sku,nid from py_db.b_goodssku  where nid in" + str(strTmp)  # order by nid desc limit 100  where nid in ('430231','430232','430233')
        #print(strSql)
        n = self.sqlcursor.execute(strSql)
        sArray = self.sqlcursor.fetchall()
        self.WriteSKUToFile(sArray)

        self.closeSql(111)
        return sArray

    '''
    说明：采购未入库结果数据入redis
    参数：采购未入库计算结果集
    '''
    def syn_DataInRedis(self, InStockData):
        updateTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        list_UnInStore_agrs = [[2,3],['unStock_updateTime',updateTime]]
        if (self.synPub.setArrayArgsToHashRedis('', 1, InStockData,list_UnInStore_agrs)) == -1:
            return -1
        else:
             return 0

    '''
    说明：如果本地数据库连接，需要关闭数据库
    '''
    def connSql(self, flag=0):
        if flag == 111:
            # 个人测试库环境(192.168.105.111)
            '''
            self.db_conn = MySQLdb.Connect(DATABASES['default']['HOST'], DATABASES['default']['USER'],
                                      DATABASES['default']['PASSWORD'],
                                      DATABASES['syn']['NAME'], charset='utf8')
            self.sqlcursor = self.db_conn.cursor()
            '''
            # 正式环境
            self.db_conn = connection
            self.sqlcursor = self.db_conn.cursor()


        if flag == 10:
            # 个人测试库环境(192.168.105.111)
            # self.db_conn_py = MySQLdb.Connect(DATABASES['default']['HOST'], DATABASES['default']['USER'],DATABASES['default']['PASSWORD'],DATABASES['syn']['NAME'], charset='utf8')
            # 正式环境
            self.db_conn_py = pymssql.connect(host='122.226.216.10', user='fancyqube', password='K120Esc1',
                                              database='ShopElf', port='18793')
            self.sqlcursor_py = self.db_conn_py.cursor()


    '''
    说明：如果本地数据库连接，需要关闭数据库
    '''
    def closeSql(self,flag=0):
        if flag == 111:
            self.sqlcursor.close()
            self.db_conn.close()
        if flag == 10:
            self.db_conn_py.close()
            self.sqlcursor_py.close()

    '''
    说明：获取Redis的size
    '''
    def GetRedisSzie(self,patternName):
        return self.synPub.GteHashKeysCount(patternName)

    def Find_NID_SKU(self,sSKUArray,sNID):
        if len(sNID) == 0:
            return ''
        for row_sSKUArray in sSKUArray:
            if cmp(str(sNID),str(row_sSKUArray[1])) == 0:
                return row_sSKUArray[0]

        return ''

    def WriteSKUToFile(self,skuList):
        if len(skuList) == 0:
            return
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%Y%m%d%H%M%S", local_time)

        skuPath = self.cf.get("SKUDATA","sku_path")
        recordSplit = self.cf.get("SKUDATA", "recordSplit")
        fileHead = self.cf.get("SKUDATA", "fileHead")
        strCurrentDate = time.strftime("%Y%m%d")
        strFileName = skuPath + fileHead + strCurrentDate + '.dat'

        f = open(strFileName, 'a+')
        for obj in skuList:
            strINFO =str(data_head) + recordSplit + str(obj[0].encode('gb2312')) + recordSplit + str(obj[1])
            f.write(strINFO)
            f.write('\n')
        f.close()

    def ReadSKUFromFile(self,nIndex):
        if nIndex == 0:
            return [],0
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%Y%m%d%H%M%S", local_time)

        skuPath = self.cf.get("SKUDATA","sku_path")
        recordSplit = self.cf.get("SKUDATA", "recordSplit")
        fileHead = self.cf.get("SKUDATA", "fileHead")
        nPerReadRecord = int(self.cf.get("SKUDATA", "perReadRecord"))
        #strCurrentDate = time.strftime("%Y%m%d")
        strFileName = skuPath + fileHead + '.dat'
        #print('strFileName={}'.format(strFileName))

        i = 0
        nCount = 0
        strSKUID = ""
        gDicSKU={}
        with open(strFileName, 'r') as f:
            for line in f:
                i += 1
                nCount += 1
                if nCount == (nIndex + nPerReadRecord):
                    break
                if i >= nIndex:
                    # print line
                    if len(line.split(recordSplit)) == 3:
                        SKUID = line.split(recordSplit)[2].replace('\n', '')
                        SKUNAME = line.split(recordSplit)[1].replace('\n', '')
                        if len(SKUID) != 0:
                            strSKUID = strSKUID + SKUID + ","
                            gDicSKU[SKUID] = SKUNAME
        f.close()

        if nCount == (nIndex + nPerReadRecord):
            nIndex = nIndex + nPerReadRecord
        else:
            nIndex = -1
        #print(sArraySKUID)
        return strSKUID,gDicSKU,nIndex

    def WriteDiffResultToFile(self,sResult):
        if len(sResult) == 0:
            return
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%Y%m%d%H%M%S", local_time)

        diffDataPath = self.cf.get("DIFFDATA","diffdata_path")
        fileHead = self.cf.get("DIFFDATA", "fileHead")
        strCurrentDate = time.strftime("%Y%m%d")
        strFileName = diffDataPath + fileHead + strCurrentDate + '.dat'

        f = open(strFileName, 'a+')
        for obj in sResult:
            #print('obj={}'.format(obj))
            if int(obj[1]) != 19:
                continue
            f.write(str(data_head) + ":" + str(obj))
            f.write('\n')
        f.close()

    def CheckPyAndRedisDiff(self,strSKUID,gDicSKU):
        strNID = strSKUID[:-1]
        self.connSql(10)
        #sql server 环境执行
        strSql = "select d.GoodsSKUID,m.StoreID,SUM(case when (d.Amount - isnull(id.Number,0)) <= 0 then NULL else (d.Amount - isnull(id.Number,0)) end ) " + \
             "from CG_StockOrderD(nolock) d " +\
             "left join CG_StockOrderM(nolock) m on d.StockOrderNID = m.NID  " +\
             "left join (select om.NID as StockOrderID,m.StoreID as StoreID,d.GoodsSKUID as GoodsSKUID,sum(d.Amount) as Number  " +\
             "from CG_StockInD(nolock) d inner join CG_StockInM m on d.StockInNID = m.NID  " +\
             "inner  join (select  nid as StoreID,StoreName from B_store) st on st.StoreID = 19  " +\
             "left join CG_StockOrderM(nolock) om on m.StockOrder = om.BillNumber  " + \
             "where d.GoodsSKUID in("  + strNID +") and  m.CheckFlag = 1 and m.MakeDate > (GETDATE()-365) " +\
             "group by om.NID,d.GoodsSKUID,m.StoreID) id on d.StockOrderNID = id.StockOrderID and d.GoodsSKUID = id.GoodsSKUID and id.StoreID=19 " +\
             "where d.GoodsSkuID in (" + strNID +") and m.MakeDate > (GETDATE()-365) and (m.CheckFlag = 1) and (m.Archive = 0) group by d.GoodsSKUID,m.StoreID "
        '''
        strSql = "select d.GoodsSKUID,m.StoreID,CONVERT(SUM(case when (d.Amount - IFNULL(id.Number,0)) <= 0 then NULL else (d.Amount - IFNULL(id.Number,0)) end ),char) "+ \
                 "from CG_StockOrderD d " + \
                 "left join CG_StockOrderM m on d.StockOrderNID = m.NID " + \
                 "left join (select om.NID as StockOrderID,m.StoreID as StoreID,d.GoodsSKUID as GoodsSKUID,sum(d.Amount) as Number " + \
                 "from CG_StockInD d inner join CG_StockInM m on d.StockInNID = m.NID " + \
                 "left join CG_StockOrderM om on m.StockOrder = om.BillNumber  " + \
                 "where d.GoodsSKUID in("  + strNID +") and " +\
                 "m.CheckFlag = 1 and m.MakeDate > date_add('2018-02-13 09:52:33', interval -1 year) " + \
                 "group by om.NID,d.GoodsSKUID,m.StoreID) id on d.StockOrderNID = id.StockOrderID and d.GoodsSKUID = id.GoodsSKUID and id.StoreID=19 " + \
                 "where d.GoodsSkuID in (" + strNID +") and " +\
                 "m.MakeDate > date_add('2018-02-13 09:52:33', interval -1 year) and (m.CheckFlag = 1) and (m.Archive = 0) group by d.GoodsSKUID,m.StoreID"
        '''
        #print('strSql={}'.format(strSql))
        n = self.sqlcursor_py.execute(strSql)
        sResultArray = self.sqlcursor_py.fetchall()
        if cmp(str(sResultArray),'None') == 0:
            self.closeSql(10)
            return []
        #print('sResultArray={}'.format(sResultArray))
        sArrayDiffResult = []
        for sRow_sResultArray in sResultArray:
            sSKUID = sRow_sResultArray[0]
            sSKUName = gDicSKU.get(str(sSKUID))
            #print('sSKUName={},sSKUID={}'.format(sSKUName,sSKUID))
            sPYAmount = sRow_sResultArray[2]
            if cmp(str(sSKUName),'None') == 0:
                if float(sPYAmount) > 0.0:
                    sArrayDiffResult.append(sRow_sResultArray)
                    continue
                else:
                    continue
            if cmp(str(sPYAmount),'None') == 0:
                sPYAmount = 0.0
            sLocalAmount = self.synPub.getFromHashRedis("",sSKUName,"NotInStore")
            #print('sPYAmount={},sLocalAmount={}'.format(sPYAmount,sLocalAmount))
            if sLocalAmount == -1 or sLocalAmount == -2 or len(sLocalAmount) == 0:
                if float(sPYAmount) > 0.0:
                    sArrayDiffResult.append(sRow_sResultArray)
                    continue
                else:
                    continue
            #print('sLocalAmount = {}'.format(sLocalAmount))
            if (float(sPYAmount) - float(sLocalAmount)) != 0:
                sArrayDiffResult.append(sRow_sResultArray)

        #print('sArrayDiffResult={}'.format(sArrayDiffResult))
        self.closeSql(10)
        return sArrayDiffResult


    '''
    说明：采购未入库统计
    参数：list_SKU:sku列表格式   Dic_CG_StockOrderD_data：订单字典格式   Dic_CG_StockOrderM_data：订单明细字典格式  Dic_CG_StockInD_data：入库字典  Dic_CG_StockInM_data：入库明细字典
    
    '''
    def Syn_LoadUnStoreInfo(self,list_SKU,Dic_CG_StockOrderD_data,Dic_CG_StockOrderM_data,Dic_CG_StockInD_data,Dic_CG_StockInM_data):
        lastResultArray = []
        strOneYearAgo = self.getCurTimeOneYear(-12)
        preTime = time.time()
        sCurrentDate = self.tLog.write_redis_log('dealDataTime', '', 0)
        list_B_GoodsSKU = self.get_B_GoodsSKU_Data(list_SKU)
        if len(list_B_GoodsSKU) == 0:
            return 0
        for sRow_list_SKU in list_B_GoodsSKU:
            str_B_GoodsSKU_Name = sRow_list_SKU[0].encode('gb2312')
            self.Recordlog(str_B_GoodsSKU_Name + ',' + str(sRow_list_SKU[1]), sys._getframe().f_lineno)
            sList_CG_StockOrderD = Dic_CG_StockOrderD_data.get(str(sRow_list_SKU[1]))
            if len(sList_CG_StockOrderD) == 0:
                continue
            CG_StockOrderD_StockOrderNID = ''
            SkuOrderAmount = 0.0
            sArrayOrder = {}
            sArrayInStockOrder = {}
            #sArrayOrder_73 = {}
            #sArrayInStockOrder_73 = {}
            for sRow_CG_StockOrderD in sList_CG_StockOrderD:
                #print('sRow_CG_StockOrderD={}'.format(sRow_CG_StockOrderD))
                fAmount = sRow_CG_StockOrderD[1]
                CG_StockOrderD_StockOrderNID = sRow_CG_StockOrderD[2]  # G_StockOrderD :StockOrderNID
                sList_CG_StockOrderM = Dic_CG_StockOrderM_data.get(CG_StockOrderD_StockOrderNID)
                #print('sList_CG_StockOrderM={}'.format(sList_CG_StockOrderM))
                # CG_StockOrderM 获取对应的字段值 通过CG_StockOrderD订购StockOrderID在G_StockOrderM表只能获取一条记录(G_StockOrderM.NID = CG_StockOrderD.StockOrderID)
                if cmp(str(sList_CG_StockOrderM), 'None') == 0 or len(sList_CG_StockOrderM) == 0:
                    continue
                else:
                    CG_StockOrderM_StoreID = sList_CG_StockOrderM[1]
                    CG_StockOrderM_MakeDate = sList_CG_StockOrderM[2]
                    CG_StockOrderM_CheckFlag = sList_CG_StockOrderM[3]
                    CG_StockOrderM_Archice = sList_CG_StockOrderM[4]
                    CG_StockOrderM_BillNumber = sList_CG_StockOrderM[5]
                    #print('{},{},{},{},{}'.format(CG_StockOrderM_StoreID, CG_StockOrderM_MakeDate,CG_StockOrderM_CheckFlag, CG_StockOrderM_Archice,CG_StockOrderM_BillNumber))
                    # 删除过滤记录 MakeDate > DATE_SUB(now(), INTERVAL 1 YEAR) and  (CheckFlag = 1)  and (Archive = 0)
                    if int(CG_StockOrderM_StoreID) == 19 and cmp(str(CG_StockOrderM_MakeDate), strOneYearAgo) > 0 and int(CG_StockOrderM_CheckFlag) == 1 and int(CG_StockOrderM_Archice) == 0:
                        sArrayOrder[CG_StockOrderM_BillNumber] = fAmount
                    '''
                 #其他店铺 比如统计73
                    else:
                        if int(CG_StockOrderM_StoreID) == 73 and cmp(str(CG_StockOrderM_MakeDate), strOneYearAgo) > 0 and int(CG_StockOrderM_CheckFlag) == 1 and int(CG_StockOrderM_Archice) == 0:
                        sArrayOrder_73[CG_StockOrderM_BillNumber] = fAmount
                 '''
            #print('sArrayOrder={}'.format(sArrayOrder))
            #CG_StockInD  CD_StockInM
            sList_CG_StockInD = Dic_CG_StockInD_data.get(str(sRow_list_SKU[1]))
            CG_StockInD_StockInNID = ''
            SkuINMAmount = 0.0
            for sRow_CG_StockInD in sList_CG_StockInD:
                #print('sRow_CG_StockInD={}'.format(sRow_CG_StockInD))
                CG_StockInD_StockInNID = sRow_CG_StockInD[1]  # G_StockOrderD :StockOrderNID
                fAmount = sRow_CG_StockInD[2]

                sList_CG_StockInM = Dic_CG_StockInM_data.get(CG_StockInD_StockInNID)
                #print('sList_CG_StockInM={}'.format(sList_CG_StockInM))
                # CG_StockOrderM 获取对应的字段值 通过CG_StockOrderD订购StockOrderID在G_StockOrderM表只能获取一条记录(G_StockOrderM.NID = CG_StockOrderD.StockOrderID)
                if cmp(str(sList_CG_StockInM), 'None') == 0 or len(sList_CG_StockInM) == 0:
                    continue
                else:
                    CG_StockInM_StockID = sList_CG_StockInM[1]
                    CG_StockInM_MakeDate = sList_CG_StockInM[2]
                    CG_StockInM_CheckFlag = sList_CG_StockInM[3]
                    CG_StockInM_StockOrder = sList_CG_StockInM[4]
                    #print('CG_StockInM_StockOrder={}'.format(CG_StockInM_StockOrder))
                    if len(str(CG_StockInM_StockOrder).replace(' ','')) == 0:
                        continue
                    #print('test3 {},{},{},{}'.format( CG_StockInM_StockID,CG_StockInM_MakeDate, CG_StockInM_CheckFlag,CG_StockInM_StockOrder))
                    # 删除过滤记录  m.CheckFlag = 1 and m.MakeDate > DATE_SUB(now(), INTERVAL 1 YEAR) and m.StoreID = 19
                    if int(CG_StockInM_StockID) == 19 and cmp(str(CG_StockInM_MakeDate), strOneYearAgo) > 0 and int(CG_StockInM_CheckFlag) == 1 :
                        sTmp = sArrayInStockOrder.get(CG_StockInM_StockOrder)
                        if cmp(str(sTmp),'None') == 0:
                            sArrayInStockOrder[CG_StockInM_StockOrder] = fAmount
                        else:
                            sTmpAmount = float(fAmount) + float(sTmp)
                            sArrayInStockOrder[CG_StockInM_StockOrder] = sTmpAmount
                    '''
                 #其他店铺 比如统计73
                        else:
                            if int(CG_StockInM_StockID) == 73 and cmp(str(CG_StockInM_MakeDate), strOneYearAgo) > 0 and int(CG_StockInM_CheckFlag) == 1 :
                                sTmp = sArrayInStockOrder.get(CG_StockInM_StockOrder)
                                if cmp(str(sTmp),'None') == 0:
                                    sArrayInStockOrder_73[CG_StockInM_StockOrder] = fAmount
                                else:
                                    sTmpAmount = float(fAmount) + float(sTmp)
                                    sArrayInStockOrder_73[CG_StockInM_StockOrder] = sTmpAmount
                 '''
            #print('sArrayInStockOrder={}'.format(sArrayInStockOrder))
            #其他店铺统计将代码下面代码拷贝一份即可
            SkuUnStockAmount = 0.0
            for sRow_sArrayOrder in sArrayOrder:
                fOrderAmount = sArrayOrder.get(sRow_sArrayOrder)
                fInStockAmount = sArrayInStockOrder.get(sRow_sArrayOrder)
                #print(fInStockAmount)
                if cmp(str(fInStockAmount),'None') == 0:
                    fInStockAmount = '0.0'
                fUnStoreAmount = float(fOrderAmount)-float(fInStockAmount)
                if fUnStoreAmount < 0.0:
                    fUnStoreAmount = 0.0
                SkuUnStockAmount += fUnStoreAmount
                #print('{}:{}-{}:{}'.format(sRow_sArrayOrder,fOrderAmount,fInStockAmount,fUnStoreAmount))
            if SkuUnStockAmount < 0:
                SkuUnStockAmount = 0.0
            tmpArray1_1 = []
            tmpArray1_1.append(sRow_list_SKU[0])
            #tmpArray1_1.append('19')
            tmpArray1_1.append('NotInStore')
            tmpArray1_1.append(SkuUnStockAmount)
            lastResultArray.append(copy.deepcopy(tmpArray1_1))
            del tmpArray1_1[:]
        #print('lastResultArray={}'.format(lastResultArray))

        #数据写入redis
        if len(lastResultArray) != 0:
            self.syn_DataInRedis(lastResultArray)
            self.Recordlog(lastResultArray, sys._getframe().f_lineno)

        self.tLog.write_redis_log('dealDataTime', sCurrentDate, len(lastResultArray))
        dealTime = time.time()
        strInfo = 'Deal Success and UsedTime:{}'.format(dealTime - preTime)
        self.Recordlog(strInfo, sys._getframe().f_lineno)
        return 1

    '''
        说明：获取b_goodssku 表数据
        入参：
        出参：元组 数据格式sku和nid
        where sku in ('HDR0128PK','HDR0128BL')
        '''

    def get_B_GoodsSKU_Nid(self, sSKU):
        strSql = "select nid,sku from py_db.b_goodssku  where sku in(" + sSKU + ")"
        n = self.sqlcursor.execute(strSql)
        sArray = self.sqlcursor.fetchall()
        return sArray

    '''
    说明：
    '''
    def UpdateSkuUnstock(self,strSKUID):
        sUppleNID = self.get_B_GoodsSKU_Nid(strSKUID)
        strNID = ","
        gGoodSKU = {}
        for sRow in sUppleNID:
            strNID = strNID + str(sRow[0]).replace('L','') + ","
            gGoodSKU[sRow[0]] = sRow[1]
        strNID = strNID[1:-1]
        sSqlArray = []
        sResultArray = []
		
        if len(strNID) > 0:
            # sql server 环境执行
            strSql = "select d.GoodsSKUID,m.StoreID,Convert(NUMERIC(18,0),SUM(case when (d.Amount - isnull(id.Number,0)) <= 0 then NULL else (d.Amount - isnull(id.Number,0)) end )) " + \
                 "from CG_StockOrderD(nolock) d " +\
                 "left join CG_StockOrderM(nolock) m on d.StockOrderNID = m.NID  " +\
                 "left join (select om.NID as StockOrderID,m.StoreID as StoreID,d.GoodsSKUID as GoodsSKUID,sum(d.Amount) as Number  " +\
                 "from CG_StockInD(nolock) d inner join CG_StockInM m on d.StockInNID = m.NID  " +\
                 "inner  join (select  nid as StoreID,StoreName from B_store) st on st.StoreID = 19  " +\
                 "left join CG_StockOrderM(nolock) om on m.StockOrder = om.BillNumber  " + \
                 "where d.GoodsSKUID in("  + strNID +") and  m.CheckFlag = 1 and m.MakeDate > (GETDATE()-365) " +\
                 "group by om.NID,d.GoodsSKUID,m.StoreID) id on d.StockOrderNID = id.StockOrderID and d.GoodsSKUID = id.GoodsSKUID and id.StoreID=m.StoreID " +\
                 "where d.GoodsSkuID in (" + strNID +") and m.MakeDate > (GETDATE()-365) and (m.CheckFlag = 1) and (m.Archive = 0) group by d.GoodsSKUID,m.StoreID "
            '''
            strSql = "select d.GoodsSKUID,m.StoreID,CONVERT(SUM(case when (d.Amount - IFNULL(id.Number,0)) <= 0 then NULL else (d.Amount - IFNULL(id.Number,0)) end ),char) " + \
                     "from CG_StockOrderD d " + \
                     "left join CG_StockOrderM m on d.StockOrderNID = m.NID " + \
                     "left join (select om.NID as StockOrderID,m.StoreID as StoreID,d.GoodsSKUID as GoodsSKUID,sum(d.Amount) as Number " + \
                     "from CG_StockInD d inner join CG_StockInM m on d.StockInNID = m.NID " + \
                     "inner  join (select  nid as StoreID,StoreName from b_store) st on st.StoreID = 19  " + \
                     "left join CG_StockOrderM om on m.StockOrder = om.BillNumber  " + \
                     "where d.GoodsSKUID in(" + strNID + ") and " + \
                     "m.CheckFlag = 1 and m.MakeDate > date_add('2018-02-13 09:52:33', interval -1 year) " + \
                     "group by om.NID,d.GoodsSKUID,m.StoreID) id on d.StockOrderNID = id.StockOrderID and d.GoodsSKUID = id.GoodsSKUID and id.StoreID=19 " + \
                     "where d.GoodsSkuID in (" + strNID + ") and " + \
                     "m.MakeDate > date_add('2018-02-13 09:52:33', interval -1 year) and (m.CheckFlag = 1) and (m.Archive = 0) group by d.GoodsSKUID,m.StoreID"
			'''

            #print('strSql={}'.format(strSql))
            n = self.sqlcursor_py.execute(strSql)
            sSqlArray = self.sqlcursor_py.fetchall()
            if cmp(str(sSqlArray), 'None') == 0:
                return []

            for sRow in sSqlArray:
                if sRow[1] == 19:
                    sSKUName = gGoodSKU.get(sRow[0])
                    sTmp = []
                    sTmp.append(sSKUName) #SKUName
                    sTmp.append(sRow[0]) #SKUID
                    sTmp.append(sRow[1]) #StoreID
                    sTmp.append(sRow[2]) #采购未入库数量
                    sResultArray.append(copy.deepcopy(sTmp))
                    del sTmp[:]
        return sResultArray

    def getStatusConfig(self):
        reload(sys)
        sys.setdefaultencoding('utf8')
        strSql = "select hq_GoodsStatus,statuscode from goodsstatus_compare"
        n = self.sqlcursor.execute(strSql)
        sArray = self.sqlcursor.fetchall()
        gDicCfg = {}
        for sRowArray in sArray:
            # print('sRowArray={}'.format(sRowArray[0]))
            gDicCfg[str(sRowArray[0])] = sRowArray[1]
        return gDicCfg

    def UpdateSkuInStoreAndStatus(self,unStockData):
        gDicCfg = self.getStatusConfig()
        gResult = {}
        if len(gDicCfg) == 0:
            return gResult
        sSKUID = ','
        sSKUName = ','
        gSKIdAndName = {}
        for sRow in unStockData:
            sSKUID = sSKUID + str(sRow[1]).replace('L','') + ","
            sSKUName = sSKUName + "'" + str(sRow[0]) + "',"
            gSKIdAndName[sRow[0]] = sRow[1]
        sSKUID = sSKUID[1:-1]
        sSKUName = sSKUName[1:-1]
        #strGoodsStatusSql = "select sku,goodsstatus from b_goods where sku in(" + sSKUName + ")"
        strGoodsStatusSql = "select sku,goodsstatus from b_goods(nolock) where sku in(" + sSKUName + ")"
        n = self.sqlcursor_py.execute(strGoodsStatusSql)
        sResultStatus = self.sqlcursor_py.fetchall()
        #print("sResultStatus={},strGoodsStatusSql={}".format(sResultStatus,strGoodsStatusSql))
        nTmpStatus = 0
        if len(sResultStatus) == 0 or cmp(str(sResultStatus),'None') == 0:
            nTmpStatus = -1
        #print('sResultStatus={}'.format(str(sResultStatus)))
        gResultStatus = {}
        for sRow in sResultStatus:
            gResultStatus[gSKIdAndName.get(sRow[0])] = gDicCfg.get(str(sRow[1]))

        #strGoodsInstockSql = "select GoodsSKUID,Number,ReservationNum,SellCount1,-1 from kc_currentstock  WHERE  StoreID=19 and GoodsSKUID in(" + str(sSKUID) +")"
        strGoodsInstockSql = "select GoodsSKUID,isnull(Number,0),isnull(ReservationNum,0),SellCount1,Convert(NUMERIC(18,4),CASE WHEN SellCount1 = 0 THEN -1 ELSE CEILING((Number - isnull(ReservationNum,0)) * 7/SellCount1) END) as canday from kc_currentstock(nolock)  WHERE  StoreID=19 and GoodsSKUID in(" + str(sSKUID) +")"
        #print('strGoodsInstockSql={}'.format(strGoodsInstockSql))
        n = self.sqlcursor_py.execute(strGoodsInstockSql)
        sResultInstock = self.sqlcursor_py.fetchall()
        #print('sResultInstock={}'.format(sResultInstock))
        if len(sResultInstock) == 0:
            sResultInstock = []
        for sRow in sResultInstock:
            sStatus  = gResultStatus.get(sRow[0])
            sTmp = []
            sTmp.append(sRow[0]) #商品SKUID
            sTmp.append(sRow[1])  # 库存量
            sTmp.append(sRow[2])  # 占用量
            sTmp.append(sRow[3])  # 7天销量
            sTmp.append(sRow[4])  # 可卖天数
            if nTmpStatus == -1 or cmp(str(sStatus),'None') == 0:
                sTmp.append(-1)  # 商品状态
            else:
                sTmp.append(sStatus)  # 商品状态
            gResult[sRow[0]] = copy.deepcopy(sTmp)
            del sTmp[:]
        return  gResult

    '''
    说明：  根据SKU刷新redis记录，并返回前端
            可用数量 = 库存 - 占用
            采购未入库
            可卖天数 = 可用数量/(sellcount1/7)
            状态：映射 1 2 3 4
    返回列表：[库存、占用、7天销量、可卖天数、采购未入库、状态、刷新时间]
    '''
    def UpdateSkuInfo(self,sListSku):
        sSku = ""
        preTime = time.time()
        for sRow in sListSku:
            sSku = sSku + "'" + sRow + "',"
        sSku = sSku[:-1]
        gResult = []
        self.connSql(10)
        self.connSql(111)
        updateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        #获取采购未入库  SKUName、SKUID、StoreID、采购未入库数量（列表存储）
        sUnStock = self.UpdateSkuUnstock(str(sSku))
        if len(sUnStock) > 0:
            #获取库存数量、商品状态   商品SKUID、库存量、占用量、7天销量、可卖天数、商品状态（字典存储）
            sResult = self.UpdateSkuInStoreAndStatus(sUnStock)
            with connRedis.pipeline(transaction=False) as p:
                for sRow in sUnStock:
                    sTmp = []
                    sTmp.append(sRow[0])
                    sSKUId =  sRow[1]
                    sOtherInfo = sResult.get(sSKUId)
                    if cmp(str(sRow[3]), 'None') == 0:
                        sTmp.append(0)  # 未入库数量
                    else:
                        sTmp.append(int(float(sRow[3])))  # 未入库数量
                    #p.hset(sRow[0], '19', sTmp[1])
                    p.hset(sRow[0], 'NotInStore', sTmp[1])
                    #p.hset(sRow[0], 'unStock_updateTime', updateTime)
                    p.hset(sRow[0], 'UpdateTime', updateTime)
                    if len(sOtherInfo) > 0:
                        p.hset(sRow[0], 'Number', int(sOtherInfo[1])) # 库存量
                        p.hset(sRow[0], 'ReservationNum', int(sOtherInfo[2])) # 占用量
                        p.hset(sRow[0], 'SellCount1', int(sOtherInfo[3]))# 7天销量
                        p.hset(sRow[0], 'CanSaleDay', int(sOtherInfo[4]))# 可卖天数
                        #p.hset(sRow[0], 'goodsstatus', sOtherInfo[5])
                        p.hset(sRow[0], 'GoodsStatus', sOtherInfo[5])
                        #p.hset(sRow[0], 'KC_updateTime', updateTime)
                        p.hset(sRow[0], 'UpdateTime', updateTime)

                        sTmp.append(int(sOtherInfo[1])) #库存
                        sTmp.append(int(sOtherInfo[2])) #占用
                        sTmp.append(int(sOtherInfo[3])) #7天销量
                        sTmp.append(int(sOtherInfo[4])) #可卖天数
                        sTmp.append(int(sOtherInfo[5]))  # 商品状态
                    sTmp.append(updateTime)
                    gResult.append(copy.deepcopy(sTmp))
                    del sTmp[:]
                p.execute()
        self.closeSql(10)
        self.closeSql(111)
        dealTime = time.time()
        strInfo = 'Deal Success and UsedTime:{}'.format(dealTime - preTime)
        #print('sResult={},strInfo={}'.format(gResult,strInfo))
        return  gResult

    def BatchReadRedis(self,gSKUNameAndKey):
        gSKUValue = {}
        gSKUAllValue = []
        strInfo = []
        with connRedis.pipeline(transaction=False) as p:
            for sRow in gSKUNameAndKey:
                sSku = sRow.get("SKU")
                sSkuKey = sRow.get("SKUKEY",[])
                for sRowKey in sSkuKey:
                    p.hget(sSku, sRowKey)
                sShopSku = sRow.get("ShopSKU")
                sShopSkuKey = sRow.get("ShopSKUKEY",[])
                for sRowShopKey in sShopSkuKey:
                    p.hget(sShopSku, sRowShopKey)
            strInfo = p.execute()
            #print(strInfo)

        i = 0
        for  sRow in gSKUNameAndKey:
            subSKU = {}
            subSKU['SKU'] = sRow.get("SKU")
            sSkuKey = sRow.get("SKUKEY",[])
            sTmp = []
            for sRowKey in sSkuKey:
                if len(strInfo) >= i:
                    sTmp.append(strInfo[i])
                else:
                    sTmp.append('None')
                i += 1
            subSKU['SKUKEY'] = copy.deepcopy(sTmp)
            del sTmp[:]

            subSKU['ShopSKU'] = sRow.get("ShopSKU")
            sShopSkuKey = sRow.get("ShopSKUKEY",[])
            for sRowShopKey in sShopSkuKey:
                if len(strInfo) >= i:
                    sTmp.append(strInfo[i])
                else:
                    sTmp.append('None')
                i += 1
            subSKU['ShopSKUKEY'] = copy.deepcopy(sTmp)
            del sTmp[:]

            gSKUAllValue.append(subSKU)
        #print(gSKUAllValue)
        return gSKUAllValue


    def readData_Redis_table(self, params):

        redis_value_list = []
        for param in params:
            sku         = param.get('SKU', '')
            skukeys      = param.get('SKUKEY', [])
            shopsku     = param.get('ShopSKU', '')
            shopskukeys  = param.get('ShopSKUKEY', [])

            result_sku = []
            for skukey in skukeys:
                result_sku.append(connRedis.hget(str(sku).split('*')[0], skukey))

            result_shopsku = []
            for shopskukey in shopskukeys:
                redis_result = connRedis.hget(shopsku, shopskukey)
                if not redis_result:
                    redis_result = connRedis.hget(shopsku, str(shopskukey).split('.')[-1])
                result_shopsku.append(redis_result)

            redis_value_list.append({'SKU': sku, 'SKUKEY': result_sku, 'ShopSKU': shopsku, 'ShopSKUKEY': result_shopsku})

        return  redis_value_list


'''
sArray1 = ('744943','317083')  #,'7315','421418','124623'
sArray2 = [['FBA-W7297CA-L','8547'],['FBA-W7297CA-M','9197'],['FBA-W7297CA-S','9200']]
sArray3 = {'744943':[('744943','76.0000','265624')],'317083':[('317083','10.0000','512815'),('317083','10.0000','532177'),('317083','10.0000','636458'),('317083','10.0000','695237')]}  # CG_StockOrderD :GoodsSkuId,Amount,stockorderId
sArray4 = {'484315':('484315','19','2017-08-25 14:12:53.000','1','0','CGD-2017-08-25-0667'),'695237':('6952379','19','2018-01-09 15:08:48.000','1','1','CGD-2018-01-09-1882'),'636458':('6364582','19','2017-12-08 14:26:35.000','1','0','CGD-2017-12-08-1139'),'532177':('5321770','19','2017-10-06 15:01:32.000','1','0','CGD-2017-10-06-0514'),'512815':('5128152','19','2017-09-16 13:35:53.000','1','0','CGD-2017-09-16-0569')}
sArray5 = {'744943':[('744943','265624','71.0000')],'317083':[('317083','501391','10.0000'),('317083','534677','10.0000'),('317083','621837','10.0000'),('317083','674442','10.0000')]}  # CG_StockOrderD :GoodsSkuId,Amount,stockorderId
sArray6 = {'265624':('265624','19','2017-12-13 14:16:55.000','1','0','CGD-2017-12-13-1214'),'674442':('674442','19','2018-01-11 12:41:49.000','1','CGD-2018-01-09-1882'),'621837':('621837','19','2017-12-11 12:20:15.000','1','CGD-2017-12-08-1139'),'534677':('534677','19','2017-10-16 16:24:45.000','1','CGD-2017-10-06-0514'),'501391':('501391','19','2017-09-17 16:06:49.000','1','CGD-2017-09-16-0569')}

#sArray7 = ['MU2111R','W1711BK-S','W1711BK-M','W1711BK-L','W1711BK-XL','HB0622BK','HB0622BL','PA0754GD1','PA0754GR1','PA0754PK1','HB-0245-BL','HB-0245-YW']
sArray8 = ['MU2111R','HB1413','TL0361BK','TL0361BL','TL0361OR','TL0361RD','HG0106BL','HG0106WT','HG0106GR']
sArray9 = [{'SKU':'MU2111R','SKUKEY':['19','Number','ReservationNum','SellCount1','CanSaleDay'],\
            'ShopSKU':'MU2111R','ShopSKUKEY':['ReservationNum','SellCount1','CanSaleDay']}, \
           {'SKU': 'MU2111R', 'SKUKEY': ['19', 'Number', 'ReservationNum', 'SellCount1', 'CanSaleDay'],\
            'ShopSKU': 'MU2111R', 'ShopSKUKEY': ['CanSaleDay']}]
bb = py_SynRedis_tables()
#bb.UpdateSkuInfo(sArray8)
bb.BatchReadRedis(sArray9)
#bb.Syn_LoadUnStoreInfo(sArray1,sArray3,sArray4,sArray5,sArray6)
'''

'''
bb = py_SynRedis_tables()
sArray1 = [430231, 430232, 430233]
sArray2 = ((), (), ())  # CG_StockOrderD :GoodsSkuId,Amount,stockorderId
sArray3 = ((430231, 3, 727658), (430232, 4, 727658), (430233, 3, 727658))
sArray4 = ((727658, 19, '2018-01-25 14:01:23', 1, 0, 'CGD-2018-01-25-1244'))
sArray5 = ((), (), ())
sArrayList = (1, 2, 3, 4, 5)  # 或者[1,2,3,4,5]
bb.Syn_LoadInStoreInfo(sArrayList)
bb.get_Web_Data(sArrayList)
'''
