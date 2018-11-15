# -*- coding: utf-8 -*-

import traceback


class t_config_site_ebay():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def queryConfigEbay(self,):
        result = {}
        try:
            cursor = self.db_conn.cursor()
            sql = "SELECT siteID,siteName, siteDescription, dispatchTimeMax, siteCurrency FROM t_config_site_ebay;"
            cursor.execute(sql)
            result['data'] = cursor.fetchall()
            result['code'] = 0
            cursor.close()
            return result
        except Exception, ex:
            result['code'] = -1
            print '%s_%s:%s' % (traceback.print_exc(), Exception, ex)
            return result

