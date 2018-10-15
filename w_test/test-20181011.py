# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: test-20181011.py
 @time: 2018/10/11 14:18
"""  
import logging.handlers
from mws import Reports, Products,Finances
import time
import datetime
import pymysql
import traceback
from bs4 import BeautifulSoup
import requests
import logging
import logging.handlers
import platform
import os
import sys
import win32api
import oss2
import chardet

log_day = datetime.datetime.now().strftime("%Y%m%d")
log_file_name = 'fba_refresh_' + log_day + '.log'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(filename)s %(funcName)s:%(lineno)d] %(thread)d %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=log_file_name,
                    filemode='a')

logging.handlers.RotatingFileHandler(log_file_name,
                                     maxBytes=20 * 1024 * 1024,
                                     backupCount=10)

DATABASE = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'hq_db',
    'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
    'PORT': '3306',
    'USER': 'by15161458383',
    'PASSWORD': 'K120Esc1'
}


class GetShippingPrice:
    def __init__(self, auth_info_ship, data_base):
        self.db_conn = pymysql.connect(data_base['HOST'],
                                       data_base['USER'],
                                       data_base['PASSWORD'],
                                       data_base['NAME'])
        self.auth_info = auth_info_ship
        self.product_public = Products(self.auth_info['AWSAccessKeyId'],
                                       self.auth_info['SecretKey'],
                                       self.auth_info['SellerId'],
                                       self.auth_info['ShopSite'])

    def close_db_conn(self):
        try:
            if self.db_conn:
                self.db_conn.close()
        except Exception as ex:
            print ex
            logging.error('class  GetShippingPrice close db connection failed!' )
            logging.error('traceback.format_exc():\n%s' % traceback.format_exc())

    def get_price_info_by_seller_sku(self, seller_sku):
        if isinstance(seller_sku, str):
            seller_sku = [seller_sku]

        try:
            product_info_response = self.product_public.get_competitive_pricing_for_sku(self.auth_info['MarketplaceId'], seller_sku)
            product_info_response_dic = product_info_response._response_dict
        except Exception as e:
            print e
            time.sleep(10)  # 防止超请求限制，重新提交
            product_info_response = self.product_public.get_competitive_pricing_for_sku(self.auth_info['MarketplaceId'], seller_sku)
            product_info_response_dic = product_info_response._response_dict
        return product_info_response_dic

    def get_seller_sku_list(self):
        try:
            cursor = self.db_conn.cursor()

            sql = "select seller_sku, status from %s where shopname = '%s' and refresh_status != 1 and seller_sku in('_((!${:10108','_((!${:10113')" \
                  % (self.auth_info['table_name'], self.auth_info['ShopName'])

            print 'get product sql is: %s' % sql
            logging.debug('get product sql is: %s' % sql)
            cursor.execute(sql)
            seller_sku_obj = cursor.fetchall()
            cursor.close()

            if seller_sku_obj is not None:
                seller_sku_list = list()
                i_count = 0
                for seller_sku in seller_sku_obj:
                    if seller_sku[0] is not None:
                        i_count += 1
                        seller_sku_list.append(seller_sku[0])
                        if i_count % 20 == 0:
                            seller_sku_list = list(set(seller_sku_list))
                            print 'seller_sku_list is: %s' % str(seller_sku_list)
                            logging.debug('seller_sku_list is: %s' % str(seller_sku_list))
                            price_info = self.get_price_info_by_seller_sku(seller_sku_list)
                            logging.debug('product_info is: %s' % str(price_info))
                            self.update_db_by_price_info(price_info)
                            seller_sku_list = []
                print seller_sku_list
                seller_sku_list = list(set(seller_sku_list))
                print 'seller_sku_list is: %s' % str(seller_sku_list)
                logging.debug('seller_sku_list is: %s' % str(seller_sku_list))
                if seller_sku_list:
                    price_info = self.get_price_info_by_seller_sku(seller_sku_list)
                    logging.debug('product_info is: %s' % str(price_info))
                    self.update_db_by_price_info(price_info)
        except Exception as e:
            print e
            logging.debug('----------------------------------shipping_price fail-----------------------------------------------')
            logging.error('traceback.format_exc():\n%s' % traceback.format_exc())

    def update_db_by_price_info(self, price_info):
        resp_obj = price_info.get('GetCompetitivePricingForSKUResult')
        if isinstance(resp_obj, list):
            resp_list = resp_obj
            for resp_each in resp_list:
                print resp_each.get('status').get('value')
                logging.debug('get_price_status is: %s' % resp_each.get('status').get('value'))
                if resp_each.get('status').get('value') == 'Success':
                    sku = resp_each.get('Product').get('Identifiers').get('SKUIdentifier').get('SellerSKU').get('value')
                    if resp_each.get('Product').get('CompetitivePricing').get('CompetitivePrices').get('CompetitivePrice') is not None:
                        ship_price_info = resp_each.get('Product').get('CompetitivePricing').get('CompetitivePrices').get('CompetitivePrice')
                        print ship_price_info
                        if isinstance(ship_price_info, list):
                            ship_price = ship_price_info[0].get('Price').get('Shipping').get('Amount').get('value')
                        else:
                            ship_price = ship_price_info.get('Price').get('Shipping').get('Amount').get('value')
                        # ship_price = resp_each.get('Product').get('CompetitivePricing').get('CompetitivePrices').get('CompetitivePrice').get('Price').get('Shipping').get('Amount').get('value')
                    else:
                        ship_price = 0.00
                    price_sql = "update %s set shipping_price = %s  where shopname = '%s' and seller_sku = '%s'" % (self.auth_info['table_name'], ship_price, self.auth_info['ShopName'], sku)
                    print price_sql
                    logging.debug('price_sql is: %s' % price_sql)
                    self.execute_db(price_sql)
                    rank_list = resp_each.get('Product').get('SalesRankings').get('SalesRank')
                    sale_rank = None
                    if isinstance(rank_list, list):
                        for rank in rank_list:
                            if rank.get('ProductCategoryId').get('value') == 'kitchen_display_on_website':
                                sale_rank = rank.get('Rank').get('value')
                                break
                    else:
                        sale_rank = rank_list.get('Rank').get('value')
                    sale_rank_sql = "update %s set sale_rank = %s  where shopname = '%s' and seller_sku = '%s'" % (self.auth_info['table_name'], sale_rank, self.auth_info['ShopName'], sku)
                    logging.debug('sale_rank_sql is: %s' % sale_rank_sql)
                    self.execute_db(sale_rank_sql)
        elif isinstance(resp_obj, dict):
            resp_dict = resp_obj
            logging.debug('get_price_status is: %s' % resp_dict.get('status').get('value'))
            if resp_dict.get('status').get('value') == 'Success':
                sku = resp_dict.get('Product').get('Identifiers').get('SKUIdentifier').get('SellerSKU').get('value')
                if resp_dict.get('Product').get('CompetitivePricing').get('CompetitivePrices').get('CompetitivePrice') is not None:
                    ship_price = resp_dict.get('Product').get('CompetitivePricing').get('CompetitivePrices').get('CompetitivePrice').get('Price').get('Shipping').get('Amount').get('value')
                else:
                    ship_price = 0.00
                price_sql = "update %s set shipping_price = %s  where shopname = '%s' and seller_sku = '%s'" % (self.auth_info['table_name'], ship_price, self.auth_info['ShopName'], sku)
                print price_sql
                logging.debug('price_sql is: %s' % price_sql)
                self.execute_db(price_sql)
                rank_list = resp_dict.get('Product').get('SalesRankings').get('SalesRank')
                sale_rank = None
                if isinstance(rank_list, list):
                    for rank in rank_list:
                        if rank.get('ProductCategoryId').get('value') == 'kitchen_display_on_website':
                            sale_rank = rank.get('Rank').get('value')
                            break
                else:
                    sale_rank = rank_list.get('Rank').get('value')
                sale_rank_sql = "update %s set sale_rank = %s  where shopname = '%s' and seller_sku = '%s'" % (self.auth_info['table_name'], sale_rank, self.auth_info['ShopName'], sku)
                logging.debug('sale_rank_sql is: %s' % sale_rank_sql)
                self.execute_db(sale_rank_sql)

    def execute_db(self, sql):
        print 'sql is: %s' % sql
        # cursor = self.db_conn.cursor()
        # try:
        #     cursor.execute(sql)
        #     cursor.execute('commit;')
        #     cursor.close()
        # except Exception as e:
        #     cursor.close()
        #     print e
        #     logging.error('traceback.format_exc():\n%s' % traceback.format_exc())


auth_info = {'AWSAccessKeyId': 'AKIAIP5T3XYETWAWHHDA', 'ShopName': 'AMZ-0052-Bohonan-US/PJ', 'SecretKey': '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', 'table_name': 't_online_info_amazon', 'ShopSite': 'US', 'ShopIP': u'118.89.143.150', 'SellerId': 'ARBNA8Y4OL6TV', 'MarketplaceId': 'ATVPDKIKX0DER', 'update_type': 'refresh_ad_data'}
ship_price_obj = GetShippingPrice(auth_info, DATABASE)
ship_price_obj.get_seller_sku_list()
ship_price_obj.close_db_conn()
