# -*- coding:utf-8 -*-
"""
 @desc:
 @author: wuchongxiang
 @site:
 @software: PyCharm
 @file: amazon_refresh_product-20180502.py
 @time: 2018-05-02 13:45
"""
from mws import Reports, Feeds,Products
import time
import datetime
import pymysql as MySQLdb
import traceback
import pika
from bs4 import BeautifulSoup
import requests
import logging
import logging.handlers

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(filename)s %(funcName)s:%(lineno)d] %(thread)d %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='test_image.log',
                    filemode='a')

logging.handlers.RotatingFileHandler('test_image.log',
                                     maxBytes=100 * 1024 * 1024,
                                     backupCount=10)

DATABASE = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hq_db',
        'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
        'PORT': '3306',
        'USER': 'by15161458383',
        'PASSWORD': 'K120Esc1'
            }


class GetProductInfoByAsin:
    """
     按asin值获取产品图片及主、变体关系
    """
    def __init__(self, auth_info):
        self.db_conn = MySQLdb.connect(DATABASE['HOST'],
                                       DATABASE['USER'],
                                       DATABASE['PASSWORD'],
                                       DATABASE['NAME'])
        self.auth_info = auth_info
        self.product_public = Products(self.auth_info['AWSAccessKeyId'],
                                       self.auth_info['SecretKey'],
                                       self.auth_info['SellerId'],
                                       self.auth_info['ShopSite']
                                       )

    def get_product_info(self, asin_list):
        try:
            product_info_response = self.product_public.get_matching_product(self.auth_info['MarketplaceId'], asin_list)
            product_info_response_dic = product_info_response._response_dict
        except Exception as e:
            logging.error(e)
            time.sleep(10)  # 防止超请求限制，重新提交
            product_info_response = self.product_public.get_matching_product(self.auth_info['MarketplaceId'], asin_list)
            product_info_response_dic = product_info_response._response_dict
        return product_info_response_dic

    def update_parent_asin(self, main_asin, child_asin):
        cursor = self.db_conn.cursor()
        sql = "update %s set parent_asin = '%s' where asin1 = '%s' and shopname = '%s'" \
              % (self.auth_info['table_name'], main_asin, child_asin, self.auth_info['ShopName'])
        print 'update_parent_asin sql is: %s' % sql
        logging.debug('update_parent_asin sql is: %s' % sql)
        cursor.execute(sql)
        cursor.execute('commit;')
        cursor.close()

    def connect_image(self, asin, image_url):
        cursor = self.db_conn.cursor()
        sql = "update %s set image_url = '%s' where asin1 = '%s' and shopname = '%s'" \
              % (self.auth_info['table_name'], image_url, asin, self.auth_info['ShopName'])
        print 'connect_image sql is: %s' % sql
        logging.debug( 'connect_image sql is: %s' % sql)
        cursor.execute(sql)
        cursor.execute('commit;')
        cursor.close()

    def deal_worker(self, product):
        main_asin = product['ASIN']['value']
        print 'main_asin is: %s' % main_asin
        logging.debug('main_asin is: %s' % main_asin)
        try:
            image_url = product['Product']['AttributeSets']['SmallImage']['URL']['value']
        except Exception as e:
            print e
            image_url = product['Product']['AttributeSets']['ItemAttributes']['SmallImage']['URL']['value']
        print 'image_url is: %s' % image_url
        logging.debug('image_url is: %s' % image_url)

        # parent -> child
        if product['Product']['Relationships'].has_key('VariationChild'):
            print product['Product']['Relationships']

            child_list = product['Product']['Relationships']['VariationChild']  # 多个变体时为列表,单个变体时为字典
            if isinstance(child_list, list):  # 多个变体
                for child in child_list:
                    child_asin = child['Identifiers']['MarketplaceASIN']['ASIN']['value']
                    print ' child_asin is: %s' % child_asin
                    logging.debug('child_asin is: %s' % child_asin)
                    self.update_parent_asin(main_asin, child_asin)
            else:  # 单个变体
                child_asin = child_list['Identifiers']['MarketplaceASIN']['ASIN']['value']
                print ' child_asin is: %s' % child_asin
                logging.debug('child_asin is: %s' % child_asin)
                self.update_parent_asin(main_asin, child_asin)

        # child -> parent
        if product['Product']['Relationships'].has_key('VariationParent'):
            parent_asin = product['Product']['Relationships']['VariationParent']['Identifiers']['MarketplaceASIN']['ASIN']['value']
            print 'parent_asin is: %s' % parent_asin
            logging.debug('parent_asin is: %s' % parent_asin)
            self.update_parent_asin(parent_asin, main_asin)

        self.connect_image(main_asin, image_url)

    def update_db_by_product_info(self, product_info):
        product_list = product_info['GetMatchingProductResult']  # 提交多个asin时为列表，单个时为字典
        if isinstance(product_list, list):
            for product in product_list:
                try:
                    self.deal_worker(product)
                except Exception as e:
                    print 'exception product is：%s' % str(product)
                    logging.debug('exception product is：%s' % str(product))
                    logging.error('traceback.format_exc():\n%s' % traceback.format_exc())
                    print e
                    continue
        else:
            try:
                self.deal_worker(product_list)
            except Exception as e:
                logging.debug('exception product list is：%s' % str(product_list))
                logging.error('traceback.format_exc():\n%s' % traceback.format_exc())
                print 'exception product is：%s' % str(product_list)
                print e

    def refresh_product(self):
        cursor = self.db_conn.cursor()
        sql_product_parent = "update %s set parent_asin = asin1 where status = 'Incomplete' and shopname = '%s'" \
                             % (self.auth_info['table_name'], self.auth_info['ShopName'])
        sql_product_multiple = "update %s set product_type = 1 where parent_asin is not null and shopname = '%s'" \
                               % (self.auth_info['table_name'], self.auth_info['ShopName'])
        print 'sql_product_parent: %s' % sql_product_parent
        logging.debug('sql_product_parent: %s' % sql_product_parent)
        cursor.execute(sql_product_parent)
        cursor.execute('commit;')
        print 'sql_product_multiple: %s' % sql_product_multiple
        logging.debug('sql_product_multiple: %s' % sql_product_multiple)
        cursor.execute(sql_product_multiple)
        cursor.execute('commit;')
        cursor.close()

    def get_parent_asin_and_image(self, seller_sku_list=None):
        cursor = self.db_conn.cursor()
        if seller_sku_list is None:
            sql = "select asin1,seller_sku, status from %s where shopname = '%s'" \
                  % (self.auth_info['table_name'], self.auth_info['ShopName'])
        else:
            seller_sku = str(seller_sku_list)
            seller_sku = seller_sku.replace('[u', '')
            seller_sku = seller_sku.replace('[', '')
            seller_sku = seller_sku.replace(']', '')
            seller_sku = seller_sku.replace(", u'", ", '")
            print 'seller_sku is: %s' % seller_sku
            sql = "select asin1, seller_sku, status from %s where shopname = '%s' and seller_sku in (%s)" \
                  % (self.auth_info['table_name'], self.auth_info['ShopName'], seller_sku)
        print 'get product sql is: %s' % sql
        logging.debug('get product sql is: %s' % sql)
        cursor.execute(sql)
        asin_status_obj = cursor.fetchall()
        cursor.close()
        if asin_status_obj is not None:
            asin_list =[]
            i_count = 0
            for asin_status in asin_status_obj:
                if asin_status[0] is not None:
                    i_count += 1
                    asin_list.append(asin_status[0])
                    if i_count % 10 == 0:
                        asin_list = list(set(asin_list))
                        print 'asin_list is: %s' % str(asin_list)
                        logging.debug('asin_list is: %s' % str(asin_list))
                        product_info = self.get_product_info(asin_list)
                        logging.debug('product_info is: %s' % str(product_info))
                        self.update_db_by_product_info(product_info)
                        asin_list = []
                else:
                    print "asin is null, get product info by seller_sku"
                    logging.debug("asin is null, get product info by seller_sku")
                    print "seller_sku is: %s" % asin_status[1]
                    logging.debug("seller_sku is: %s" % asin_status[1])
                    sku_obj = GetProductInfoBySellerSku(self.auth_info,DATABASE)
                    sku_obj.refresh_data_by_seller_sku(asin_status[1])
            print asin_list
            asin_list = list(set(asin_list))
            print 'asin_list is: %s' % str(asin_list)
            logging.debug('asin_list is: %s' % str(asin_list))
            if asin_list:
                product_info = self.get_product_info(asin_list)
                logging.debug('product_info is: %s' % str(product_info))
                self.update_db_by_product_info(product_info)
            self.refresh_product()


class GetProductInfoBySellerSku:
    """
    按seller_sku值获取产品图片及主、变体关系
    """
    def __init__(self, auth_info, DATABASE):
        self.db_conn = MySQLdb.connect(DATABASE['HOST'],
                                       DATABASE['USER'],
                                       DATABASE['PASSWORD'],
                                       DATABASE['NAME'])
        self.auth_info = auth_info
        self.product_public = Products(self.auth_info['AWSAccessKeyId'],
                                       self.auth_info['SecretKey'],
                                       self.auth_info['SellerId'],
                                       self.auth_info['ShopSite'])

    def get_product_info_by_seller_sku(self, seller_sku):
        try:
            product_info_response = self.product_public.get_matching_product_for_id(self.auth_info['MarketplaceId'], 'SellerSKU', [seller_sku])
            product_info_response_dic = product_info_response._response_dict
        except Exception as e:
            print e
            time.sleep(2)  # 防止超请求限制，重新提交
            product_info_response = self.product_public.get_matching_product_for_id(self.auth_info['MarketplaceId'], 'SellerSKU', [seller_sku])
            product_info_response_dic = product_info_response._response_dict
        return product_info_response_dic

    def update_asin(self, this_asin, image_url, seller_sku):
        cursor = self.db_conn.cursor()
        try:
            sql = "update %s set asin1 = '%s' , image_url = '%s' where seller_sku ='%s' and shopname = '%s'" \
                  % (self.auth_info['table_name'], this_asin,  image_url, seller_sku, self.auth_info['ShopName'])
            print 'update_parent_asin sql is: %s' % sql
            logging.debug('update_parent_asin sql is: %s' % sql)
            cursor.execute(sql)
            cursor.execute('commit;')
            cursor.close()
        except Exception as e:
            cursor.close()
            print e
            logging.error('traceback.format_exc():\n%s' % traceback.format_exc())

    def execute_db(self, sql):
        cursor = self.db_conn.cursor()
        try:
            cursor.execute(sql)
            cursor.execute('commit;')
            cursor.close()
        except Exception as e:
            cursor.close()
            print e

    def update_db_by_product_info(self, product_info, seller_sku):
        main_asin = product_info['GetMatchingProductForIdResult']['Products']['Product']['Identifiers']['MarketplaceASIN']['ASIN']['value']
        image_url = product_info['GetMatchingProductForIdResult']['Products']['Product']['AttributeSets']['ItemAttributes']['SmallImage']['URL']['value']
        self.update_asin(main_asin, image_url, seller_sku)

        if product_info['GetMatchingProductForIdResult']['Products']['Product']['Relationships'].has_key('VariationChild'):
            child_list = product_info['GetMatchingProductForIdResult']['Products']['Product']['Relationships']['VariationChild']
            if isinstance(child_list, list):
                for child in child_list:
                    child_asin = child['Identifiers']['MarketplaceASIN']['ASIN']['value']
                    sql_child = "update %s set parent_asin = '%s' where asin1 ='%s' and shopname = '%s'" \
                                % (self.auth_info['table_name'], main_asin, child_asin, self.auth_info['ShopName'])
                    print 'sql_child is: %s' % sql_child
                    logging.debug('sql_child_1 is: %s' % sql_child)
                    self.execute_db(sql_child)
            else:
                child_asin = child_list['Identifiers']['MarketplaceASIN']['ASIN']['value']
                sql_child = "update %s set parent_asin = '%s' where asin1 ='%s' and shopname = '%s'" \
                            % (self.auth_info['table_name'], main_asin, child_asin, self.auth_info['ShopName'])
                print 'sql_child is: %s' % sql_child
                logging.debug('sql_child_2 is: %s' % sql_child)
                self.execute_db(sql_child)

        if product_info['GetMatchingProductForIdResult']['Products']['Product']['Relationships'].has_key('VariationParent'):
            parent_asin = product_info['GetMatchingProductForIdResult']['Products']['Product']['Relationships']['VariationParent']['Identifiers']['MarketplaceASIN']['ASIN']['value']
            sql_parent = "update %s set parent_asin = '%s' where asin1 ='%s' and shopname = '%s'" \
                         % (self.auth_info['table_name'], parent_asin, main_asin, self.auth_info['ShopName'])
            print 'parent_asin is: %s' % parent_asin
            print 'sql_parent is: %s' % sql_parent
            logging.debug('parent_asin is: %s' % parent_asin)
            logging.debug('sql_parent is: %s' % sql_parent)
            self.execute_db(sql_parent)

    def refresh_data_by_seller_sku(self, seller_sku):
        product_info = self.get_product_info_by_seller_sku(seller_sku)
        print "get product_info by seller_sku is: %s " % str(product_info)
        logging.debug("get product_info by seller_sku is: %s " % str(product_info))
        if product_info['GetMatchingProductForIdResult']['status']['value'] == 'Success':
            self.update_db_by_product_info(product_info, seller_sku)
        else:
            print 'get product_info by seller_sku error'
            logging.debug('get product_info by seller_sku error')

auth_info_str = "{'AWSAccessKeyId': 'AKIAI3NT4LW2HPPDT5UA', 'ShopName': 'AMZ-0001-Yonger-FR/PJ', 'uuid': '099a7852-fdb2-459a-b1a0-34d4082fe0b8', 'SecretKey': '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', 'table_name': 't_online_info_amazon', 'ShopSite': 'FR', 'ShopIP': '123.57.63.178', 'SellerId': 'ASJ38YS5SMHCI', 'update_type': 'refresh_shop_all', 'MarketplaceId': 'A13V1IB3VIYZZH'}"
auth_info = eval(auth_info_str)
get_product_info_obj = GetProductInfoByAsin(auth_info)
get_product_info_obj.get_parent_asin_and_image()








