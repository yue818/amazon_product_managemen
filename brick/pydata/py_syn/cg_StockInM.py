# encoding: utf-8
"""
@author: ZhangYu
@contact: 292724306@qq.com
@site:
@software: PyCharm
@file: cg_StockInM.py
@time: 2017-12-19 19:16
"""

import MySQLdb
import pymssql
import sys
#sys.path.append('/data/djangostack-1.9.7/apps/django/django_projects/Project')
from brick.pydata.py_redis.py_SynRedis_tables import py_redis_log
tLog = py_redis_log()
from public import *
import ConfigParser
cf = ConfigParser.ConfigParser()
cf.read("/data/djangostack-1.9.7/apps/django/django_projects/Project/brick/pydata/py_syn/select.conf")
maxnumFetchone = cf.getint('myconfig', 'maxnumFetchone')
class cg_StockInM:
    def __init__(self, db_conn, sqlserver_conn):
        self.db_conn = db_conn
        self.sqlserver_conn = sqlserver_conn
        self.cursor = self.db_conn.cursor()

    def getPyInfo(self, StockInNIDs,my_time):
        objs = []
        i = 0
        try:
            if self.sqlserver_conn:
                sqlcursor = self.sqlserver_conn.cursor()
                # sql = "select replace(NID,' ',''),replace(StoreID,' ',''),replace(CheckFlag,' ','') from CG_StockInM " \
                #       "where NID in (%s) and StoreID = '19' and CheckFlag = 1 and  MakeDate > '{0}'".format(my_time)
                sql = "select replace(NID,' ',''),replace(StoreID,' ',''),replace(CONVERT(varchar(100), MakeDate, 120),' ',''),replace(CheckFlag,' ',''),replace(StockOrder,' ','') from CG_StockInM(nolock) " \
                      "where NID in (%s) and StoreID = '19' and CheckFlag = 1 and  MakeDate > '{0}'".format(my_time)
                # print sql
                # print StockInNIDs
                while True:
                    if len(StockInNIDs) > maxnumFetchone:
                        StockInNIDs_tmp = StockInNIDs[:maxnumFetchone]
                        StockInNIDs = StockInNIDs[maxnumFetchone:]
                        x = ','.join(['%s'] * len(StockInNIDs_tmp))
                        try:
                            selectsql = sql % x
                            sqlcursor.execute(selectsql, tuple(StockInNIDs_tmp))
                            obj = sqlcursor.fetchall()
                            i += 1
                            for obj_tmp in obj:
                                objs.append(obj_tmp)
                            print i
                        except MySQLdb.Error, e:
                            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                            break
                    if len(StockInNIDs) <= maxnumFetchone:
                        x = ','.join(['%s'] * len(StockInNIDs))
                        try:
                            selectsql = sql % x
                            sqlcursor.execute(selectsql, tuple(StockInNIDs))
                            obj = sqlcursor.fetchall()
                            i += 1
                            for obj_tmp in obj:
                                objs.append(obj_tmp)
                            print i
                            break
                        except MySQLdb.Error, e:
                            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                            break
            if sqlcursor:
                sqlcursor.close()
            return objs
        except pymssql.Error, e:
            print "pymssql Error %d: %s" % (e.args[0], e.args[1])

    def update_cg_StockInM(self, StockInNIDs,flag,my_time):
        StockInNIDs = list(set(StockInNIDs))
        log_time = tLog.write_redis_log('cg_StockInM', '', 0)
        print "Begin---{},Time:{},IN:{}".format("cg_StockInM", datetime.now(), len(StockInNIDs))
        cursor = self.db_conn.cursor()
        objs = self.getPyInfo(StockInNIDs,my_time)
        try:
            if flag:
                # insertSQL = "REPLACE INTO py_db.cg_stockinm(NID,StoreID,MakeDate,CheckFlag,StockOrder) VALUES (%s,%s,%s,%s,%s)"
                # public_obj = public(self.db_conn, self.sqlserver_conn)
                # public_obj.commitmanyFun(objs, insertSQL)
                pass
            if objs:
                len_obj = len(objs)
            else:
                len_obj = 0
            print "End---{},Time:{},OUT:{}".format("cg_StockInM", datetime.now(), len_obj)
            tLog.write_redis_log('cg_StockInM', log_time, len_obj)
            return objs
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
