# encoding: utf-8
"""
@author: ZhangYu
@contact: 292724306@qq.com
@site: 
@software: PyCharm
@file: gs_compared.py
@time: 2017-12-25 14:26
"""
import MySQLdb


# 联表查询商品状态
class gs_compared:
    def __init__(self, db_conn):
        self.db_conn = db_conn
        self.cursor = self.db_conn.cursor()

    def getPy_status(self, hq_status):
        # hq_status = hq_status[0].encode("utf-8")
        try:
            sql = "select py_GoodsStatus from goodsstatus_compare where hq_GoodsStatus='%s'" % hq_status
            self.cursor.execute(sql)
            py_status = self.cursor.fetchone()
            return py_status
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            return hq_status
