# encoding: utf-8
"""
@author: ZhangYu
@contact: 292724306@qq.com
@site:
@software: PyCharm
@file: cg_StockOrderD.py
@time: 2017-12-19 19:16
"""

import time
import MySQLdb
import pymssql
from cg_StockInD import *
from public import *
import ConfigParser
import sys
#sys.path.append('/data/djangostack-1.9.7/apps/django/django_projects/Project')
from brick.pydata.py_redis.py_SynRedis_tables import py_redis_log
tLog = py_redis_log()
cf = ConfigParser.ConfigParser()
cf.read("/data/djangostack-1.9.7/apps/django/django_projects/Project/brick/pydata/py_syn/select.conf")
maxnumFetchone = cf.getint('myconfig', 'maxnumFetchone')
class cg_StockOrderD:
    def __init__(self, db_conn, sqlserver_conn):
        self.db_conn = db_conn
        self.sqlserver_conn = sqlserver_conn
        self.cursor = self.db_conn.cursor()

    def getMaxNID(self):
        NID = ''
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                NIDSql = "SELECT MAX(NID) from py_db.cg_stockorderd"
                cursor.execute(NIDSql)
                NIDTuple = cursor.fetchone()
                if NIDTuple:
                    NID = NIDTuple[0]
                    return NID
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def getPyInfo(self, param1,flag):
        objs = []
        StockOrderNID = []
        i = 0
        sql = ''
        GoodsSKUID = []
        Max_NID = ''
        param = param1
        try:
            if self.sqlserver_conn:
                sqlcursor = self.sqlserver_conn.cursor()
                if flag:
                    GoodsSKUID = []
                    while 'All' in param:
                        param.remove('All')
                    x = ','.join(['%s'] * len(param))
                    GoodsSKUIDSql = "select GoodsSKUID from CG_StockOrderD where StockOrderNID in (%s)" % x
                    sqlcursor.execute(GoodsSKUIDSql,tuple(param))
                    GoodsSKUID_tmp = sqlcursor.fetchall()
                    for GoodsSKUID_tmp_tmp in GoodsSKUID_tmp:
                        GoodsSKUID.append(GoodsSKUID_tmp_tmp[0])
                    GoodsSKUID = list(set(GoodsSKUID))
                    param = GoodsSKUID
                    # param = [154455,32644,395247,4051,59225]
                    # param = [306138]

                    param1 = param
                    # NID = self.getMaxNID()
                    # NID = 2365751
                    # if NID:
                    #     sql = "select replace(GoodsSKUID,' ',''),replace(cast(Amount AS VARCHAR ),' ',''),replace(StockOrderNID,' ','') from CG_StockOrderD(nolock) where NID > {}".format(
                    #         NID)
                    #     sqlcursor.execute(sql)
                    #     objs = sqlcursor.fetchall()
                    #     for obj in objs:
                    #         GoodsSKUID.append(obj[1])
                    #         StockOrderNID.append(obj[2])
                    #     param = GoodsSKUID
                sql = "select replace(GoodsSKUID,' ',''),replace(cast(Amount AS VARCHAR ),' ',''),replace(StockOrderNID,' ','') from CG_StockOrderD(nolock) where GoodsSKUID in (%s)"
                while True:
                    if len(param) > maxnumFetchone:
                        param_tmp = param[:maxnumFetchone]
                        param = param[maxnumFetchone:]
                        x = ','.join(['%s'] * len(param_tmp))
                        try:
                            selectsql = sql % x
                            sqlcursor.execute(selectsql, tuple(param_tmp))
                            obj = sqlcursor.fetchall()
                            i += 1
                            for obj_tmp in obj:
                                objs.append(obj_tmp)
                                if obj_tmp[2] != '' and obj_tmp[2] is not None:
                                    StockOrderNID.append(obj_tmp[2])
                            print i
                        except MySQLdb.Error, e:
                            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                            break
                    if len(param) <= maxnumFetchone:
                        x = ','.join(['%s'] * len(param))
                        try:
                            selectsql = sql % x
                            sqlcursor.execute(selectsql, tuple(param))
                            obj = sqlcursor.fetchall()
                            i += 1
                            for obj_tmp in obj:
                                objs.append(obj_tmp)
                                if obj_tmp[2] != '' and obj_tmp[2] is not None:
                                    StockOrderNID.append(obj_tmp[2])
                            print i
                            break
                        except MySQLdb.Error, e:
                            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                            break
            if sqlcursor:
                sqlcursor.close()
            return objs, param1, StockOrderNID
        except pymssql.Error, e:
            print "pymssql Error %d: %s" % (e.args[0], e.args[1])

    def update_cg_StockOrderD(self, param,flag,my_time):
        log_time = tLog.write_redis_log('cg_StockOrderD', '', 0)
        print "Begin---{},Time:{},IN:{}".format("cg_StockOrderD", datetime.now(), len(param))
        objs, GoodsSKUIDs, StockOrderNID = self.getPyInfo(param,flag)
        try:
            if flag:
                # insertSQL = "REPLACE INTO py_db.cg_stockorderd(GoodsSKUID,Amount,StockOrderNID,NID) VALUES (%s,%s,%s,%s)"
                # public_obj = public(self.db_conn, self.sqlserver_conn)
                # public_obj.commitmanyFun(objs, insertSQL)

                # insertSQL = "REPLACE INTO py_db.cg_stockorderd(NID) VALUES ({})".format(Max_NID)
                # cursor = self.db_conn.cursor()
                # cursor.execute(insertSQL)
                # cursor.execute('commit')
                pass
            if objs:
                len_obj = len(objs)
            else:
                len_obj = 0
            print "End---{},Time:{},OUT:{}".format("cg_StockOrderD", datetime.now(), len_obj)
            tLog.write_redis_log('cg_StockOrderD', log_time, len_obj)
            if GoodsSKUIDs:
                cg_StockInD_obj = cg_StockInD(self.db_conn, self.sqlserver_conn)
                cg_StockInD_objs, cg_StockInM_objs = cg_StockInD_obj.update_cg_StockInD(GoodsSKUIDs,flag,my_time)

            public_obj = public(self.db_conn, self.sqlserver_conn)
            SKUList = public_obj.getSKU(GoodsSKUIDs)
            return SKUList, objs, cg_StockInD_objs, cg_StockInM_objs, GoodsSKUIDs, StockOrderNID
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
