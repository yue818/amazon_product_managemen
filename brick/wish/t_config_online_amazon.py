# -*- coding: utf-8 -*-
import traceback


class t_config_online_amazon():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def getauthByShopName(self, ShopName):
        shocur = self.db_conn.cursor()
        shocur.execute("select IP,`Name`,K,V from t_config_online_amazon  where `Name` = %s ;", (ShopName,))
        t_config_online_amazon_objs = shocur.fetchall()
        shocur.close()
        auth_info = {}
        for t_config_online_amazon_obj in t_config_online_amazon_objs:
            auth_info['IP'] = t_config_online_amazon_obj[0]
            auth_info['ShopName'] = t_config_online_amazon_obj[1]
            k = t_config_online_amazon_obj[2]
            v = t_config_online_amazon_obj[3]
            auth_info[k] = v
        return auth_info

    def getSitebyShopName(self, ShopName):
        result = {}
        try:
            cursor = self.db_conn.cursor()
            sql = "select DISTINCT site from t_config_online_amazon where shop_name = %s; "
            cursor.execute(sql, (ShopName,))
            result['data'] = cursor.fetchall()
            result['code'] = 0
            cursor.close()
            return result
        except Exception, ex:
            result['code'] = -1
            print '%s_%s:%s' % (traceback.print_exc(), Exception, ex)
            return result


# from brick.db import dbconnect
#
# t = t_config_online_amazon(dbconnect.run({})['db_conn'])
# a =  t.getSitebyShopName('AMZ-0017')
# for b in a['data']:
#     print b[0]
#
#
# print a['data']
# print len(a['data'])
