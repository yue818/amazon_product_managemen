# encoding: utf-8
'''
@author: zhangyu
@contact: 292724306@qq.com
@software: pycharm
@file: wish_processed_order_syn.py
@time: 2018-06-04 15:21
'''
# encoding: utf-8
import requests
import json
# import MySQLdb
from datetime import datetime
from django.db import connection
import logging
from skuapp.table.t_store_configuration_file import t_store_configuration_file
from brick.wish.wish_api_before.token_verification import verb_token
logger = logging.getLogger('sourceDns.webdns.views')

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'hq_db',
#         # 'HOST': 'hequskuapp.mysql.rds.aliyuncs.com',
#         'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
#         'PORT': '3306',
#         'USER': 'by15161458383',
#         'PASSWORD': 'K120Esc1'
#     },
#     'syn': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'py_db',
#         # 'HOST': 'hequskuapp.mysql.rds.aliyuncs.com',
#         'HOST': 'rm-uf6kd5a4wee2n2ze6rw.mysql.rds.aliyuncs.com',
#         'PORT': '3306',
#         'USER': 'by15161458383',
#         'PASSWORD': 'K120Esc1'
#     },
#     'pic': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'pic_db',
#         # 'HOST': 'hequskuapp.mysql.rds.aliyuncs.com',
#         'HOST': 'rm-uf6kd5a4wee2n2ze6rw.mysql.rds.aliyuncs.com',
#         'PORT': '3306',
#         'USER': 'by15161458383',
#         'PASSWORD': 'K120Esc1'
#     }
#
# }


class wish_processed_order():

    def __init__(self):
        # self.my_conn = MySQLdb.Connect(DATABASES['default']['HOST'], DATABASES['default']['USER'],
        #                                DATABASES['default']['PASSWORD'], DATABASES['default']['NAME'], charset='utf8')
        # self.my_cursor = self.my_conn.cursor()
        self.db_conn = connection
        self.cursor = self.db_conn.cursor()

    def getData(self, access_token):
        url = "https://merchant.wish.com/api/v2/order/get-fulfill"
        params = {
            "access_token": access_token,
            "format": "json",
            "limit": "500",
        }
        try:
            r = requests.get(url, params=params, timeout=30)
            info = json.loads(r.text)
            return info
        except:
            return {}

    def get_access_token(self, shopName):
        # shopName = 'Wish-0236'
        sql = "select K, V from t_config_online_amazon where Name = '{}'".format(shopName)
        self.cursor.execute(sql)
        rts = self.cursor.fetchall()
        access_token = ''
        for rt in rts:
            if rt[0] == 'access_token':
                access_token = rt[1]
        return access_token

    def insertDB(self, shopName):
        # shopName = "Wish-0236"
        try:
            auth_info = verb_token(shopName, self.db_conn)
            access_token = auth_info.get('access_token')
            if access_token:
                info = self.getData(access_token)
                if 'code' in info and 'data' in info and info['code'] == 0:
                    objs_tmp = t_store_configuration_file.objects.filter(ShopName_temp=shopName).values('Operators')
                    Operators = objs_tmp[0]['Operators'] if objs_tmp else ''
                    dict_order = {'shopName': shopName, 'updateTime': datetime.now(), 'street_address2': None,
                                  'color': None, 'size': None, 'Operators': Operators, 'phone_number': None, 'last_updated': None
                                  ,'expected_ship_date': None, 'product_id': None, 'buyer_id': None, 'is_combined_order': None,
                                  'variant_id': None, 'requires_delivery_confirmation': None, 'cost': None, 'shipping_cost': None,
                                  'hours_to_fulfill': None, 'sku': None,'order_total':None,'state':None,'days_to_fulfill':None,
                                  'product_name':None,'transaction_id':None,'order_time':None,'order_id':None,'price':None,
                                  'released_to_merchant_time':None,'is_wish_express':None,'product_image_url':None,
                                  'tracking_confirmed':None,'shipping':None,'quantity':None,'city':None,'name':None,'country':None,
                                  'zipcode':None,'street_address1':None}
                    try:
                        truncateSQL = "delete from wish_processed_order where shopName='{}'".format(shopName)
                        self.cursor.execute(truncateSQL)
                        for order in info['data']:
                            for k, v in order['Order'].items():
                                if k == 'ShippingDetail':
                                    for x, y in order['Order']['ShippingDetail'].items():
                                        dict_order[x] = y
                                else:
                                    dict_order[k] = v
                            insertSQL = "INSERT INTO wish_processed_order(shopName,last_updated,expected_ship_date,product_id,buyer_id,is_combined_order," \
                                        "variant_id,requires_delivery_confirmation,cost,shipping_cost,hours_to_fulfill,order_size,sku,order_total," \
                                        "state,days_to_fulfill,product_name,transaction_id,order_time,order_id,price,released_to_merchant_time," \
                                        "is_wish_express,product_image_url,tracking_confirmed,shipping,quantity,phone_number,city,user_name,country," \
                                        "zipcode,street_address1,street_address2,color,updateTime, Operators) VALUE (%(shopName)s,%(last_updated)s,%(expected_ship_date)s,%(product_id)s,%(buyer_id)s," \
                                        "%(is_combined_order)s,%(variant_id)s,%(requires_delivery_confirmation)s,%(cost)s,%(shipping_cost)s," \
                                        "%(hours_to_fulfill)s,%(size)s,%(sku)s,%(order_total)s,%(state)s,%(days_to_fulfill)s,%(product_name)s," \
                                        "%(transaction_id)s,%(order_time)s,%(order_id)s,%(price)s,%(released_to_merchant_time)s,%(is_wish_express)s," \
                                        "%(product_image_url)s,%(tracking_confirmed)s,%(shipping)s,%(quantity)s,%(phone_number)s,%(city)s,%(name)s," \
                                        "%(country)s,%(zipcode)s,%(street_address1)s,%(street_address2)s,%(color)s,%(updateTime)s, %(Operators)s)"
                            self.cursor.execute(insertSQL, dict_order)
                    except Exception, e1:
                        logger.error('order_syn---------------------------------%s' % e1)
                        self.db_conn.rollback()
                        # 数据同步错误
                        return 3
                    else:
                        self.db_conn.commit()
                        return 0
                else:
                    logger.error("error token:{}".format(shopName))
                    # 错误的token
                    return 2
            else:
                # 没有token
                return 1
        except Exception, e:
            logger.error(e)
            return 1

    def closeDB(self):
        if self.cursor:
            self.cursor.close()
        if self.db_conn:
            self.db_conn.close()
# a = wish_processed_order()
# try:
#     a.insertDB()
# except Exception, e:
#     print e
# finally:
#     a.closeDB()
