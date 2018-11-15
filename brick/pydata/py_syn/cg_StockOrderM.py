# encoding: utf-8
"""
@author: ZhangYu
@contact: 292724306@qq.com
@site:
@software: PyCharm
@file: cg_StockOrderM.py
@time: 2017-12-19 19:16
"""


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



class cg_StockOrderM:
    def __init__(self, db_conn, sqlserver_conn):
        self.db_conn = db_conn
        self.sqlserver_conn = sqlserver_conn
        self.cursor = self.db_conn.cursor()

    def getPyInfo(self, OrderNIDs,my_time):
        objs = []
        i = 0
        try:
            if self.sqlserver_conn:
                sqlcursor = self.sqlserver_conn.cursor()
                while 'All' in OrderNIDs:
                    OrderNIDs.remove('All')
                # sql = "select replace(NID,' ',''),replace(StoreID,' ',''),replace(CheckFlag,' ','') from CG_StockOrderM where NID in (%s) and  CheckFlag = 1 and Archive = 0 and  MakeDate > '{0}'".format(my_time)
                sql = "select NID,StoreID,CONVERT(varchar(100), MakeDate, 120),CheckFlag,Archive,BillNumber from CG_StockOrderM(nolock) where NID in (%s)  and  MakeDate > '{0}'".format(
                    my_time)
                while True:
                    if len(OrderNIDs) > maxnumFetchone:
                        OrderNIDs_tmp = OrderNIDs[:maxnumFetchone]
                        OrderNIDs = OrderNIDs[maxnumFetchone:]
                        x = ','.join(['%s'] * len(OrderNIDs_tmp))
                        try:
                            selectsql = sql % x
                            sqlcursor.execute(selectsql, tuple(OrderNIDs_tmp))
                            obj = sqlcursor.fetchall()
                            i += 1
                            for obj_tmp in obj:
                                objs.append(obj_tmp)
                            print i
                        except MySQLdb.Error, e:
                            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                            break
                    if len(OrderNIDs) <= maxnumFetchone:
                        x = ','.join(['%s'] * len(OrderNIDs))
                        try:
                            selectsql = sql % x
                            sqlcursor.execute(selectsql, tuple(OrderNIDs))
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
            # print objs
            return objs
        except pymssql.Error, e:
            print "pymssql Error %d: %s" % (e.args[0], e.args[1])

    def update_cg_StockOrderM(self, StockOrderNID,flag,my_time):
        OrderNIDs = list(set(StockOrderNID))
        log_time = tLog.write_redis_log('cg_StockOrderM', '', 0)
        print "Begin---{},Time:{},IN:{}".format("cg_StockOrderM", datetime.now(), len(StockOrderNID))
        objs = self.getPyInfo(StockOrderNID,my_time)
        try:
            if flag:
                # insertSQL = "REPLACE INTO py_db.cg_stockorderm(NID,StoreID,MakeDate,CheckFlag,Archive,BillNumber) VALUES (%s,%s,%s,%s,%s,%s)"
                # public_obj = public(self.db_conn, self.sqlserver_conn)
                # public_obj.commitmanyFun(objs, insertSQL)
                pass
            if objs:
                len_obj = len(objs)
            else:
                len_obj = 0
            print "End---{},Time:{},OUT:{}".format("cg_StockOrderM", datetime.now(),len_obj)
            tLog.write_redis_log('cg_StockOrderM', log_time, len_obj)
            return objs
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
