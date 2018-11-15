# encoding: utf-8
"""
@author: ZhangYu
@contact: 292724306@qq.com
@site:
@software: PyCharm
@file: b_store.py
@time: 2017-12-21 15:21
"""

import MySQLdb
import pymssql


#from brick.pydata.py_redis.py_SynRedis_pub import *
#redis_p = py_SynRedis_pub()
class b_store:
    def __init__(self, db_conn, sqlserver_conn=None):
        self.db_conn = db_conn
        self.sqlserver_conn = sqlserver_conn
        self.cursor = self.db_conn.cursor()

    def getPyInfo(self, StoreIDs):
        objs = []
        try:
            if self.sqlserver_conn:
                sqlcursor = self.sqlserver_conn.cursor()
                x = ','.join(['%s'] * len(StoreIDs))
                selectsql = "select NID,CategoryLevel,StoreCode,StoreName,CategoryParentID,CategoryParentName," \
                            "CategoryOrder,CategoryCode,FitCode,Address,Used,Memo,URL,FitCountry,IsNegativeStock," \
                            "IsVirtual from B_Store where NID in (%s)" % x
                sqlcursor.execute(selectsql, tuple(StoreIDs))
                objtmp = sqlcursor.fetchall()
                #print "b_store存入redis"
                #print redis_p.setArrayToListRedis(objtmp, 'b_store', 1)
                #print "b_store存入redis结束"
                for obj in objtmp:
                    if obj:
                        objs.append(obj)
            if sqlcursor:
                sqlcursor.close()
            # print objs
            return objs
        except pymssql.Error, e:
            print "pymssql Error %d: %s" % (e.args[0], e.args[1])

    def update_b_store(self, objs):
        print u"开始更新{0}".format("b_store")
        StoreIDs = []
        for obj in objs:
            StoreIDs.append(obj[1])
        StoreIDs = list(set(StoreIDs))       #给列表去重
        objs = self.getPyInfo(StoreIDs)
        try:
            insertSQL = "replace INTO py_db.B_Store(NID,CategoryLevel,StoreCode,StoreName,CategoryParentID,CategoryParentName," \
                        "CategoryOrder,CategoryCode,FitCode,Address,Used,Memo,URL,FitCountry,IsNegativeStock," \
                        "IsVirtual) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cursor.executemany(insertSQL, objs)
            self.cursor.execute('commit')
            print u"结束更新{0}".format("b_store")
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
