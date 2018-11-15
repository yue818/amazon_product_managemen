# coding: utf-8
"""
@author: wangzy
@contact: 15205512335
@site:
@software: PyCharm
@file: py_Redis_diff.py
@time: 2018-02-24 15:21
"""

import sys
import subprocess
import time
import ConfigParser
from py_SynRedis_pub import py_SynRedis_pub,connRedis
import MySQLdb

DATABASES = {
	'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hq',
        'HOST': '192.168.105.111',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'root123'
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

from django.db import  connection
db_conn = connection
sqlcursor = db_conn.cursor()

class Batch_LoadAndImportData():
    synRedis = py_SynRedis_pub()
    def getStatusConfig(self):
        reload(sys)
        sys.setdefaultencoding('utf8')
        '''
        db_conn = MySQLdb.Connect(DATABASES['default']['HOST'], DATABASES['default']['USER'],
                                  DATABASES['default']['PASSWORD'],
                                  DATABASES['default']['NAME'], charset='utf8')
        sqlcursor = db_conn.cursor()
        '''
        strSql = "select hq_GoodsStatus,statuscode from goodsstatus_compare"
        n = sqlcursor.execute(strSql)
        sArray = sqlcursor.fetchall()
        gDicCfg = {}
        for sRowArray in sArray:
            # print('sRowArray={}'.format(sRowArray[0]))
            gDicCfg[str(sRowArray[0])] = sRowArray[1]
        #sqlcursor.close()
        #db_conn.close()
        return gDicCfg
    #
    def LoadAndImportData(self,bcpString):
        result_code = subprocess.call(bcpString, shell=True)

    def WriteToRedis(self,fileName,strSplit,nKeyIndex,keyName,nValueIndex,gDicCfg={}):
        #print('gDicCfg={}'.format(gDicCfg))
        nStatus = len(gDicCfg)
        with connRedis.pipeline(transaction=False) as p:
            with open(fileName) as fileobject:
                j = 0
                for line in fileobject:
                    updateTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                    image_list = line.strip(strSplit).split(strSplit)
                    nLen = len(image_list)
                    i = 0
                    for sName in keyName:
                        if nLen >= nValueIndex[i]:
                            #print('{},{},{},{}'.format(i, nValueIndex[i],sName,image_list))
                            if nStatus != 0:
                                nTmpStatus = gDicCfg.get(str(image_list[nValueIndex[i] - 1].replace('\n','')))
                                #print('nTmpStatus = {}'.format(nTmpStatus))
                                #self.synRedis.setToValuesHashRedis(image_list[nKeyIndex - 1], sName,nTmpStatus)
                                '''
                                strStatus = ""
                                if cmp(str(nTmpStatus),"None") == 0:
                                    strStatus = str(nTmpStatus)								
                                elif int(nTmpStatus) == 1:
                                    strStatus = str(nTmpStatus) + "-正常"
                                elif int(nTmpStatus) == 2:
                                    strStatus = str(nTmpStatus) + "-售完下架"
                                elif int(nTmpStatus) == 3:
                                    strStatus = str(nTmpStatus) + "-临时下架"
                                elif int(nTmpStatus) == 4:
                                    strStatus = str(nTmpStatus) + "-停售"
                                else:
                                    strStatus = str(nTmpStatus)
                                '''
                                p.hset(image_list[nKeyIndex - 1], sName, nTmpStatus)
                            else:
                                #self.synRedis.setToValuesHashRedis(image_list[nKeyIndex - 1], sName,image_list[nValueIndex[i] - 1])
                                p.hset(image_list[nKeyIndex - 1], sName,image_list[nValueIndex[i] - 1])
                            i += 1
                    p.hset(image_list[nKeyIndex - 1], "KC_updateTime",updateTime)
                    if j == 5000:
                        p.execute()
                        j = 0
                    j += 1
                p.execute()

    def SynShopSevenSales(self):
        reload(sys)
        sys.setdefaultencoding('utf8')
        '''
        db_conn = MySQLdb.Connect(DATABASES['default']['HOST'], DATABASES['default']['USER'],
                                  DATABASES['default']['PASSWORD'],
                                  DATABASES['default']['NAME'], charset='utf8')
        sqlcursor = db_conn.cursor()
        '''
        strSql = "select ShopSKU,sum(SalesVolume) from t_report_sales_daily where orderday between  DATE_ADD(SYSDATE(),INTERVAL -8 DAY)  " \
                 "and DATE_ADD(SYSDATE(),INTERVAL -1 DAY) GROUP BY ShopSKU "
        n = sqlcursor.execute(strSql)
        sArray = sqlcursor.fetchall()

        with connRedis.pipeline(transaction=False) as p:
            j = 0
            for sRowArray in sArray:
                updateTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                if sRowArray[0] == "":
                    continue
                #p.hset(str(sRowArray[0].encode('gb2312')), "sevensales", sRowArray[1])  #测试环境可以
                p.hset(sRowArray[0], "sevensales", sRowArray[1]) #正式环境
                p.hset(sRowArray[0], "sevensales_updateTime",updateTime)

                if j == 20000:
                    p.execute()
                    j = 0
                j += 1
                #print('{},sRowArray={},i={}'.format(str(sRowArray[0].encode('gb2312')),sRowArray[0],i))
            p.execute()

        sqlcursor.close()
        db_conn.close()
        return 0

    def synSKUStatusAndAmount(self):
        cf = ConfigParser.ConfigParser()
        cf.read("/data/djangostack-1.9.7/apps/django/django_projects/Project/brick/pydata/py_redis/py_Config.conf")
        InAndOutPATH = cf.get("InAndOut", "PATH")
        InAndOutIP = cf.get("InAndOut", "IP")
        InAndOutUSER = cf.get("InAndOut", "USER")
        InAndOutPASS = cf.get("InAndOut", "PASS")
        InAndOutPORT = cf.get("InAndOut", "PORT")
        InAndOutSPLIT = cf.get("InAndOut", "SPLIT")

        bcpOutString_goods="bcp 'select sku,goodsstatus from b_goods(nolock)' queryout " + InAndOutPATH +\
                           "b_goods.csv -t '"+InAndOutSPLIT+"' -c -U "+InAndOutUSER+" -P "+InAndOutPASS+" -S "+InAndOutIP+","+InAndOutPORT
        bcpOutString_CurrentStock="bcp 'select b.SKU,Convert(NUMERIC(18,0),isnull(a.Number,0))," \
                                  "Convert(NUMERIC(18,0),isnull(a.ReservationNum,0))," \
                                  "Convert(NUMERIC(18,0),isnull(a.SellCount1,0))," \
                                  "Convert(NUMERIC(18,0),CASE WHEN a.SellCount1 = 0 THEN -9999 ELSE CEILING((a.Number - isnull(a.ReservationNum,0)) * 7/a.SellCount1) END) as canday " \
                                  "from KC_CurrentStock(nolock) a, B_GoodsSKU(nolock) b WHERE a.GoodsSKUID = b.NID  and a.StoreID=19' queryout  " + InAndOutPATH +\
                                  "KC_CurrentStock.csv -t '"+InAndOutSPLIT+"' -c -U "+InAndOutUSER+" -P "+InAndOutPASS+" -S "+InAndOutIP+","+InAndOutPORT
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.LoadAndImportData(bcpOutString_goods)
        self.LoadAndImportData(bcpOutString_CurrentStock)

        gDicCfg = self.getStatusConfig()
        #文件内容:suk、status
        self.WriteToRedis(InAndOutPATH+'b_goods.csv',InAndOutSPLIT,1,['goodsstatus',],[2,],gDicCfg)
        #print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        #文件内容:SKU,Number,ReservationNum
        self.WriteToRedis(InAndOutPATH+'KC_CurrentStock.csv',InAndOutSPLIT,1,['Number','ReservationNum','SellCount1','CanSaleDay'],[2,3,4,5],{})
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        self.SynShopSevenSales()
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

#bb = Batch_LoadAndImportData()
#bb.synSKUStatusAndAmount()