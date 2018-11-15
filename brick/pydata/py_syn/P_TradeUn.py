# encoding: utf-8
"""
@author: ZhangYu
@contact: 292724306@qq.com
@site:
@software: PyCharm
@file: P_TradeUn.py
@time: 2017-12-21 15:21
"""

import MySQLdb
import pymssql
from public import *

#from brick.pydata.py_redis.py_SynRedis_pub import *
#redis_p = py_SynRedis_pub()
cf = ConfigParser.ConfigParser()
cf.read("/data/djangostack-1.9.7/apps/django/django_projects/Project/brick/pydata/py_syn/select.conf")
maxnumFetchone = cf.getint('myconfig', 'maxnumFetchone')


class P_TradeUn:
    def __init__(self, db_conn, sqlserver_conn):
        self.db_conn = db_conn
        self.sqlserver_conn = sqlserver_conn
        self.cursor = self.db_conn.cursor()

    def getPyInfo(self, NIDs):
        objs = []
        i = 0
        sql = "SELECT NID,SUFFIX,ORDERTIME,AMT,SALESTAX from P_TradeUn WHERE NID in (%s)"
        if NIDs:
            try:
                if self.sqlserver_conn:
                    sqlcursor = self.sqlserver_conn.cursor()
                while True:
                    if len(NIDs) > maxnumFetchone:
                        while True:
                            NIDs_tmp = NIDs[:maxnumFetchone]
                            x = ','.join(['%s'] * len(NIDs_tmp))
                            try:
                                selectsql = sql % x
                                sqlcursor.execute(selectsql, tuple(NIDs_tmp))
                                obj = sqlcursor.fetchall()
                            except pymssql.Error, e:
                                print "pymssql Error %d: %s" % (e.args[0], e.args[1])
                            else:
                                #print "P_TradeUn存入redis"
                                #print redis_p.setArrayToListRedis(obj, 'P_TradeUn', 1)
                                #print "P_TradeUn存入redis结束"
                                NIDs = NIDs[maxnumFetchone:]
                                i += 1
                                for obj_tmp in obj:
                                    objs.append(obj_tmp)
                                print i
                                break

                    if len(NIDs) <= maxnumFetchone:
                        while True:
                            x = ','.join(['%s'] * len(NIDs))
                            try:
                                selectsql = sql % x
                                sqlcursor.execute(selectsql, tuple(NIDs))
                                obj = sqlcursor.fetchall()
                            except pymssql.Error, e:
                                print "pymssql Error %d: %s" % (e.args[0], e.args[1])
                            else:
                                #print "P_TradeUn存入redis"
                                #print redis_p.setArrayToListRedis(obj, 'P_TradeUn', 1)
                                #print "P_TradeUn存入redis结束"
                                i += 1
                                for obj_tmp in obj:
                                    objs.append(obj_tmp)
                                print i
                                break
                        break
                if sqlcursor:
                    sqlcursor.close()
                # print objs
                return objs
            except pymssql.Error, e:
                print "pymssql Error %d: %s" % (e.args[0], e.args[1])

    def update_P_TradeUn(self, NIDs):
        print "开始更新{0}".format("P_TradeUn")
        objs = self.getPyInfo(NIDs)
        sql = "REPLACE INTO py_db.P_TradeUn(NID,SUFFIX,ORDERTIME,AMT,SALESTAX ) VALUES (%s,%s,%s,%s,%s)"
        public_obj = public(self.db_conn, self.sqlserver_conn)
        public_obj.commitmanyFun(objs, sql)
        print "结束更新{0}".format("P_TradeUn")
