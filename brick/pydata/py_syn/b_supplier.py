# encoding: utf-8
"""
@author: ZhangYu
@contact: 292724306@qq.com
@site: 
@software: PyCharm
@file: b_supplier.py
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


# 联表查询供应商名称
class b_supplier:
    def __init__(self, db_conn, sqlserver_conn=None):
        self.db_conn = db_conn
        self.sqlserver_conn = sqlserver_conn
        self.cursor = self.db_conn.cursor()

    def selectSupplierName(self, SupplierID):
        sql = "SELECT SupplierName from b_supplier WHERE NID=%s"
        self.cursor.execute(sql, SupplierID)
        SupplierName = self.cursor.fetchone()
        if SupplierName:
            return SupplierName
        else:
            return ''

    def getPyInfo(self, SupplierIDs):
        i = 0
        b_supplier_objs = []
        selectsql = "select NID,CategoryID,SupplierCode,SupplierName,FitCode,LinkMan,Address,OfficePhone," \
                    "Mobile,Used,Recorder,InputDate,Modifier,ModifyDate,Email,QQ,MSN,ArrivalDays,URL,Memo," \
                    "Account,CreateDate,SupPurchaser,supplierLoginId from B_Supplier where NID in (%s)"
        try:
            if self.sqlserver_conn:
                sqlcursor = self.sqlserver_conn.cursor()
                while True:
                    if len(SupplierIDs) > maxnumFetchone:
                        SupplierIDs_tmp = SupplierIDs[:maxnumFetchone]
                        SupplierIDs = SupplierIDs[maxnumFetchone:]
                        x = ','.join(['%s'] * len(SupplierIDs_tmp))
                        sql = selectsql % x
                        sqlcursor.execute(sql, tuple(SupplierIDs_tmp))
                        objs = sqlcursor.fetchall()
                        for obj in objs:
                            if obj:
                                b_supplier_objs.append(obj)
                        i += 1
                    if len(SupplierIDs) <= maxnumFetchone:
                        x = ','.join(['%s'] * len(SupplierIDs))
                        sql = selectsql % x
                        sqlcursor.execute(sql, tuple(SupplierIDs))
                        objs = sqlcursor.fetchall()
                        for obj in objs:
                            if obj:
                                b_supplier_objs.append(obj)
                        i += 1
                        break
                    print i
            if sqlcursor:
                sqlcursor.close()
            # print objs
            return b_supplier_objs
        except pymssql.Error, e:
            print "pymssql Error %d: %s" % (e.args[0], e.args[1])

    def update_b_supplier(self, SupplierIDs):
        print "Begin{},Time:{},Count:{}".format("b_supplier", datetime.now(), len(SupplierIDs))
        objs = self.getPyInfo(SupplierIDs)
        try:
            insertSQL = "replace INTO py_db.b_supplier(NID,CategoryID,SupplierCode,SupplierName,FitCode,LinkMan,Address,OfficePhone," \
                        "Mobile,Used,Recorder,InputDate,Modifier,ModifyDate,Email,QQ,MSN,ArrivalDays,URL,Memo," \
                        "Account,CreateDate,SupPurchaser,supplierLoginId" \
                        ") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                        "%s,%s,%s,%s,%s,%s)"
            public_obj = public(self.db_conn, self.sqlserver_conn)
            public_obj.commitmanyFun(objs, insertSQL)
            print "End{},Time:{},Count:{}".format("b_supplier", datetime.now(), len(SupplierIDs))
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
