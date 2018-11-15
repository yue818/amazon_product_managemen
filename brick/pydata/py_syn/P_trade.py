# encoding: utf-8
"""
@author: ZhangYu
@contact: 292724306@qq.com
@site:
@software: PyCharm
@file: P_trade.py
@time: 2017-12-21 15:21
"""
import ConfigParser

import MySQLdb
import pymssql
from public import *
from datetime import datetime


#from brick.pydata.py_redis.py_SynRedis_pub import *
#redis_p = py_SynRedis_pub()
cf = ConfigParser.ConfigParser()
cf.read("/data/djangostack-1.9.7/apps/django/django_projects/Project/brick/pydata/py_syn/select.conf")
maxnumFetchone = cf.getint('myconfig', 'maxnumFetchone')


class P_trade:
    def __init__(self, db_conn, sqlserver_conn):
        self.db_conn = db_conn
        self.sqlserver_conn = sqlserver_conn
        self.cursor = self.db_conn.cursor()

    def getPyInfo(self, TradeNIDs):
        print "获取p_trade开始时间：{0}".format(datetime.now())
        objs = []
        i = 0
        sql = "select NID,SUFFIX,ORDERTIME,AMT,SALESTAX from P_Trade where NID in (%s)"
        try:
            if self.sqlserver_conn:
                sqlcursor = self.sqlserver_conn.cursor()
                while True:
                    if len(TradeNIDs) > maxnumFetchone:
                        while True:
                            TradeNIDs_tmp = TradeNIDs[:maxnumFetchone]
                            x = ','.join(['%s'] * len(TradeNIDs_tmp))
                            try:
                                selectsql = sql % x
                                sqlcursor.execute(selectsql, tuple(TradeNIDs_tmp))
                                obj = sqlcursor.fetchall()
                            except pymssql.Error, e:
                                print "pymssql Error %d: %s" % (e.args[0], e.args[1])
                            else:
                                #print "P_trade存入redis"
                                #print redis_p.setArrayToListRedis(obj, 'P_trade', 1)
                                #print "P_trade存入redis结束"
                                TradeNIDs = TradeNIDs[maxnumFetchone:]
                                i += 1
                                for obj_tmp in obj:
                                    objs.append(obj_tmp)
                                print i
                                break

                    if len(TradeNIDs) <= maxnumFetchone:
                        while True:
                            x = ','.join(['%s'] * len(TradeNIDs))
                            try:
                                selectsql = sql % x
                                sqlcursor.execute(selectsql, tuple(TradeNIDs))
                                obj = sqlcursor.fetchall()
                            except pymssql.Error, e:
                                print "pymssql Error %d: %s" % (e.args[0], e.args[1])
                            else:
                                #print "P_trade存入redis"
                                #print redis_p.setArrayToListRedis(obj, 'P_trade', 1)
                                #print "P_trade存入redis结束"
                                i += 1
                                for obj_tmp in obj:
                                    objs.append(obj_tmp)
                                print i
                                break
                        break
            if sqlcursor:
                sqlcursor.close()
            # print objs
            print "获取p_trade结束时间：{0}".format(datetime.now())
            return objs
        except pymssql.Error, e:
            print "pymssql Error %d: %s" % (e.args[0], e.args[1])

    def update_P_trade(self, TradeNIDs):
        objs = self.getPyInfo(TradeNIDs)
        print "开始更新{0}".format("P_trade")
        if objs:
            sql = "Replace INTO py_db.P_trade(NID,SUFFIX,ORDERTIME,AMT,SALESTAX) VALUES (%s,%s,%s,%s,%s)"
            public_obj = public(self.db_conn, self.sqlserver_conn)
            public_obj.commitmanyFun(objs, sql)
            print "结束更新{0}".format("P_trade")

        else:
            print "{0}更新失败".format("P_trade")