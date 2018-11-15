# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: 20181108.py
 @time: 2018/11/8 15:56
"""
import logging.handlers
from mws import Feeds
import time
import datetime
import pymysql as MySQLdb
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
import random

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


class UpdateProductInfo:
    """
    产品信息修改
    """
    def __init__(self):
        pass

    @staticmethod
    def submit_feed(auth_info, data, feed_type):
        submit_feed_public = Feeds(auth_info['AWSAccessKeyId'], auth_info['SecretKey'], auth_info['SellerId'], auth_info['ShopSite'])
        market_place_ids = [auth_info['MarketplaceId']]
        submit_feed_rsp = submit_feed_public.submit_feed(data, feed_type, marketplaceids=market_place_ids)
        submit_feed_rsp_dict = submit_feed_rsp.parsed
        print submit_feed_rsp_dict
        logging.debug('submit_feed_rsp_dict: %s' % str(submit_feed_rsp_dict))
        return submit_feed_rsp_dict

    @staticmethod
    def get_deal_status(auth_info, feed_id):
        """
            获取提交所提交请求的处理状态，当为 '_DONE_' 时表示处理完成，此时方可提交申请获取处理结果信息
        """
        get_status_public = Feeds(auth_info['AWSAccessKeyId'], auth_info['SecretKey'], auth_info['SellerId'], auth_info['ShopSite'])
        get_status_rsp = get_status_public.get_feed_submission_list([feed_id])
        get_status_rsp_dict = get_status_rsp.parsed
        feed_processing_status = get_status_rsp_dict['FeedSubmissionInfo']['FeedProcessingStatus']['value']
        return feed_processing_status

    def get_deal_result(self, auth_info, data):
        """
         获取处理结果信息，设定总共等待31倍time_sleep时长检查请求是否处理完成（本例等待 31*10=310 秒）
        超过等待时长则设为处理超时
        """
        get_result_public = Feeds(auth_info['AWSAccessKeyId'], auth_info['SecretKey'], auth_info['SellerId'], auth_info['ShopSite'])
        feed_id = '91401017843'

        print '\n'
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print 'result id is: %s, now wait for  10 seconds  then check deal status.' % feed_id
        logging.debug('result id is: %s, now wait for  10 seconds  then check deal status.' % feed_id)

        time_sleep = 10
        count = 0
        while count < 5:
            time.sleep(time_sleep)
            time_sleep += time_sleep  # 每次等待时长翻倍（即10,20,40,80,160）
            count += 1
            try:
                feed_processing_status = self.get_deal_status(auth_info, feed_id)
                if feed_processing_status == '_DONE_':
                    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print 'now we can get the result'
                    logging.debug('now we can get the result')
                    feed_result = get_result_public.get_feed_submission_result(feed_id)
                    print 'get result raw'
                    logging.debug('get result raw')
                    response = feed_result._response_dict
                    print 'get result dict'
                    logging.debug('get result dict: %s' % str(response))
                    logging.debug(response)
                    print response
                    return response
                else:
                    print '\n'
                    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print 'processing_status is:%s, we will wait for %s seconds ' %(feed_processing_status,time_sleep)
                    logging.debug('processing_status is:%s, we will wait for %s seconds ' %(feed_processing_status,time_sleep))
            except Exception as e:
                print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print 'error: %s' % e
                logging.error('error: %s' % e)
        else:  # 循环超过5次，即总等待时长超过 31*time_sleep，则计为超时
            print 'Get submit_feed reuslt timeout'
            logging.error('Get submit_feed reuslt timeout')
            return None

    def update_local_db(self, auth_info):
        cursor = self.db_conn.cursor()
        if auth_info['update_type'] == 'load_product':
            for sku in auth_info['product_list']:
                sql = "update %s set quantity = 999, deal_result = 'Success', status = 'Active', updatetime= '%s' where shopname = '%s' and seller_sku = '%s'" \
                      %(auth_info['table_name'], datetime.datetime.now(), auth_info['ShopName'], sku)
                print 'load sql: %s' % sql
                logging.debug('load sql: %s' % sql)
                cursor.execute(sql)
                cursor.execute('commit;')
            cursor.close()
        elif auth_info['update_type'] == 'unload_product':
            for sku in auth_info['product_list']:
                sql = "update %s set quantity = 0 , deal_result = 'Success', status = 'Inactive', updatetime= '%s' where shopname = '%s' and seller_sku = '%s'" \
                      % (auth_info['table_name'], datetime.datetime.now(), auth_info['ShopName'], sku)
                print 'unload sql: %s' % sql
                logging.debug('unload sql: %s' % sql)
                cursor.execute(sql)
                cursor.execute('commit;')
            cursor.close()
        elif auth_info['update_type'] == 'auto_load_product':
            for sku in auth_info['product_list']:
                sql = "update %s set quantity = 999, status = 'Active', updatetime= '%s' where shopname = '%s' and seller_sku = '%s'" \
                      % (auth_info['table_name'], datetime.datetime.now(), auth_info['ShopName'], sku)
                sql_auto = "update  t_amazon_auto_load set deal_result = 'Success', deal_time = '%s' where batch_id = '%s' and shop_name = '%s' and seller_sku = '%s'" \
                           % (datetime.datetime.now(), auth_info['batch_id'], auth_info['ShopName'], sku)
                logging.debug('load sql: %s' % sql)
                logging.debug('load sql_auto: %s' % sql_auto)
                cursor.execute(sql)
                cursor.execute(sql_auto)
                cursor.execute('commit;')
            cursor.close()
        elif auth_info['update_type'] == 'auto_unload_product':
            for sku in auth_info['product_list']:
                sql = "update %s set quantity = 0 , status = 'Inactive', updatetime = '%s' where shopname = '%s' and seller_sku = '%s'" \
                      % (auth_info['table_name'], datetime.datetime.now(), auth_info['ShopName'], sku)
                sql_auto = "update  t_amazon_auto_load set deal_result = 'Success', deal_time = '%s' where batch_id = '%s' and shop_name = '%s' and seller_sku = '%s'" \
                           % (datetime.datetime.now(), auth_info['batch_id'], auth_info['ShopName'], sku)
                logging.debug('unload sql: %s' % sql)
                logging.debug('unload sql_auto: %s' % sql_auto)
                cursor.execute(sql)
                cursor.execute(sql_auto)
                cursor.execute('commit;')
            cursor.close()
        elif auth_info['update_type'] == 'product_price_modify':
                sql = "update %s set price = '%s', sale_price='%s',sale_from_date='%s',sale_end_date='%s' , deal_result = 'Success',  updatetime= '%s' where shopname = '%s' and seller_sku = '%s'" \
                      % (auth_info['table_name'], auth_info['price_info_dic']['standard_price'], auth_info['price_info_dic']['sale_price'], auth_info['price_info_dic']['start_date'], auth_info['price_info_dic']['end_date'],  datetime.datetime.now(), auth_info['ShopName'], auth_info['seller_sku'])
                print 'sql is:%s' % sql
                logging.debug('sql is:%s' % sql)
                cursor.execute(sql)
                cursor.execute('commit;')
        elif auth_info['update_type'] == 'product_price_modify_multi':
            price_info_dic = auth_info['price_info_dic']
            for sku, price in price_info_dic.items():
                sql = "update %s set price = '%s',deal_result = 'Success',  updatetime= '%s' where shopname = '%s' and seller_sku = '%s'" \
                      % (auth_info['table_name'], price, datetime.datetime.now(), auth_info['ShopName'], sku)
                print 'sql is:%s' % sql
                logging.debug('sql is:%s' % sql)
                cursor.execute(sql)
                cursor.execute('commit;')

                sql_log = "update t_amazon_operation_log set deal_result = 1, end_time='%s' where batch_id = '%s' and shop_name = '%s' and seller_sku ='%s'" \
                          % (datetime.datetime.now(), auth_info['batch_id'], auth_info['ShopName'], sku)
                print 'sql_log is:%s' % sql_log
                logging.debug('sql_log is:%s' % sql_log)
                cursor.execute(sql_log)
                cursor.execute('commit;')

        elif auth_info['update_type'] == 'product_image_modify':
            sql = "update %s set image_url = '%s', deal_result = 'Success',  updatetime= '%s' where shopname = '%s' and seller_sku = '%s'" \
                  % (auth_info['table_name'], auth_info['image_info_dic']['pic_url'], datetime.datetime.now(), auth_info['ShopName'], auth_info['seller_sku'])
            print 'sql is:%s' % sql
            logging.debug('sql is:%s' % sql)
            cursor.execute(sql)
            cursor.execute('commit;')
        else:
            print 'other'
            pass

    def update_db_when_error(self, auth_info, error_msg):
        cursor = self.db_conn.cursor()
        error_msg = str(error_msg)
        try:
            if auth_info['update_type'] in ('product_info_modify', 'product_price_modify', 'product_image_modify'):
                sql = "update %s set deal_result = 'Fail', deal_result_info = '%s', updatetime= '%s' where shopname = '%s' and seller_sku = '%s'" \
                      % (auth_info['table_name'], error_msg.replace("'", '`'), datetime.datetime.now(), auth_info['ShopName'], auth_info['seller_sku'])
                print 'sql is:%s' % sql
                cursor.execute(sql)
                cursor.execute('commit;')
            # elif auth_info['update_type'] == 'product_price_modify_multi':
            #     pass
            elif auth_info['update_type'] in ('auto_load_product', 'auto_unload_product'):
                for sku in auth_info['product_list']:
                    sql_auto_fail = "update  t_amazon_auto_load set deal_result = 'Fail', deal_remark ='%s', deal_time = '%s' where batch_id = '%s' and shop_name = '%s' and seller_sku = '%s'" \
                           % (error_msg.replace("'", '`'), datetime.datetime.now(), auth_info['batch_id'], auth_info['ShopName'], sku)
                    logging.debug('sql_auto_fail sql: %s' % sql_auto_fail)
                    cursor.execute(sql_auto_fail)
                    cursor.execute('commit;')
            else:
                for sku in auth_info['product_list']:
                    sql = "update %s set deal_result = 'Fail', deal_result_info = '%s', updatetime= '%s' where shopname = '%s' and seller_sku = '%s'" \
                          % (auth_info['table_name'], error_msg.replace("'", '`'), datetime.datetime.now(), auth_info['ShopName'], sku)
                    print 'error sql: %s' % sql
                    logging.debug('error sql: %s' % sql)
                    cursor.execute(sql)
                    cursor.execute('commit;')
                    if auth_info['update_type'] == 'product_price_modify_multi':
                        sql_log = "update t_amazon_operation_log set deal_result = -1, deal_result_info = '%s', end_time='%s' where batch_id = '%s' and shop_name = '%s' and seller_sku ='%s'" \
                                  % (error_msg.replace("'", '`'), datetime.datetime.now(), auth_info['batch_id'], auth_info['ShopName'], sku)
                        print 'sql_log is:%s' % sql_log
                        logging.debug('sql_log is:%s' % sql_log)
                        cursor.execute(sql_log)
                        cursor.execute('commit;')

        except Exception as e:
            print e
            traceback.print_exc()
            logging.error(traceback.format_exc())
        finally:
            cursor.close()

    def random_code(self):
        # Random Code Info
        Upper = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        Lower = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        Number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        code = []

        for i in range(2):
            code.append(random.choice(Number))

        letter = Upper + Lower

        for i in range(9):
            code.append(random.choice(letter))

        result = ''.join(code)

        return result

    def get_images_new(self, auth_info):
        """
        从t_templet_amazon_wait_upload表取主sku图片信息
        从t_templet_amazon_published_variation取变体sku图片信息
        若有变体则只上传变体图片，若无则上传主体图片
        返回sku图片字典，格式如下
        {'seller_sku':{'main_url':main_image_url, 'other_url1':other_url1,'other_url12:other_url2,……}}

        """
        # OSS Connection Info
        ACCESS_KEY_ID = 'LTAIH6IHuMj6Fq2h'
        ACCESS_KEY_SECRET = 'N5eWsbw8qBkMfPREkgF2JnTsDASelM'
        ENDPOINT_OUT = 'oss-cn-shanghai.aliyuncs.com'
        BUCKETNAME_APIVERSION = 'fancyqube-all-mainsku-pic'

        # Path for Download Images
        LOCAL_PATH = 'C:\inetpub\wwwroot\\'


        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT_OUT, BUCKETNAME_APIVERSION)
        # cursor = db_connect.cursor()
        try:
            # 主体图片信息
            # sql_main = "select seller_sku, image_url from t_online_info_amazon where 	id = %s" % upload_id
            # cursor.execute(sql_main)
            # main_image_info = cursor.fetchone()
            image_path = LOCAL_PATH  # 本地图片根目录
            image_all_dic = {}
            image_each_dic = {}
            if auth_info['image_info_dic']['pic_url']:
                image_oss = auth_info['image_info_dic']['pic_url']
                print 'image_oss is %s' % image_oss
            # if main_image_info[1]:
                image_url = image_oss.split('/', 3)[-1]
                print 'image_url is'
                print image_url
                code = self.random_code()
                image_url_local = code + '.' + image_oss.split('.')[-1]
                bucket.get_object_to_file(image_url, image_path + image_url_local)
                image_each_dic['main_url'] = image_url_local

            image_all_dic[auth_info['seller_sku']] = image_each_dic
            print 'image_all_dic is %s' % str(image_all_dic)
            return image_all_dic
        except Exception as e:
            print e
            traceback.print_exc()
            logging.error('get_image_new: traceback.format_exc():\n%s' % traceback.format_exc())
            return None


    def get_image_xml_new(self, ip, image_info, seller_id):
        print '111111111111111111111111111111111111111111111'
        IMAGE_HEAD_XML = '''<?xml version="1.0" encoding="utf-8" ?>
        <AmazonEnvelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="amznenvelope.xsd">
            <Header>
                <DocumentVersion>1.01</DocumentVersion>
                <MerchantIdentifier>SELLERID</MerchantIdentifier>
            </Header>
            <MessageType>ProductImage</MessageType>'''
        IMAGE_BODY_XML = '''
            <Message>
                <MessageID>MESSAGENUM</MessageID>
                <OperationType>Update</OperationType>
                <ProductImage>
                    <SKU>PRODUCTSKU</SKU>
                    <ImageType>CHANGE_IMAGE_TYPE</ImageType>
                    <ImageLocation>IMAGELOCALTIONURL</ImageLocation>
                </ProductImage>
            </Message>'''
        IMAGE_FEET_XML = '''
        </AmazonEnvelope>'''
        print '2222222222222222222222222222222222222222222222222'
        try:
            num = 1
            image_xml = {}
            print '33333333333333333333333333333333333333'
            for key, value in image_info.items():
                print key
                print value
                print '4444444444444444444444444444444444444'
                for key_child in sorted(value.keys()):
                    print key_child
                    print '555555555555555555555555555555555'
                    if key_child == 'main_url':
                        image_type = 'Main'
                    else:
                        image_type = 'PT' + key_child[-1]
                    image_url = 'http://' + ip + '/' + value[key_child]
                    print 'image_url is'
                    print image_url
                    image_xml[num] = IMAGE_BODY_XML
                    image_xml[num] = image_xml[num].replace('MESSAGENUM', str(num))
                    image_xml[num] = image_xml[num].replace('PRODUCTSKU', key)
                    image_xml[num] = image_xml[num].replace('CHANGE_IMAGE_TYPE', image_type)
                    image_xml[num] = image_xml[num].replace('IMAGELOCALTIONURL', image_url)
                    num += 1
            print 'image_xml is '
            print image_xml
            image_complete_xml = ''
            image_complete_xml += IMAGE_HEAD_XML
            image_complete_xml = image_complete_xml.replace('SELLERID', seller_id)
            for i in image_xml:
                image_complete_xml += image_xml[i]
            image_complete_xml += IMAGE_FEET_XML
            return image_complete_xml
        except Exception as e:
            logging.error('get_image_xml_new: traceback.format_exc():\n%s' % traceback.format_exc())

    def feed_start(self, auth_info):
        """
                '_POST_INVENTORY_AVAILABILITY_DATA_'  => 库存
                '_POST_PRODUCT_PRICING_DATA_'               => 价格
                '_POST_PRODUCT_DATA_'                               => 商品信息
                '_POST_PRODUCT_IMAGE_DATA_'                 => 图片

            处理结果中 MessagesWithError 为0表示处理成功
        """
        try:
            feed_data = auth_info['feed_xml']
            if auth_info['update_type'] in ('load_product', 'unload_product','auto_load_product', 'auto_unload_product'):
                feed_type = '_POST_INVENTORY_AVAILABILITY_DATA_'
            elif auth_info['update_type'] == 'product_info_modify':
                feed_type = '_POST_PRODUCT_DATA_'
            elif auth_info['update_type'] in ('product_price_modify', 'product_price_modify_multi'):
                feed_type = '_POST_PRODUCT_PRICING_DATA_'
            elif auth_info['update_type'] == 'product_image_modify':
                images = self.get_images_new(auth_info)
                image_xml = self.get_image_xml_new(auth_info['IP'], images, auth_info['SellerId'])
                print 'image_xml is :%s' % image_xml
                logging.debug('image_xml is :%s' % image_xml)
                feed_data = image_xml
                feed_type = '_POST_PRODUCT_IMAGE_DATA_'
            else:
                feed_type = ''

            submit_feed_response = ''
            submit_feed_result = self.get_deal_result(auth_info, submit_feed_response)

            if submit_feed_result \
                    and submit_feed_result['Message']['ProcessingReport']['ProcessingSummary']['MessagesWithError']['value'] == '0':
                self.update_local_db(auth_info)
                return 'Success'
            else:
                self.update_db_when_error(auth_info, 'MessagesWithError is not 0 in mws API processing report ')
                return 'Fail'
            # feed_data = auth_info['feed_xml']
            # feed_type = '_POST_INVENTORY_AVAILABILITY_DATA_'
            # submit_feed_response = self.submit_feed(auth_info, feed_data, feed_type)
            # submit_feed_result = self.get_deal_result(auth_info, submit_feed_response)
            # if submit_feed_result \
            #         and submit_feed_result['Message']['ProcessingReport']['ProcessingSummary']['MessagesWithError']['value'] == '0':
            #     self.update_local_db(auth_info)
            #     return 'Success'
            # else:
            #     self.update_db_when_error(auth_info, 'MessagesWithError is not 0 in mws API processing report ')
            #     return 'Fail'
        except Exception, ex:
            print ex
            logging.error('feed_start: traceback.format_exc():\n%s' % traceback.format_exc())
            self.update_db_when_error(auth_info, ex)
            return 'Fail'

auth_info  = {"AWSAccessKeyId": "AKIAIL7AGIDBWJIYXLYA", "ShopName": "AMZ-0033-YJQ-US/PJ", "amazon_upload_id": 15075, "IP": "182.92.66.164", "SecretKey": "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", "SellerId": "A34SE6EB7V1VZJ", "MarketplaceId": "ATVPDKIKX0DER", "ShopSite":"US"}
obj = UpdateProductInfo()
obj.get_deal_result(auth_info, None)



# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: 20181108a.py
 @time: 2018/11/8 16:14
"""
product_list = ['(!$4${4$1802033333333333333333333', '(!$4${4$180201', '(!$4${4$2']
error_list = list()
res = {'Header': {'MerchantIdentifier': {'value': 'A34SE6EB7V1VZJ'}, 'DocumentVersion': {'value': '1.02'}, 'value': '\n\t\t'}, 'Message': {'ProcessingReport': {'Result': [{'AdditionalInfo': {'SKU': {'value': '(!$4${4$1802022222222222'}, 'value': '\n\t\t\t\t\t'}, 'ResultDescription': {'value': "We're unable to complete your request because this SKU is not in the Amazon catalog. If this was a deleted SKU, wait 24 hours before resubmitting it. If you tried to add this SKU to the Amazon catalog before, check your data and correct any errors before resubmitting. "}, 'value': '\n\t\t\t\t', 'ResultMessageCode': {'value': '13013'}, 'MessageID': {'value': '1'}, 'ResultCode': {'value': 'Error'}}, {'AdditionalInfo': {'SKU': {'value': '(!$4${4$180181111111111111111'}, 'value': '\n\t\t\t\t\t'}, 'ResultDescription': {'value': "We're unable to complete your request because this SKU is not in the Amazon catalog. If this was a deleted SKU, wait 24 hours before resubmitting it. If you tried to add this SKU to the Amazon catalog before, check your data and correct any errors before resubmitting. "}, 'value': '\n\t\t\t\t', 'ResultMessageCode': {'value': '13013'}, 'MessageID': {'value': '2'}, 'ResultCode': {'value': 'Error'}}, {'AdditionalInfo': {'SKU': {'value': '(!$4${4$1802033333333333333333333'}, 'value': '\n\t\t\t\t\t'}, 'ResultDescription': {'value': "We're unable to complete your request because this SKU is not in the Amazon catalog. If this was a deleted SKU, wait 24 hours before resubmitting it. If you tried to add this SKU to the Amazon catalog before, check your data and correct any errors before resubmitting. "}, 'value': '\n\t\t\t\t', 'ResultMessageCode': {'value': '13013'}, 'MessageID': {'value': '3'}, 'ResultCode': {'value': 'Error'}}], 'DocumentTransactionID': {'value': '91401017843'}, 'ProcessingSummary': {'MessagesProcessed': {'value': '3'}, 'MessagesWithWarning': {'value': '0'}, 'MessagesSuccessful': {'value': '0'}, 'value': '\n\t\t\t\t', 'MessagesWithError': {'value': '3'}}, 'value': '\n\t\t\t', 'StatusCode': {'value': 'Complete'}}, 'value': '\n\t\t', 'MessageID': {'value': '1'}}, 'noNamespaceSchemaLocation': {'namespace': 'http://www.w3.org/2001/XMLSchema-instance', 'value': 'amzn-envelope.xsd'}, 'MessageType': {'value': 'ProcessingReport'}, 'value': '\n\t'}
res = {'Header': {'MerchantIdentifier': {'value': 'A34SE6EB7V1VZJ'}, 'DocumentVersion': {'value': '1.02'}, 'value': '\n\t\t'}, 'Message': {'ProcessingReport': {'Result': {'AdditionalInfo': {'SKU': {'value': '(!$4${4$1802033333333333333333333'}, 'value': '\n\t\t\t\t\t'}, 'ResultDescription': {'value': "We're unable to complete your request because this SKU is not in the Amazon catalog. If this was a deleted SKU, wait 24 hours before resubmitting it. If you tried to add this SKU to the Amazon catalog before, check your data and correct any errors before resubmitting. "}, 'value': '\n\t\t\t\t', 'ResultMessageCode': {'value': '13013'}, 'MessageID': {'value': '3'}, 'ResultCode': {'value': 'Error'}}, 'DocumentTransactionID': {'value': '91411017843'}, 'ProcessingSummary': {'MessagesProcessed': {'value': '1'}, 'MessagesWithWarning': {'value': '0'}, 'MessagesSuccessful': {'value': '0'}, 'value': '\n\t\t\t\t', 'MessagesWithError': {'value': '1'}}, 'value': '\n\t\t\t', 'StatusCode': {'value': 'Complete'}}, 'value': '\n\t\t', 'MessageID': {'value': '1'}}, 'noNamespaceSchemaLocation': {'namespace': 'http://www.w3.org/2001/XMLSchema-instance', 'value': 'amzn-envelope.xsd'}, 'MessageType': {'value': 'ProcessingReport'}, 'value': '\n\t'}

result_obj = res.get('Message').get('ProcessingReport').get('Result')
if isinstance(result_obj, list):
    for val in result_obj:
        sku = val.get('AdditionalInfo').get('SKU').get('value')
        print sku
        error_list.append(sku)
elif isinstance(result_obj, dict):
    sku = result_obj.get('AdditionalInfo').get('SKU').get('value')
    print sku
    error_list.append(sku)


product_list = list(set(product_list) - set(error_list))
print error_list
print product_list

