# encoding: utf-8
"""
@author: ZhangYu
@contact: 292724306@qq.com
@site:
@software: PyCharm
@file: cg_StockInD.py
@time: 2017-12-19 19:16
"""


import MySQLdb
import pymssql
from cg_StockInM import *
from public import *
import ConfigParser
import sys
# sys.path.append('/data/djangostack-1.9.7/apps/django/django_projects/Project')
from brick.pydata.py_redis.py_SynRedis_tables import py_redis_log
tLog = py_redis_log()
cf = ConfigParser.ConfigParser()
cf.read("/data/djangostack-1.9.7/apps/django/django_projects/Project/brick/pydata/py_syn/select.conf")
maxnumFetchone = cf.getint('myconfig', 'maxnumFetchone')
class cg_StockInD:
    def __init__(self, db_conn, sqlserver_conn):
        self.db_conn = db_conn
        self.sqlserver_conn = sqlserver_conn
        self.cursor = self.db_conn.cursor()

    def getMaxNID(self):
        NID = ''
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                NIDSql = "SELECT MAX(NID) from py_db.cg_stockind"
                cursor.execute(NIDSql)
                NIDTuple = cursor.fetchone()
                if NIDTuple:
                    NID = NIDTuple[0]
                    return NID
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def getPyInfo(self, GoodsSKUIDs,flag):
        objs = []
        i = 0
        StockInNIDs = []
        try:
            if self.sqlserver_conn:
                sqlcursor = self.sqlserver_conn.cursor()
                # sql = "select replace(StockInNID,' ',''),replace(GoodsSKUID,' ',''),replace(cast(Amount AS VARCHAR ),' ','') from CG_StockInD where GoodsSKUID in (%s)"
                sql = "select replace(GoodsSKUID,' ',''),replace(StockInNID,' ',''),replace(cast(Amount AS VARCHAR ),' ',''),replace(NID,' ','') from CG_StockInD(nolock) where GoodsSKUID in (%s)"
                # if flag:
                #     NID = self.getMaxNID()
                #     # NID = 2300000
                #     if NID:
                #         sql = "select replace(GoodsSKUID,' ',''),replace(StockInNID,' ',''),replace(cast(Amount AS VARCHAR ),' ',''),replace(NID,' ','') from CG_StockInD(nolock) where GoodsSKUID in (%s) AND NID>{}".format(NID)
                while True:
                    if len(GoodsSKUIDs) > maxnumFetchone:
                        GoodsSKUIDs_tmp = GoodsSKUIDs[:maxnumFetchone]
                        GoodsSKUIDs = GoodsSKUIDs[maxnumFetchone:]
                        x = ','.join(['%s'] * len(GoodsSKUIDs_tmp))
                        try:
                            selectsql = sql % x
                            sqlcursor.execute(selectsql, tuple(GoodsSKUIDs_tmp))
                            obj = sqlcursor.fetchall()
                            i += 1
                            for obj_tmp in obj:
                                objs.append(obj_tmp)
                                if obj_tmp[1] != '' and obj_tmp[1] is not None:
                                    StockInNIDs.append(obj_tmp[1])
                            print i
                        except MySQLdb.Error, e:
                            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                            break
                    if len(GoodsSKUIDs) <= maxnumFetchone:
                        x = ','.join(['%s'] * len(GoodsSKUIDs))
                        try:
                            selectsql = sql % x
                            sqlcursor.execute(selectsql, tuple(GoodsSKUIDs))
                            obj = sqlcursor.fetchall()
                            i += 1
                            for obj_tmp in obj:
                                objs.append(obj_tmp)
                                if obj_tmp[1] != '' and obj_tmp[1] is not None:
                                    StockInNIDs.append(obj_tmp[1])
                            print i
                            break
                        except MySQLdb.Error, e:
                            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                            break
            if sqlcursor:
                sqlcursor.close()
            return objs, StockInNIDs
        except pymssql.Error, e:
            print "pymssql Error %d: %s" % (e.args[0], e.args[1])

    def  update_cg_StockInD(self, GoodsSKUIDs,flag,my_time):
        GoodsSKUIDs = list(set(GoodsSKUIDs))
        print "Begin---{},Time:{},IN:{}".format("cg_StockInD", datetime.now(), len(GoodsSKUIDs))
        log_time = tLog.write_redis_log('cg_StockInD', '', 0)
        cursor = self.db_conn.cursor()
        cg_StockInM_objs = []
        objs, StockInNIDs = self.getPyInfo(GoodsSKUIDs,flag)
        try:
            if flag:
                # insertSQL = "REPLACE INTO py_db.cg_stockind(GoodsSKUID,StockInNID,Amount,NID) VALUES (%s,%s,%s,%s)"
                # public_obj = public(self.db_conn, self.sqlserver_conn)
                # public_obj.commitmanyFun(objs, insertSQL)

                # insertSQL = "REPLACE INTO py_db.cg_stockind(NID) VALUES ({})".format(Max_NID)
                # cursor = self.db_conn.cursor()
                # cursor.execute(insertSQL)
                # cursor.execute('commit')
                pass
            if objs:
                len_obj = len(objs)
            else:
                len_obj = 0
            print "End---{},Time:{},OUT:{}".format("cg_StockInD", datetime.now(), len_obj)
            tLog.write_redis_log('cg_StockInD', log_time, len_obj)
            if StockInNIDs:
                cg_StockInM_obj = cg_StockInM(self.db_conn, self.sqlserver_conn)
                cg_StockInM_objs = cg_StockInM_obj.update_cg_StockInM(StockInNIDs, flag,my_time)
            return objs,cg_StockInM_objs
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
