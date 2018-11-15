# coding:utf-8
"""
@author: ZhangYu
@contact: 292724306@qq.com
@site:
@software: PyCharm
@file: py_information_by_cg_stocklogs.py
@time: 2017-12-30 13:27
"""
import MySQLdb
import pymssql
import logging
import sys
#sys.path.append('/data/djangostack-1.9.7/apps/django/django_projects/Project')
from cg_StockOrderD import *
from cg_StockOrderM import *
from public import *
from brick.pydata.py_redis.py_SynRedis_tables import py_SynRedis_tables
from datetime import datetime


cf = ConfigParser.ConfigParser()
cf.read("/data/djangostack-1.9.7/apps/django/django_projects/Project/brick/pydata/py_syn/select.conf")
OrderNIDsNum = cf.getint('myconfig', 'OrderNIDsNum')
maxnumFetchone = cf.getint('myconfig', 'maxnumFetchone')
flag = cf.getint('myconfig', 'flag')
tt = py_SynRedis_tables()

'''获取当前时间-12月'''
my_time = tt.getCurTimeOneYear(-12)

'''
健壮性
增加一层判断  是否全量redis和log表增量
全量：全部获取skuid且不持久化
增量：获取新增的orderid且持久化
'''
if flag == 0:
    flag = ''

class py_information_by_cg_stocklogs():
    def __init__(self, db_conn, sqlserver_conn):
        self.db_conn = db_conn
        self.sqlserver_conn = sqlserver_conn
        self.public_obj = public(self.db_conn, self.sqlserver_conn)

    def CG_Recordlog(self, message, logLevel):
        strCurrentDate = time.strftime("%Y%m%d")
        my_strFileName = '/tmp/py_log/CG' + strCurrentDate + '.log'
        logging.basicConfig(filename=my_strFileName, datefmt='%Y-%m-%d %H:%M:%S', level=logLevel, filemode='a',
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # logger = logging.getLogger(__name__)
        logging.info(str(message))

    # 输入普源日志到本地  用于下次判断
    def setHqLog(self, MaxNID):
        cursor = self.db_conn.cursor()
        try:
            insertSql = "REPLACE INTO py_db.CG_StockLogs(NID) VALUES (%s)" % MaxNID
            # public_obj = public(self.db_conn)
            # public_obj.commitmanyFun(objs, insertSql)
            cursor.execute(insertSql)
            cursor.execute('commit')
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            self.db_conn.rollback()

    def setHqOP(self, SKUList):
        cursor = self.db_conn.cursor()
        SKUListTmp = []
        if SKUList:
            for SKU in SKUList:
                SKU = SKU + ',2'
                SKU = SKU.split(',')
                SKUListTmp.append(SKU)
            # for SKU in SKUList:
            insertSql = "REPLACE INTO t_product_puyuan_op (sku,status,Op_time) VALUES (%s,%s,'{0}')".format(datetime.now())
            cursor.executemany(insertSql, SKUListTmp)
            cursor.execute('commit')

    # 获取本地日志最大ID
    def getMaxNID(self):
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                NIDSql = "SELECT MAX(NID) from py_db.CG_StockLogs"
                cursor.execute(NIDSql)
                NIDTuple = cursor.fetchone()
                if NIDTuple:
                    NID = NIDTuple[0]
                    return NID
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])


    # 获取普源日志
    def getPyLog(self):
        objs = []
        MaxNID = ''
        NID = self.getMaxNID()
        if self.sqlserver_conn and NID:
            sqlcursor = self.sqlserver_conn.cursor()
            selectsql = "SELECT NID,OrderNID from CG_StockLogs(nolock) WHERE NID > %s  "
            MaxNIDsql = "SELECT MAX(NID) from CG_StockLogs(nolock) WHERE NID > %s  "
            try:
                sqlcursor.execute(selectsql, NID)
                public_obj = public()
                objs = public_obj.fetchmanyFun(sqlcursor)
                sqlcursor.execute(MaxNIDsql, NID)
                MaxNID = sqlcursor.fetchone()[0]
                if not MaxNID:
                    MaxNID = NID
                return objs, MaxNID
            except MySQLdb.Error, e:
                print "MySQLdb Error %d: %s" % (e.args[0], e.args[1])

    #五个列表转化成4个字典
    def listToDic(self,argv1, argv2, argv3, argv4, argv5):
        if str(argv1) != "[None]" and str(argv2) != "[None]" and str(argv3) != "[None]" and str(argv4) != "[None]" and str(argv5) != "[None]":
            # print "gArrayOrderD:"
            gArrayOrderD = {}
            for sRow in argv1:
                gArrayOrderD[str(sRow)] = []
            # print(gArrayOrderD)

            for sRow in argv2:
                sOrderD = gArrayOrderD.get(sRow[0])
                sOrderD.append(sRow)
            # print gArrayOrderD

            # print "gArrayOrderM:"
            gArrayOrderM = {}
            for sRow in argv2:
                gArrayOrderM[sRow[2]] = ()
            # print(gArrayOrderM)

            for sRow in argv3:
                gArrayOrderM[str(sRow[0])] = sRow
            # print gArrayOrderM

            # print "gArrayInD:"
            gArrayInD = {}
            for sRow in argv1:
                gArrayInD[str(sRow)] = []
            # print(gArrayInD)

            for sRow in argv4:
                sInD = gArrayInD.get(sRow[0])
                sInD.append(sRow)
            # print gArrayInD

            # print "gArrayInM:"
            gArrayInM = {}
            for sRow in argv4:
                gArrayInM[sRow[1]] = ()
            # print(gArrayInM)

            for sRow in argv5:
                gArrayInM[sRow[0]] = sRow
            # print gArrayInM

        return gArrayOrderD,gArrayOrderM,gArrayInD,gArrayInM

    def py_synchronization_by_cg_stocklogs(self):
        print "cg_stocklogs---program---Begin：{0}".format(datetime.now())
        self.CG_Recordlog("cg_stocklogs---program---Begin：{0}".format(datetime.now()), logging.INFO)
        cg_StockOrderD_obj = cg_StockOrderD(self.db_conn, self.sqlserver_conn)
        cg_StockOrderM_obj = cg_StockOrderM(self.db_conn, self.sqlserver_conn)
        i = 0
        x = 0
        objs=[]
        param = []
        Num = ''
        MaxNID = ''
        try:
            '''全量·增量的判断  决定从哪里取参数'''
            if flag:
                OrderNIDs = []
                objs,MaxNID = self.getPyLog()
                if objs:
                    for obj in objs:
                        OrderNIDs.append(obj[1])
                        i += 1
                    param = list(set(OrderNIDs))
                Num = OrderNIDsNum
            else:
                GoodsSKUID=[]
                mscursor = self.db_conn.cursor()
                GoodsSKUIDSql = "select NID from py_db.b_goodssku"
                mscursor.execute(GoodsSKUIDSql)
                GoodsSKUID_tmp = mscursor.fetchall()
                for GoodsSKUID_tmp_tmp in GoodsSKUID_tmp:
                        GoodsSKUID.append(GoodsSKUID_tmp_tmp[0])
                param = list(set(GoodsSKUID))
                print "param:{0}".format(len(param))
                Num = maxnumFetchone
            print len(param)
            while True:
                if len(param)>Num:
                    param_Tmp = param[:Num]
                    SKUList, cg_StockOrderD_objs, cg_StockInD_objs, cg_StockInM_objs, GoodsSKUIDs, StockOrderNID = \
                        cg_StockOrderD_obj.update_cg_StockOrderD(param_Tmp,flag,my_time)
                    cg_StockOrderM_obj_objs = cg_StockOrderM_obj.update_cg_StockOrderM(StockOrderNID,flag,my_time)
                    x += 1
                    # print "{},{},{},{},{}".format(GoodsSKUIDs, cg_StockOrderD_objs,cg_StockOrderM_obj_objs,cg_StockInD_objs, cg_StockInM_objs)
                    gArrayOrderD, gArrayOrderM, gArrayInD, gArrayInM = self.listToDic(GoodsSKUIDs, cg_StockOrderD_objs,cg_StockOrderM_obj_objs,cg_StockInD_objs, cg_StockInM_objs)
                    print "param---{0}---{1}".format(x, datetime.now())
                    self.CG_Recordlog("param---{0}---{1}".format(x, datetime.now()), logging.INFO)
                    self.CG_Recordlog("GoodsSKUIDs:{0},cg_StockOrderD:{1},cg_StockOrderM:{2},cg_StockInD:{3},"
                                   "cg_StockInM:{4}".format(len(GoodsSKUIDs), len(cg_StockOrderD_objs),
                                                            len(cg_StockOrderM_obj_objs), len(cg_StockInD_objs),
                                                            len(cg_StockInM_objs)), logging.INFO)
                    print "Begin---redis"
                    tt.Syn_LoadUnStoreInfo(GoodsSKUIDs, gArrayOrderD, gArrayOrderM, gArrayInD, gArrayInM)
                    print "End---redis"
                    if SKUList:
                        self.setHqOP(SKUList)
                    param = param[Num:]
                if len(param)<=Num and len(param)!=0:
                    SKUList, cg_StockOrderD_objs, cg_StockInD_objs, cg_StockInM_objs, GoodsSKUIDs, StockOrderNID = \
                        cg_StockOrderD_obj.update_cg_StockOrderD(param,flag,my_time)
                    cg_StockOrderM_obj_objs = cg_StockOrderM_obj.update_cg_StockOrderM(StockOrderNID,flag,my_time)
                    x += 1
                    # print "{},{},{},{},{}".format(GoodsSKUIDs, cg_StockOrderD_objs,
                    #                               cg_StockOrderM_obj_objs,
                    #                               cg_StockInD_objs, cg_StockInM_objs)
                    gArrayOrderD, gArrayOrderM, gArrayInD, gArrayInM = self.listToDic(GoodsSKUIDs, cg_StockOrderD_objs,
                                                                                 cg_StockOrderM_obj_objs,
                                                                                 cg_StockInD_objs, cg_StockInM_objs)
                    # print gArrayOrderD
                    # print gArrayOrderM
                    # print gArrayInD
                    # print gArrayInM
                    print "param---{0}---{1}".format(x, datetime.now())
                    self.CG_Recordlog("param---{0}---{1}".format(x, datetime.now()), logging.INFO)
                    self.CG_Recordlog("GoodsSKUIDs:{0},cg_StockOrderD:{1},cg_StockOrderM:{2},cg_StockInD:{3},"
                                   "cg_StockInM:{4}".format(len(GoodsSKUIDs), len(cg_StockOrderD_objs),
                                                            len(cg_StockOrderM_obj_objs), len(cg_StockInD_objs),
                                                            len(cg_StockInM_objs)), logging.INFO)
                    print "Begin---redis"
                    tt.Syn_LoadUnStoreInfo(GoodsSKUIDs, gArrayOrderD, gArrayOrderM, gArrayInD, gArrayInM)
                    print "End---redis"
                    if SKUList:
                        self.setHqOP(SKUList)
                    break
                if len(param)==0:
                    print "no data"
                    break
        except MySQLdb.Error, e:
            self.public_obj.setStatus("py_synchronization_by_cg_stocklogs", 3)
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            self.db_conn.rollback()
            print "cg_stocklogs---Failed{0}".format(datetime.now())
            self.CG_Recordlog("cg_stocklogs---Failed{0}".format(datetime.now()), logging.ERROR)
        else:
            self.setHqLog(MaxNID)
            self.public_obj.setStatus("py_synchronization_by_cg_stocklogs", 1)
            print "END program：{0}".format(datetime.now())
            self.CG_Recordlog("END program：{0}".format(datetime.now()), logging.INFO)
        finally:
            self.db_conn.close()
            self.sqlserver_conn.close()
