# coding:utf-8
"""
@author: ZhangYu
@contact: 292724306@qq.com
@site:
@software: PyCharm
@file: py_information_by_P_TradeLogs.py
@time: 2017-12-30 13:27
"""
import MySQLdb
import pymssql

from public import *
from datetime import datetime
import ConfigParser
from P_trade import *
from P_TradeDt import *
from P_TradeDtUn import *
from P_TradeUn import *

cf = ConfigParser.ConfigParser()
cf.read("/data/djangostack-1.9.7/apps/django/django_projects/Project/brick/pydata/py_syn/select.conf")
maxnum = cf.getint('myconfig', 'maxnum')



class py_information_by_P_TradeLogs():
    def __init__(self, db_conn, sqlserver_conn):
        self.db_conn = db_conn
        self.sqlserver_conn = sqlserver_conn
        self.public_obj = public(self.db_conn, self.sqlserver_conn)

    # 输入普源日志到本地  用于下次判断
    def setHqLog(self, objs):
        print "开始更新{0}".format("P_TradeLogs")
        sql = "REPLACE INTO py_db.P_TradeLogs (NID,TradeNID) VALUES (%s,%s)"
        public_obj = public(self.db_conn)
        public_obj.commitmanyFun(objs, sql)
        print "结束更新{0}".format("P_TradeLogs")

    def setHqOP(self, SKUList):
        SKUListTmp = []
        # print SKUList
        for SKU in SKUList:
            SKU = SKU + ',3'
            SKU = SKU.split(',')
            SKUListTmp.append(SKU)
        # for SKU in SKUList:
        insertSql = "REPLACE INTO t_product_puyuan_op (sku,status) VALUES (%s,%s)"
        public_obj = public(self.db_conn)
        public_obj.commitmanyFun(SKUListTmp, insertSql)

    # 获取本地日志最大ID
    def getMaxNID(self):
        print "获取本地日志最大ID开始时间：{0}".format(datetime.now())
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                NIDSql = "SELECT MAX(NID) from py_db.P_TradeLogs"
                cursor.execute(NIDSql)
                NIDTuple = cursor.fetchone()
                if NIDTuple:
                    NID = NIDTuple[0]
                    print "获取本地日志最大ID结束时间：{0}".format(datetime.now())
                    return NID
        except MySQLdb.Error, e:
            # print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])


    # 获取普源日志
    def getPyLog(self):
        print "获取普源日志开始时间：{0}".format(datetime.now())
        objs = []
        NID = self.getMaxNID()
        if self.sqlserver_conn and NID:
            sqlcursor = self.sqlserver_conn.cursor()
            # selectsql = "SELECT NID,TradeNID,Operator,Logs from P_TradeLogs WHERE NID > %s  "
            selectsql = "SELECT NID,TradeNID from P_TradeLogs WHERE NID > %s"
            while True:
                try:
                    print "execute开始{0}".format(datetime.now())
                    sqlcursor.execute(selectsql, NID)
                    print "execute结束{0}".format(datetime.now())
                    public_obj = public()
                    objstmp = public_obj.fetchmanyFun(sqlcursor)
                except pymssql.Error, e:
                    print "pymssql Error %d: %s" % (e.args[0], e.args[1])
                else:
                    print "获取普源日志结束时间：{0}".format(datetime.now())
                    objs = objstmp
                    print len(objs)
                    break
            return objs


    def py_synchronization_by_P_TradeLogs(self):
        print u"P_TradeLogs程序开始时间：{0}".format(datetime.now())
        TradeNIDs = []
        NIDs = []
        i = 0
        try:
            objs = self.getPyLog()
            if objs:
                for obj in objs:
                    if obj[1].isdigit():
                        TradeNIDs.append(obj[1])
                    # NIDs.append(obj[0])
                    i += 1
                TradeNIDs = list(set(TradeNIDs))
                # NIDs = list(set(NIDs))
                P_trade_obj = P_trade(self.db_conn, self.sqlserver_conn)
                P_trade_obj.update_P_trade(TradeNIDs)

                P_TradeDt_obj = P_TradeDt(self.db_conn, self.sqlserver_conn)
                SKUList = P_TradeDt_obj.update_P_TradeDt(TradeNIDs)

                P_TradeDtUn_obj = P_TradeDtUn(self.db_conn, self.sqlserver_conn)
                P_TradeDtUn_obj.update_P_TradeDtUn(TradeNIDs)

                P_TradeUn_obj = P_TradeUn(self.db_conn, self.sqlserver_conn)
                P_TradeUn_obj.update_P_TradeUn(TradeNIDs)

                print i
                self.setHqLog(objs)
                if SKUList:
                    self.setHqOP(SKUList)
        except MySQLdb.Error, e:
            self.public_obj.setStatus("py_synchronization_by_P_TradeLogs", 3)
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            self.db_conn.rollback()
            print "P_TradeLogs任务失败"
        else:
            self.public_obj.setStatus("py_synchronization_by_P_TradeLogs", 1)
            print "程序结束时间：{0}".format(datetime.now())
        finally:
            self.db_conn.close()
            self.sqlserver_conn.close()
