# encoding: utf-8
"""
@author: ZhangYu
@contact: 292724306@qq.com
@site:
@software: PyCharm
@file: b_goodsSKULocation.py
@time: 2017-12-21 15:21
"""
import logging
import MySQLdb
import pymssql
from b_storelocation import *
from public import public
from datetime import datetime
import ConfigParser

cf = ConfigParser.ConfigParser()
cf.read("/data/djangostack-1.9.7/apps/django/django_projects/Project/brick/pydata/py_syn/select.conf")
maxnumFetchone = cf.getint('myconfig', 'maxnumFetchone')


class b_goodsSKULocation:
    def __init__(self, db_conn, sqlserver_conn=None):
        self.db_conn = db_conn
        self.sqlserver_conn = sqlserver_conn
        self.cursor = self.db_conn.cursor()

    def getPyInfo(self, goodsSKUIDs):
        i = 0
        b_skuloc_objs = []
        LocationIDs = []
        selectsql = "select NID,StoreID,LocationID,GoodsSKUID from B_GoodsSKULocation(nolock) where GoodsSKUID in (%s)"
        try:
            if self.sqlserver_conn:
                sqlcursor = self.sqlserver_conn.cursor()
                while True:
                    if len(goodsSKUIDs) > maxnumFetchone:
                        goodsSKUIDs_tmp = goodsSKUIDs[:maxnumFetchone]
                        goodsSKUIDs = goodsSKUIDs[maxnumFetchone:]
                        x = ','.join(['%s'] * len(goodsSKUIDs_tmp))
                        sql = selectsql % x
                        sqlcursor.execute(sql, tuple(goodsSKUIDs_tmp))
                        objs = sqlcursor.fetchall()
                        for obj in objs:
                            if obj:
                                b_skuloc_objs.append(obj)
                                LocationIDs.append(obj[2])
                        i += 1
                    if len(goodsSKUIDs) <= maxnumFetchone:
                        x = ','.join(['%s'] * len(goodsSKUIDs))
                        sql = selectsql % x
                        sqlcursor.execute(sql, tuple(goodsSKUIDs))
                        objs = sqlcursor.fetchall()
                        for obj in objs:
                            if obj:
                                b_skuloc_objs.append(obj)
                                LocationIDs.append(obj[2])
                        i += 1
                        break
                    print i
            if sqlcursor:
                sqlcursor.close()
            # print objs
            return b_skuloc_objs, LocationIDs
        except pymssql.Error, e:
            print "pymssql Error %d: %s" % (e.args[0], e.args[1])

    def update_b_goodsSKULocation(self, goodsSKUIDs):
        print "Begin:{},Time:{},Count:{}".format("b_goodsSKULocation", datetime.now(), len(goodsSKUIDs))
        goodsSKUIDs = list(set(goodsSKUIDs))
        objs, LocationIDs = self.getPyInfo(goodsSKUIDs)
        try:
            insertSQL = "Replace INTO py_db.B_GoodsSKULocation (NID,StoreID,LocationID,GoodsSKUID) VALUES (%s,%s,%s,%s)"
            public_obj = public(self.db_conn, self.sqlserver_conn)
            public_obj.commitmanyFun(objs, insertSQL)
            print "End:{},Time:{},Count:{}".format("b_goodsSKULocation", datetime.now(), len(goodsSKUIDs))

            # 更新b_storelocation表
            b_storelocation_obj = b_storelocation(self.db_conn, self.sqlserver_conn)
            b_storelocation_obj.update_b_storelocation(LocationIDs)
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
