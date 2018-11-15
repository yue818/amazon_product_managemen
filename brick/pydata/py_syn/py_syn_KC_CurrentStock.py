# coding:utf-8
"""
@author: ZhangYu
@contact: 292724306@qq.com
@site:
@software: PyCharm
@file: py_syn_KC_CurrentStock.py
@time: 2017-1-23 17:31
"""
import MySQLdb
import pymssql
import sys
#sys.path.append('/data/djangostack-1.9.7/apps/django/django_projects/Project')
from public import *
import ConfigParser
import time
from datetime import datetime as this_datetime
from brick.pydata.py_redis.py_SynRedis_tables import py_SynRedis_tables
cf = ConfigParser.ConfigParser()
cf.read("/data/djangostack-1.9.7/apps/django/django_projects/Project/brick/pydata/py_syn/select.conf")
maxnumFetchone = cf.getint('myconfig', 'maxnumFetchone')


class py_syn_KC_CurrentStock():
    def __init__(self, db_conn, sqlserver_conn):
        self.db_conn = db_conn
        self.sqlserver_conn = sqlserver_conn
        self.cursor = db_conn.cursor()
        self.public_obj = public(self.db_conn, self.sqlserver_conn)

    # 获取t_product_puyuan_op表中的SKU信息
    def getSKUList(self):
        SKUList = []
        objs,SKUList,ids = self.public_obj.getSKUList()
        return objs,SKUList,ids

    # 获取运行状态  返回 1 则运行  ；返回 0 则不运行          1分钟后再次运行该任务
    def getStatus(self):
        status = 0
        cursor = self.cursor
        tasksSql = "select depend_on_task from py_db.t_celery_task_depend where task = 'update_KC_CurrentStock'"
        cursor.execute(tasksSql)
        dependTasks = cursor.fetchall()
        if dependTasks:
            for dependTask in dependTasks:
                statusSql = "select status from py_db.t_celery_task_status where task = '{0}'".format(dependTask[0])
                cursor.execute(statusSql)
                status_tmp = cursor.fetchone()
                status = int(status_tmp[0])
                if status != 1:
                    return status
            return 1
        return 0

    def getGoodsSKUID(self, SKUlist):
        GoodsSKUIDs = []
        GoodsSKUIDs = self.public_obj.getGoodsSKUIDs(SKUlist)
        return GoodsSKUIDs

    def getPyInfo(self, GoodsSKUIDs):
        objs = []
        i = 0
        sql = "SELECT NID,StoreID,GoodsID,GoodsSKUID,Number,Money,Price,ReservationNum,OutCode,WarningCats,SaleDate," \
              "KcMaxNum,KcMinNum,SellCount1,SellCount2,SellCount3,SellDays,StockDays,SellCount from KC_CurrentStock WHERE GoodsSKUID in (%s)"
        try:
            if self.sqlserver_conn:
                sqlcursor = self.sqlserver_conn.cursor()
            while True:
                if len(GoodsSKUIDs) > maxnumFetchone:
                    while True:
                        GoodsSKUIDs_tmp = GoodsSKUIDs[:maxnumFetchone]
                        x = ','.join(['%s'] * len(GoodsSKUIDs_tmp))
                        try:
                            selectsql = sql % x
                            sqlcursor.execute(selectsql, tuple(GoodsSKUIDs_tmp))
                            obj = sqlcursor.fetchall()
                        except pymssql.Error, e:
                            print "pymssql Error %d: %s" % (e.args[0], e.args[1])
                        else:
                            # print "KC_CurrentStock存入redis"
                            # print redis_p.setArrayToHashRedis("KC_CurrentStock", 4, 2, obj)
                            # print "KC_CurrentStock存入redis结束"
                            GoodsSKUIDs = GoodsSKUIDs[maxnumFetchone:]
                            i += 1
                            for obj_tmp in obj:
                                objs.append(obj_tmp)
                            print i
                            break

                if len(GoodsSKUIDs) <= maxnumFetchone:
                    while True:
                        x = ','.join(['%s'] * len(GoodsSKUIDs))
                        try:
                            selectsql = sql % x
                            sqlcursor.execute(selectsql, tuple(GoodsSKUIDs))
                            obj = sqlcursor.fetchall()
                        except pymssql.Error, e:
                            print "pymssql Error %d: %s" % (e.args[0], e.args[1])
                        else:
                            # print "KC_CurrentStock存入redis"
                            # print redis_p.setArrayToHashRedis("KC_CurrentStock", 4, 2, obj)
                            # print "KC_CurrentStock存入redis结束"
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

    def setStatus(self):
        cursor = self.cursor
        tasksSql = "select depend_on_task from py_db.t_celery_task_depend where task = 'update_KC_CurrentStock'"
        cursor.execute(tasksSql)
        dependTasks = cursor.fetchall()
        if dependTasks:
            for dependTask in dependTasks:
                self.public_obj.setStatus(dependTask[0], 0)
        # self.public_obj.setStatus("py_synchronization_by_b_goodslog", 0)
        # self.public_obj.setStatus("py_synchronization_by_P_TradeLogs", 0)
        # self.public_obj.setStatus("py_synchronization_by_cg_stocklogs", 0)

    def update_KC_CurrentStock(self):
        print "开始更新{0}".format("KC_CurrentStock")
        flag = self.getStatus()
        i = 0
        if flag == 1:
            OPobjs,SKUList,ids = self.getSKUList()
            SKUList = list(set(SKUList))
            if SKUList:
                GoodsSKUIDs = self.getGoodsSKUID(SKUList)
                GoodsSKUIDs = list(set(GoodsSKUIDs))
                if GoodsSKUIDs:
                    objs = self.getPyInfo(GoodsSKUIDs)
                    if objs:
                        try:
                            insertSQL = "replace INTO py_db.KC_CurrentStock (NID,StoreID,GoodsID,GoodsSKUID,Number," \
                                        "Money,Price,ReservationNum,OutCode,WarningCats,SaleDate,KcMaxNum,KcMinNum," \
                                        "SellCount1,SellCount2,SellCount3,SellDays,StockDays,SellCount) VALUES (%s,%s,%s," \
                                        "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                            self.public_obj.commitmanyFun(objs, insertSQL)
                            sql = "INSERT INTO t_product_puyuan_op_history(sku,status,kc_status,Op_time,deal_time) VALUES (%s,%s,'4',%s,'{0}')".format(this_datetime.now())
                            self.public_obj.commitmanyFun(OPobjs, sql)

                            SynTables_obj = SynTables()
                            SynTables_obj.Syn_LoadInStoreInfo(GoodsSKUIDs)
                        except MySQLdb.Error, e:
                            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                        else:
                            self.deleteOP(ids)
                            self.setStatus()
                            print "结束更新{0}".format("KC_CurrentStock")
        else:
            print "依赖任务未完成，等待中。。。"

    def deleteOP(self, ids):
        i = 0
        sql = "delete from t_product_puyuan_op where id in (%s)"
        while True:
            if len(ids) > maxnumFetchone:
                while True:
                    ids_tmp = ids[:maxnumFetchone]
                    x = ','.join(['%s'] * len(ids_tmp))
                    try:
                        updatesql = sql % x
                        self.cursor.execute(updatesql, tuple(ids_tmp))
                        self.cursor.execute('commit')
                    except MySQLdb.Error, e:
                        print "MySQLdb Error %d: %s" % (e.args[0], e.args[1])
                    else:
                        ids = ids[maxnumFetchone:]
                        i += 1
                        print i
                        break

            if len(ids) <= maxnumFetchone:
                while True:
                    x = ','.join(['%s'] * len(ids))
                    try:
                        updatesql = sql % x
                        self.cursor.execute(updatesql, tuple(ids))
                        self.cursor.execute('commit')
                    except MySQLdb.Error, e:
                        print "MySQLdb Error %d: %s" % (e.args[0], e.args[1])
                    else:
                        i += 1
                        print i
                        break
                break
