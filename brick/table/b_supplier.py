# encoding: utf-8
"""
@author: ZhangYu
@contact: 292724306@qq.com
@site: 
@software: PyCharm
@file: b_supplier.py
@time: 2017-12-21 15:21
"""
#联表查询供应商名称
class b_supplier():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def selectSupplierName(self, SupplierID):
        cursor = self.db_conn.cursor()
        sql = "SELECT SupplierName from b_supplier WHERE id=%s"
        cursor.execute(sql,SupplierID)
        SupplierName = cursor.fetchone()
        cursor.close()
        if SupplierName:
            return SupplierName
        else:
            return ''

    def GetSupplierStatus(self, SupplierName):
        cursor = self.db_conn.cursor()
        sql = "SELECT Used from py_db.b_supplier WHERE SupplierName=%s;"
        cursor.execute(sql, SupplierName)
        obj = cursor.fetchone()
        cursor.close()
        if obj:
            return obj[0]   # 0 正常； 1 停用
        else:
            return None

