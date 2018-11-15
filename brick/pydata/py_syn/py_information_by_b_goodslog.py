# coding:utf-8
"""
@author: ZhangYu
@contact: 292724306@qq.com
@site:
@software: PyCharm
@file: py_information_by_b_goodslog.py
@time: 2017-12-30 13:27
"""
import MySQLdb
import pymssql
from b_goods import *
from b_goodsSKU import *
from b_supplier import *
from datetime import datetime
from public import *


class py_information_by_b_goodslog():
    def __init__(self, db_conn, sqlserver_conn):
        self.db_conn = db_conn
        # self.db_connhq = db_connhq
        self.sqlserver_conn = sqlserver_conn
        self.public_obj = public(self.db_conn, self.sqlserver_conn)

    #获取本地日志最大ID  对比普源来更新SKU
    def getMaxNID(self):
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                NIDSql = "SELECT MAX(NID) from py_db.B_GoodsLogs"
                cursor.execute(NIDSql)
                NIDTuple = cursor.fetchone()
                if NIDTuple:
                    NID = NIDTuple[0]
                    return NID
        except MySQLdb.Error, e:
            #print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    #获取普源日志
    def getPyLog(self):
        objs = []
        NID = self.getMaxNID()
        if self.sqlserver_conn and NID:
            sqlcursor = self.sqlserver_conn.cursor()
            selectsql = "SELECT NID,GoodsCode,Operator,Logs from B_GoodsLogs(nolock) WHERE NID > %s  "
            try:
                sqlcursor.execute(selectsql, NID)
                public_obj = public()
                objs = public_obj.fetchmanyFun(sqlcursor)
                return objs
            except pymssql.Error, e:
                print "pymssql Error %d: %s" % (e.args[0], e.args[1])

    #输入普源日志到本地  用于下次判断
    def setHqLog(self, objs):
        try:
            insertSql = "REPLACE INTO py_db.B_GoodsLogs VALUES (%s,%s,%s,%s)"
            public_obj = public(self.db_conn, self.sqlserver_conn)
            public_obj.commitmanyFun(objs, insertSql)
        except MySQLdb.Error, e:
            #print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def setHqOP(self, SKUList):
        cursor = self.db_conn.cursor()
        SKUListTmp = []
        try:
            if SKUList:
                # print SKUList
                for SKU in SKUList:
                    SKU = SKU + ',1'
                    SKU = SKU.split(',')
                    SKUListTmp.append(SKU)
                # for SKU in SKUList:
                insertSql = "REPLACE INTO t_product_puyuan_op (sku,status,Op_time) VALUES (%s,%s,'{0}')".format(datetime.now())
                public_obj = public(self.db_conn, self.sqlserver_conn)
                public_obj.commitmanyFun(SKUListTmp, insertSql)
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def getSKU(self,obj):
        log = obj[3]
        SKU = ''
        if obj[1] != '':
            # print u"有SKU"
            SKU = obj[1]
            return SKU
        if obj[1] == '' and obj[3] != '':
            # print u"不包含SKU 但是有日志"
            if '(' in log:
                SKU = log[log.rfind('(') + 2:log.rfind(')')]
                return SKU
            else:
                SKU = log[log.rfind(' ') + 1:log.rfind(',')]
                return SKU


    #同步普源信息  通过解析日志中的SKU  三种情况 ==》1. 直接在SKU字段中  2. 在日志中用()包围  3.在日志中未用()包围
    def py_synchronization_by_b_goodslog(self):
        print "b_goodslog---program---Begin：{0}".format(datetime.now())
        SKUList = []
        SupplierID = []
        i = 0
        try:
            b_goodsSKU_obj = b_goodsSKU(self.db_conn, self.sqlserver_conn)
            b_supplier_obj = b_supplier(self.db_conn, self.sqlserver_conn)
            b_goods_obj = b_goods(self.db_conn, self.sqlserver_conn)
            objs = self.getPyLog()
            print "logs.length:{}".format(len(objs))
            if objs:
                for obj in objs:
                    SKU = self.getSKU(obj)
                    if SKU:
                        SKUList.append(SKU)
                    i += 1
            SKUList = list(set(SKUList))
            print "SKUList.length:{}".format(len(SKUList))
            if SKUList:
                SupplierID = b_goods_obj.update_b_goods(SKUList)
                # 更新b_goodsSKU表
                b_goodsSKU_obj.update_b_goodsSKU(SKUList)
                # 获取三个字段信息
                if SupplierID:
                    # 更新b_supplier表
                    SupplierID = list(set(SupplierID))
                    b_supplier_obj.update_b_supplier(SupplierID)
                self.setHqLog(objs)
                self.setHqOP(SKUList)
        except MySQLdb.Error, e:
            self.public_obj.setStatus("py_synchronization_by_b_goodslog", 3)
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            self.db_conn.rollback()
            print u"b_goodslogs--program--Failed"
        else:
            self.public_obj.setStatus("py_synchronization_by_b_goodslog", 1)
            print "b_goodslog---program---End：{0}".format(datetime.now())
        finally:
            self.db_conn.close()
            self.sqlserver_conn.close()
