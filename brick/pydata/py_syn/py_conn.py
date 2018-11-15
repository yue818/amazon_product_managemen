# coding: utf-8
"""
@author: wangzy
@contact: 15205512335
@site:建立普源连接和关闭
@software: PyCharm
@file: py_conn.py
@time: 2018-07-14 10:21
"""
import sys
import pymssql
import ConfigParser

class py_conn():
    def __init__(self):
        self.sqlserver_conn = ''
        self.cf = ConfigParser.ConfigParser()
        self.cf.read("/data/djangostack-1.9.7/apps/django/django_projects/Project/brick/pydata/py_syn/py-conn.conf")
        #self.cf.read("/data/djangostack-1.9.7/apps/django/django_projects/Project/brick/pydata/py_syn/py-conn.conf")
        self.host = self.cf.get("PYCONN", "HOST")
        self.username = self.cf.get("PYCONN", "USERNAME")
        self.password = self.cf.get("PYCONN", "PASSWORD")
        self.database = self.cf.get("PYCONN", "DATABASE")
        self.port = self.cf.get("PYCONN", "PORT")

    def py_conn_database(self):
        result = {'errorcode': 0}
        try:
            self.sqlserver_conn = pymssql.connect(host=self.host, user=self.username, password=self.password,database=self.database,port=self.port, charset='utf8')
            self.sqlserver_cursor = self.sqlserver_conn.cursor()
            result['py_conn'] = self.sqlserver_conn
            result['py_cursor'] = self.sqlserver_cursor
            result['errortext'] = 'conn success'
        except Exception, ex:
            result['py_conn'] = ''
            result['py_cursor'] = ''
            result['errorcode'] = '-1'
            result['errortext'] = 'conn fail'
        return  result

    def py_close_conn_database(self):
        result = {'errorcode': 0}
        try:
            if self.sqlserver_cursor is not None and self.sqlserver_cursor != '':
                self.sqlserver_cursor.close()
            if self.sqlserver_conn is not None and self.sqlserver_conn != '':
                self.sqlserver_conn.close()
            result['errortext'] = 'close success'
        except Exception, ex:
            result['errorcode'] = '-1'
            result['errortext'] = 'close fail'
        return  result

    def py_commit(self):
        result = {'errorcode': 0}
        try:
            if self.sqlserver_cursor is not None and self.sqlserver_cursor != '':
                self.sqlserver_cursor.execute('commit;')
                result['errortext'] = 'commit success'
            else:
                result['errorcode'] = '-1'
                result['errortext'] = 'commit fail'
        except Exception, ex:
            result['errorcode'] = '-1'
            result['errortext'] = 'commit fail'
        return  result

    def py_rollback(self):
        result = {'errorcode': 0}
        try:
            if self.sqlserver_conn is not None and self.sqlserver_conn != '':
                self.sqlserver_conn.rollback()
                result['errortext'] = 'rollback success'
            else:
                result['errorcode'] = '-1'
                result['errortext'] = 'rollback fail'
        except Exception, ex:
            result['errorcode'] = '-1'
            result['errortext'] = 'rollback fail'
        return  result