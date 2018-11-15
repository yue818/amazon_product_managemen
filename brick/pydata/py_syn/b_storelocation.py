# encoding: utf-8
"""
@author: ZhangYu
@contact: 292724306@qq.com
@site:
@software: PyCharm
@file: b_storelocation.py
@time: 2017-12-21 15:21
"""
import logging
import MySQLdb
import pymssql
import ConfigParser
from public import public
from datetime import datetime

cf = ConfigParser.ConfigParser()
cf.read("/data/djangostack-1.9.7/apps/django/django_projects/Project/brick/pydata/py_syn/select.conf")
maxnumFetchone = cf.getint('myconfig', 'maxnumFetchone')


class b_storelocation:
    def __init__(self, db_conn, sqlserver_conn=None):
        self.db_conn = db_conn
        self.sqlserver_conn = sqlserver_conn
        self.cursor = self.db_conn.cursor()

    def getPyInfo(self, LocationIDs):
        i = 0
        b_store_objs = []
        selectsql = "select NID,StoreID,StoreCode,LocationName,LocationOrder,Address,Used,Memo,Recorder," \
                    "InputDate,Modifier,ModifyDate from B_StoreLocation(nolock) where NID in (%s)"
        try:
            if self.sqlserver_conn:
                sqlcursor = self.sqlserver_conn.cursor()
                while True:
                    if len(LocationIDs) > maxnumFetchone:
                        LocationIDs_tmp = LocationIDs[:maxnumFetchone]
                        LocationIDs = LocationIDs[maxnumFetchone:]
                        x = ','.join(['%s'] * len(LocationIDs_tmp))
                        sql = selectsql % x
                        sqlcursor.execute(sql, tuple(LocationIDs_tmp))
                        objs = sqlcursor.fetchall()
                        for obj in objs:
                            if obj:
                                b_store_objs.append(obj)
                        i += 1
                    if len(LocationIDs) <= maxnumFetchone:
                        x = ','.join(['%s'] * len(LocationIDs))
                        sql = selectsql % x
                        sqlcursor.execute(sql, tuple(LocationIDs))
                        objs = sqlcursor.fetchall()
                        for obj in objs:
                            if obj:
                                b_store_objs.append(obj)
                        i += 1
                        break
                    print i
            if sqlcursor:
                sqlcursor.close()
            return b_store_objs
        except pymssql.Error, e:
            print "pymssql Error %d: %s" % (e.args[0], e.args[1])

    def update_b_storelocation(self, LocationIDs):
        print "Begin:{},Time:{},Count:{}".format("b_storelocation", datetime.now(), len(LocationIDs))
        LocationIDs = list(set(LocationIDs))  # 给列表去重
        objs = self.getPyInfo(LocationIDs)
        try:
            insertSQL = "REPLACE INTO py_db.B_StoreLocation (NID,StoreID,StoreCode,LocationName,LocationOrder,Address,Used,Memo,Recorder," \
                        "InputDate,Modifier,ModifyDate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            public_obj = public(self.db_conn, self.sqlserver_conn)
            public_obj.commitmanyFun(objs, insertSQL)
            print "End:{},Time:{},Count:{}".format("b_storelocation", datetime.now(), len(LocationIDs))
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
