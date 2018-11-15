# -*- coding: utf-8 -*-
import traceback


class t_config_amazon_progress_bar():
    def __init__(self,db_conn):
        self.db_conn = db_conn

    def getProgress(self,uuid):
        result = {}
        try:
            cursor = self.db_conn.cursor()
            sql = "select status from t_config_amazon_progress_bar where uuid = %s order by  updatetime desc limit 1"
            cursor.execute(sql, (uuid,))
            result['data'] = cursor.fetchone()
            result['code'] = 0
            cursor.close()
            return result
        except Exception, ex:
            result['code'] = -1
            print '%s_%s:%s' % (traceback.print_exc(), Exception, ex)
            return result

    def insert_into_Progress(self, auth_info, status):
        result = {}
        try:
            cursor = self.db_conn.cursor()
            sql = "insert into t_config_amazon_progress_bar(uuid, ip, shopname, status, syntype) values ('%s', '%s', '%s', '%s', '%s')" \
                    % (auth_info['uuid'], auth_info['ShopIP'], auth_info['ShopName'], status, auth_info['update_type'])
            cursor.execute(sql)
            cursor.execute('commit;')
            result['code'] = 0
            cursor.close()
            return result
        except Exception, ex:
            result['code'] = -1
            print '%s_%s:%s' % (traceback.print_exc(), Exception, ex)
            return result




# from brick.db import dbconnect
# t_config_amazon_progress_bar_obj = t_config_amazon_progress_bar(db_conn=dbconnect.run({})['db_conn'])
# t_config_amazon_progress_bar_obj.insert_into_Progress('6fc56bc8-227e-42db-952b-ad47b4df7f9b')
