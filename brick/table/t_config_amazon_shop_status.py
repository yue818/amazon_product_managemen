# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_config_amazon_shop_status.py
 @time: 2018-02-26 10:57
"""  
# import traceback
import datetime

class t_config_amazon_shop_status:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def update_shop_status(self, auth_info, shop_name, status):
        cursor = self.db_conn.cursor()
        sql_record_exists = "select  name from t_config_amazon_shop_status where name = '%s'" % auth_info['ShopName']
        cursor.execute(sql_record_exists)
        shop_exists_obj = cursor.fetchone()
        print '-----------------------------------------------------------------------------------'
        #print shop_exists_obj[0]
        if shop_exists_obj is None or shop_exists_obj[0] is None :
            sql_insert = "insert into t_config_amazon_shop_status (name,shop_name,shop_site,IP,uuid,synType,status) " \
                         "values ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                         %(auth_info['ShopName'], shop_name, auth_info['ShopSite'], auth_info['ShopIP'], auth_info['uuid'], auth_info['update_type'],status)
            cursor.execute(sql_insert)
            cursor.execute('commit;')
        else:
            sql_update = "update t_config_amazon_shop_status set uuid = '%s', synType = '%s', status = '%s' where name = '%s'" \
                         %(auth_info['uuid'], auth_info['update_type'], status, auth_info['ShopName'])
            cursor.execute(sql_update)
            cursor.execute('commit;')
        cursor.close()

    def get_shop_status(self, shop_name):
        cursor = self.db_conn.cursor()
        sql_all = "select shop_site, syntype, status, updatetime from t_config_amazon_shop_status where shop_name = '%s'" % shop_name
        cursor.execute(sql_all)
        status_all_obj = cursor.fetchall()
        remark_all = ''
        for status_every in status_all_obj:
            if status_every[0] == 'CN':
                site_cn = '中国'
            elif status_every[0] == 'US':
                site_cn = '美国'
            elif status_every[0] == 'DE':
                site_cn = '德国'
            elif status_every[0] == 'FR':
                site_cn = '法国'
            elif status_every[0] == 'UK':
                site_cn = '英国'
            elif status_every[0] == 'CA':
                site_cn = '加拿大'
            elif status_every[0] == 'JP':
                site_cn = '日本'
            else:
                site_cn = status_every[0]

            if status_every[1] == 'refresh_shop_increment':
                refresh_type = '增量'
            elif status_every[1] == 'refresh_shop_all':
                refresh_type = '全量'
            else:
                refresh_type = status_every[1]
            remark_loop = ''
            if status_every[2] == 'success':
                remark_loop = site_cn + '站最近一次' + refresh_type + '更新时间为：' + str(status_every[3])
            elif status_every[2] == 'process':
                finish_time = status_every[3] + datetime.timedelta(minutes=6)
                remark_loop = site_cn + '站正在进行' + refresh_type + '更新! 预计完成时间为：' + str(finish_time)

            remark_all = remark_all + remark_loop + ';'
        return remark_all[:-1]
