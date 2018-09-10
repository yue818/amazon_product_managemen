# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: get_auth_info.py
 @time: 2018-02-11 14:50
"""  

# auth_info_0052 = {'AWSAccessKeyId': 'AKIAIP5T3XYETWAWHHDA',
#              'SecretKey':'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',
#              'SellerId':'ARBNA8Y4OL6TV',
#              'MarketplaceId':'ATVPDKIKX0DER',
#              'ShopIP':'118.89.143.150',
#              'ShopName':'AMZ-0052-Bohonan-US/PJ',
#              'table_name': 'GET_MERCHANT_LISTINGS_ALL_DATA',
#              'update_type': 'refresh_product', #  refresh_shop, refresh_product, load_product, unload_product
#              'product_list': ['BOHA0230','BOHA0239', '01-D25B-YA35'] }


class GetAuthInfo:
    def __init__(self, db_connection, ):
        self.db_connection = db_connection

    def get_name_by_shop_and_site(self, shop_name, site):
        cursor = self.db_connection.cursor()
        sql = "select DISTINCT name from t_config_online_amazon where shop_name = '%s' and site = '%s'" \
              %(shop_name, site)
        cursor.execute(sql)
        name_info = cursor.fetchone()
        cursor.close()
        return name_info[0]

    def get_auth_info_by_shop_name(self, shop_name):
        auth_info = {}
        cursor = self.db_connection.cursor()
        sql_site = "select site from t_config_online_amazon  where name= '%s' limit 1" % shop_name
        print sql_site
        cursor.execute(sql_site)
        auth_info['ShopSite'] = cursor.fetchone()[0]

        sql = "select IP,Name,K,V from t_config_online_amazon  where name= '%s'" % shop_name
        cursor.execute(sql)
        shop_config_info = cursor.fetchall()
        print shop_config_info
        cursor.close()
        auth_info['ShopName'] = shop_name
        for shop_config_info_obj in shop_config_info:
            auth_info['ShopIP'] = shop_config_info_obj[0]
            k = shop_config_info_obj[2]
            v = shop_config_info_obj[3]
            auth_info[k] = v
        return auth_info


