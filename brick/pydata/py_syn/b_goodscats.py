# encoding: utf-8
"""
@author: ZhangYu
@contact: 292724306@qq.com
@site: 
@software: PyCharm
@file: b_goodscats.py
@time: 2017-12-21 14:28
"""
import logging
import MySQLdb
import pymssql

# 联表查询商品种类名称
class b_goodscats:
    def __init__(self, db_conn, sqlserver_conn=None):
        self.db_conn = db_conn
        self.sqlserver_conn = sqlserver_conn
        self.cursor = self.db_conn.cursor()

    def selectCategoryName(self, Category3):
        sql = "select CategoryName from py_db.b_goodscats b where b.CategoryCode=CONCAT(substring_index('%s','|',2),'|')" % Category3
        self.cursor.execute(sql)
        CategoryName = self.cursor.fetchone()
        if CategoryName:
            return CategoryName
        else:
            return ''
