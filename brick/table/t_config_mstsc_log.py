# -*- coding:utf-8 -*-

import sys

class t_config_mstsc_log():
    def __init__(self,db_conn):
        self.db_conn = db_conn

    def getdata(self,t_config_mstsc_log_shopname):
        try:
            cursor = self.db_conn.cursor()
            # sql = "SELECT id,QuitReason,FirstName FROM hq_db.t_config_mstsc_log WHERE id in (SELECT max(id) FROM hq_db.t_config_mstsc_log where ShopName = %s)"
            sql = "SELECT id,QuitReason,FirstName FROM hq_db.t_config_mstsc_log WHERE ShopName = '%s' ORDER BY id DESC LIMIT 1"
            cursor.execute(sql,(t_config_mstsc_log_shopname,))
            t_config_mstsc_log_obj = cursor.fetchone()
            cursor.close()
            return t_config_mstsc_log_obj

        except Exception, ex:
            print 'Exception = %s ex=%s  __LINE__=%s' % (Exception, ex, sys._getframe().f_lineno)
            pass
