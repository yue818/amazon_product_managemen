# -*- coding:utf-8 -*-

import sys

class t_config_mstsc_user():
    def __init__(self,db_conn):
        self.db_conn = db_conn

    def getdata(self,username):
        try:
            cursor = self.db_conn.cursor()
            sql = "SELECT id,username,cn_name FROM hq_db.t_config_mstsc_user where username = '%s'" % username
            cursor.execute(sql)
            t_config_mstsc_user_obj = cursor.fetchone()
            cursor.close()
            return t_config_mstsc_user_obj
        except Exception, ex:
            print 'Exception = %s ex=%s  __LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)




