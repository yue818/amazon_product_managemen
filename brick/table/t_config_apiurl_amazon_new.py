# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_config_apiurl_amazon_new.py
 @time: 2018/8/2 15:24
"""


class t_config_apiurl_amazon_new():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def get_department_fixed(self, root_id, shop_site, group_all):
        cursor = self.db_conn.cursor()
        try:
            sql_department = "select department from t_config_apiurl_amazon_new where site = '%s' and rootid = %s and group_all = '%s' " % (shop_site, root_id, group_all)
            cursor.execute(sql_department)
            department_obj = cursor.fetchone()
            if department_obj and department_obj[0]:
                department_name = department_obj[0]
            else:
                department_name = None
            cursor.close()
            return department_name
        except Exception as e:
            cursor.close()
            print e
            return
