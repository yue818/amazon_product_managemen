# coding:utf-8
"""
@author: ZhangYu
@contact: 292724306@qq.com
@site:
@software: PyCharm
@file: MiniPrograms.py
@time: 2017-12-30 13:27
"""
import MySQLdb
import pymssql
from updateto_t_product_b_goods import *


class py_information():
    def __init__(self, db_conn, sqlserver_conn):
        self.db_conn = db_conn
        # self.db_connhq = db_connhq
        self.sqlserver_conn = sqlserver_conn

    #获取本地日志最大ID  对比普源来更新SKU
    def getMaxNID(self):
        try:
            if self.db_conn:
                cursor = self.db_conn.cursor()
                NIDSql = "SELECT MAX(NID) from py_db.B_GoodsLogs"
                cursor.execute(NIDSql)
                NIDTuple = cursor.fetchone()
                NID = NIDTuple[0]
                return NID
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    #获取普源日志
    def getPyLog(self):
        NID = self.getMaxNID()
        if self.sqlserver_conn and NID:
            sqlcursor = self.sqlserver_conn.cursor()
            selectsql = "SELECT NID,GoodsCode,Operator,Logs from B_GoodsLogs WHERE NID > %s  "
            try:
                sqlcursor.execute(selectsql, NID)
                objs = sqlcursor.fetchall()
                return objs
            except Exception:
                print "普源数据库获取错误"

    #输入普源日志到本地  用于下次判断
    def setHqLog(self, objs):
        cursor = self.db_conn.cursor()
        try:
		    if objs:
				for obj in objs:
					if obj:
						insertSql = "INSERT INTO py_db.B_GoodsLogs VALUES (%s,%s,%s,%s)"
						cursor.execute(insertSql, obj)
				cursor.execute('commit')
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            self.db_conn.rollback()

    def getSKU(self,obj):
        print obj[0]
        # print obj[0]
        log = obj[3]
        SKU = ''
        if obj[1] != '':
            print "有SKU"
            SKU = obj[1]
            return SKU
        if obj[1] == '' and obj[3] != '':
            print u"不包含SKU 但是有日志"
            if '(' in log:
                SKU = log[log.rfind('(') + 2:log.rfind(')')]
                return SKU
            else:
                SKU = log[log.rfind(' ') + 1:log.rfind(',')]
                return SKU


    #同步普源信息  通过解析日志中的SKU  三种情况 ==》1. 直接在SKU字段中  2. 在日志中用()包围  3.在日志中未用()包围
    def py_synchronization(self):
        SKU = ''
        i = 0
        try:
            updateto_t_product_b_goods_obj = updateto_t_product_b_goods(self.db_conn, self.sqlserver_conn)
            objs = self.getPyLog()
            if objs:
                for obj in objs:
                    SKU = self.getSKU(obj)
                    if SKU:
                        updateto_t_product_b_goods_obj.update_b_goods(SKU)
                    print "-------------------------------------------------------------"
                    i += 1
            print i
            self.setHqLog(objs)

        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            self.db_conn.rollback()

        finally:
            self.db_conn.close()
            self.sqlserver_conn.close()
