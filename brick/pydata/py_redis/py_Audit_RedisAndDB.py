# coding: utf-8
"""
@author: wangzy
@contact: 15205512335
@site:
@software: PyCharm
@file: py_Redis_diff.py
@time: 2018-02-06 15:21
"""
import sys
import os
import datetime, time, calendar
import ConfigParser
from py_SynRedis_pub import py_SynRedis_pub
import MySQLdb
import subprocess
import commands
from django.db import  connection

DATABASES = {
	'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'py_db',
        'HOST': '192.168.105.111',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'root123'
    },
    'py': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hq_db',
        'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
        'PORT': '3306',
        'USER': 'by15161458383',
        'PASSWORD': 'K120Esc1'
    },
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hq_db',
        'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
        'PORT': '3306',
        'USER': 'by15161458383',
        'PASSWORD': 'K120Esc1'
    },
}

class py_Audit_RedisAndDB:
    def __init__(self):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read("py_Config.conf")
        self.py_syn = py_SynRedis_pub()
        #cf.read("/data/djangostack-1.9.7/apps/django/django_projects/Project/brick/pydata/py_redis/py_Config.conf")

    def getStatusConfig(self):
        reload(sys)
        sys.setdefaultencoding('utf8')
        db_conn = MySQLdb.Connect(DATABASES['mysql']['HOST'], DATABASES['mysql']['USER'],
                                  DATABASES['mysql']['PASSWORD'],
                                  DATABASES['mysql']['NAME'], charset='utf8')
        sqlcursor = db_conn.cursor()
        strSql = "select hq_GoodsStatus,statuscode from goodsstatus_compare"
        n = sqlcursor.execute(strSql)
        sArray = sqlcursor.fetchall()
        gDicCfg = {}
        print(sArray)
        for sRowArray in sArray:
            # print('sRowArray={}'.format(sRowArray[0]))
            gDicCfg[str(sRowArray[0])] = sRowArray[1]
        sqlcursor.close()
        db_conn.close()
        return gDicCfg

    '''
    写差异结果
    '''
    def WriteDiffData(self,fileFlag = 0,strInfo=''):
        pyPathFile = self.cf.get("DIFFDATA", "diffdata_path")
        allPathFile = ''
        #fileFlag == 0 写redis差异   fileFlag == 1 写mysql差异
        if fileFlag == 0:
            saveFileHead = self.cf.get("DIFFDATA", "fileHead_redis") + time.strftime('%Y-%m-%d', time.localtime(time.time()))
            allPathFile = pyPathFile + saveFileHead
        elif fileFlag == 1:
            saveFileHead = self.cf.get("DIFFDATA", "fileHead_mysql") + time.strftime('%Y-%m-%d', time.localtime(time.time()))
            allPathFile = pyPathFile + saveFileHead

        f = open(allPathFile,'a+')
        f.write(strInfo)
        f.write('\n')
        f.close()
    def LoadAndImportData(self,fileName,flag):
        #KC_CurrentStock_Audit.csv
        InAndOutPATH = self.cf.get("InAndOut", "PATH")
        allPathFile = InAndOutPATH + fileName
        InAndOutIP = self.cf.get("InAndOut", "IP")
        InAndOutUSER = self.cf.get("InAndOut", "USER")
        InAndOutPASS = self.cf.get("InAndOut", "PASS")
        InAndOutPORT = self.cf.get("InAndOut", "PORT")
        InAndOutSPLIT = self.cf.get("InAndOut", "SPLIT")
        if flag == 0:
            bcpOutString="bcp 'select sku,goodsstatus from b_goods(nolock)' queryout " + allPathFile +\
                               " -t '"+InAndOutSPLIT+"' -c -U "+InAndOutUSER+" -P "+InAndOutPASS+" -S "+InAndOutIP+","+InAndOutPORT
        elif flag == 1:
            bcpOutString="bcp 'select b.SKU,a.Number,a.ReservationNum from KC_CurrentStock(nolock) a, B_GoodsSKU(nolock) b WHERE a.GoodsSKUID = b.NID and a.StoreID=19' queryout  " + allPathFile +\
                                  " -t '"+InAndOutSPLIT+"' -c -U "+InAndOutUSER+" -P "+InAndOutPASS+" -S "+InAndOutIP+","+InAndOutPORT
        result_code = subprocess.call(bcpOutString, shell=True)

    '''
    普源导出文件与本地redis数据比较
    '''
    def py_Comp_FileAndRedis(self,fileName,nCol = 0):
        pyDownPathFile = self.cf.get("DIFFDATA", "diffdata_path")
        recordSplit = self.cf.get("DIFFDATA", "SPLIT")
        allPathFile = pyDownPathFile + fileName
        if int(nCol) == 2:
            self.LoadAndImportData(fileName, 0)
        elif int(nCol) == 3:
            self.LoadAndImportData(fileName, 1)
        if os.path.exists(allPathFile):
            gDicCfg = self.getStatusConfig()
            with open(allPathFile, 'r') as f:
                for line in f:
                    if int(nCol) == 2:

                        colList = line.strip(recordSplit).split(recordSplit)
                        if len(colList) >=2 :
                            TmpStatus_1 = gDicCfg.get(str(colList[1].replace('\n', '')))
                            TmpStatus_2 = self.py_syn.getFromHashRedis('',colList[0],'goodsstatus')
                            if cmp(str(TmpStatus_1),str(TmpStatus_2)) == 0 :
                                #print('{},{},{},{}'.format(TmpStatus_1,TmpStatus_2,str(colList[1].replace('\n', '')),TmpStatus_2))
                                continue
                            elif cmp(str(TmpStatus_1),'None') !=0 and int(TmpStatus_1) == int(TmpStatus_2):
                                continue
                            else:
                                self.WriteDiffData(0,'goodsstatus:'+ line)
                                #记录写入差异文件
                    elif int(nCol) == 3:
                        colList = line.strip(recordSplit).split(recordSplit)
                        if len(colList) >=3 :
                            TmpNumber_1 = colList[1]
                            if cmp(str(TmpNumber_1),'.0000') == 0:
                                TmpNumber_1 = '0'
                            TmpNumber_2 = self.py_syn.getFromHashRedis('',colList[0],'Number')
                            if cmp(str(TmpNumber_2),'.0000') == 0:
                                TmpNumber_2 = '0'
                            TmpReservationNum_1 = colList[2].replace('\n','')
                            if cmp(str(TmpReservationNum_1),'.0000') == 0:
                                TmpReservationNum_1 = '0'
                            TmpReservationNum_2 = str(self.py_syn.getFromHashRedis('', colList[0], 'ReservationNum')).replace('\n','')
                            if cmp(str(TmpReservationNum_2),'.0000') == 0:
                                TmpReservationNum_2 = '0'

                            #print('{},{},{},{}'.format(TmpNumber_1, TmpNumber_2, TmpReservationNum_1,TmpReservationNum_2))
                            #print('{},{},{},{}'.format(int(TmpNumber_1), int(TmpNumber_2), int(TmpReservationNum_1),int(TmpReservationNum_2)))
                            if cmp(str(TmpNumber_1),str(TmpNumber_2)) == 0 and cmp(str(TmpReservationNum_1),str(TmpReservationNum_2)) == 0:
                                #print('{},{},{},{}'.format(TmpStatus_1,TmpStatus_2,str(colList[1].replace('\n', '')),TmpStatus_2))
                                continue
                            else:
                                self.WriteDiffData(0, 'KC_CurrentStock:' + line)
    '''
    bcp获取普源数据和mysql数据
    '''
    def py_Comp_PyAndMysql(self,strTable,sKey):
        PATH = self.cf.get("InAndOut1", "PATH")
        strPyFile = PATH + strTable +"_PY.dat"
        strPy = "select " + sKey + " from " + strTable
        #print('{},{},{}'.format(strTable,sKey,strPyFile))			
        py_conn = connection		
        py_cursor = py_conn.cursor()
        py_cursor.execute(strPy)
        alldata1 = py_cursor.fetchall()
        with open(strPyFile, 'w') as f:
            for result in alldata1:
                f.write(str(result) + '\n')
        f.close()
        py_conn.close()
        py_cursor.close()

        strMysql = "select "+ sKey +" from " + strTable
        strMysqlFile = PATH + strTable + "_MYSQL.dat"
        #print('{},{},{}'.format(strTable,sKey,strMysqlFile))		
        db_conn = MySQLdb.Connect(DATABASES['mysql']['HOST'], DATABASES['mysql']['USER'],
                                     DATABASES['mysql']['PASSWORD'],
                                     DATABASES['mysql']['NAME'], charset='utf8')
        sqlcursor = db_conn.cursor()
        sqlcursor.execute(strMysql)
        alldata2 = sqlcursor.fetchall()
        with open(strMysqlFile, 'w') as f:
            for result in alldata2:
                f.write(str(result) + '\n')
        f.close()
        sqlcursor.close()
        db_conn.close()

        if os.access(strPyFile, os.F_OK) and os.access(strMysqlFile, os.F_OK):
            strPyShell = "cat " + strPyFile +"|sort|uniq>>" + strPyFile +".sort"
            commands.getstatusoutput(strPyShell)
            strMysqlShell = "cat " + strMysqlFile + "|sort|uniq>>" + strMysqlFile + ".sort"
            commands.getstatusoutput(strMysqlShell)

            strDiff = "diff " + strPyFile +".sort " + strMysqlFile + ".sort >"+PATH+"diffPyAndMysql.dat"
            commands.getstatusoutput(strDiff)
            commands.getstatusoutput("rm -f "+ strPyFile +".sort " + strMysqlFile + ".sort")


if __name__ == "__main__":
    print("{},{},{}".format(sys.argv[1],sys.argv[2],sys.argv[3]))
    if len(sys.argv) != 4:
        print("3 param;sample python py_Audit_RedisAndDB sflag=redis filename='b_goods.csv' nCol = 2 ")
        print("3 param;sample python py_Audit_RedisAndDB sflag=mysql tablename='b_goods' sKey = 'nid' ")
        exit(0)
    tt = py_Audit_RedisAndDB()
    preTime = time.time()
    if cmp(str(sys.argv[1]),"redis") ==0:
        tt.py_Comp_FileAndRedis(str(sys.argv[2]), sys.argv[3])
    elif cmp(str(sys.argv[1]),"mysql") ==0:
        tt.py_Comp_PyAndMysql(str(sys.argv[2]), str(sys.argv[3]))
    else:
        exit(0)
    dealTime = time.time()
    print('Deal Success and UsedTime:{}'.format(dealTime - preTime))