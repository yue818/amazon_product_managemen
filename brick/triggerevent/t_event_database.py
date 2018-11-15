#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@desc:数据一致性事件触发实时进程
@author: dingjun
@software: PyCharm
@file:t_event_class.py
@time: 2018/5/20
@数据一致性事件触发实时进程对象
"""
import sys
import MySQLdb

class t_event_database():
    def __init__(self):
        self.DATABASES = {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'hq_db',
            'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
            'PORT': '3306',
            'USER': 'by15161458383',
            'PASSWORD': 'K120Esc1'
        }
    def run(self):
        DATABASES = self.DATABASES
        try:
            result = {}
            db_conn = MySQLdb.connect(DATABASES['HOST'], DATABASES['USER'], DATABASES['PASSWORD'], DATABASES['NAME'],port=3306,charset='utf8')
            result['db_conn'] = db_conn
            result['errorcode'] = 0
        except MySQLdb.Error, e:
            result['errorcode'] = 26666
            result['errortext'] = "MySQL Error:%s" % str(e)
        except Exception, ex:
            result['errorcode'] = -1
            result['errortext'] = 'Exception = %s ex=%s  __LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)
        return result