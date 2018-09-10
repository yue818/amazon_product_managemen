#!/usr/bin/python
# coding: utf-8

# from socket import *
# import win32api
# import sys
# import threading
from bs4 import BeautifulSoup
from mws import Feeds, Products
import json
import time
import pika
import requests
import platform
import logging
import logging.handlers
import os
import oss2
import random
import MySQLdb
import datetime
import traceback

# logging.basicConfig(level=logging.DEBUG,format='%(asctime)s [%(filename)s %(funcName)s:%(lineno)d] %(thread)d %(levelname)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S',filename='amazon_upload_product.log',filemode='a')
# logging.handlers.RotatingFileHandler('C:\\inetpub\\wwwroot\\amazon_upload_product.log', maxBytes=100 * 1024 * 1024, backupCount=100)

log_formatter = logging.Formatter('%(asctime)s [%(filename)s %(funcName)s:%(lineno)d] %(thread)d %(levelname)s %(message)s')
logFile = 'C:\\inetpub\\wwwroot\\amazon_upload_product.log'
my_handler = logging.handlers.RotatingFileHandler(
    logFile,
    mode='a',
    maxBytes=100 * 1024 * 1024,
    backupCount=4,
    encoding=None,
    delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.DEBUG)
logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)
logger.addHandler(my_handler)

# logging.debug('This is debug message')
# logging.info('This is info message')
# logging.warning('This is warning message')
# logging.error('This is error message')

# logging.basicConfig函数各参数:
# filename: 指定日志文件名
# filemode: 和file函数意义相同，指定日志文件的打开模式，'w'或'a'
# format: 指定输出的格式和内容，format可以输出很多有用信息，如上例所示:
# %(levelno)s: 打印日志级别的数值
# %(levelname)s: 打印日志级别名称
# %(pathname)s: 打印当前执行程序的路径，其实就是sys.argv[0]
# %(filename)s: 打印当前执行程序名
# %(funcName)s: 打印日志的当前函数
# %(lineno)d: 打印日志的当前行号
# %(asctime)s: 打印日志的时间
# %(thread)d: 打印线程ID
# %(threadName)s: 打印线程名称
# %(process)d: 打印进程ID
# %(message)s: 打印日志信息
# datefmt: 指定时间格式，同time.strftime()
# level: 设置日志级别，默认为logging.WARNING
# stream: 指定将日志的输出流，可以指定输出到sys.stderr,sys.stdout或者文件，默认输出到sys.stderr，当stream和filename同时指定时，stream被忽略

# Test environment sql connection info
DATABASE = {
    'NAME': 'hq',
    'HOST': '192.168.105.111',
    'PORT': '3306',
    'USER': 'root',
    'PASSWORD': 'root123'
}

# Real environment sql connection info
DATABASES = {
    # 'NAME': 'hq_db_test2',
    'NAME': 'hq_db',
    'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
    'PORT': '3306',
    'USER': 'by15161458383',
    'PASSWORD': 'K120Esc1'
}

# Rabbitmq Connection Info
# RABBITMQ = {
#     # 'hostname': '127.0.0.1',
#     'hostname': '106.14.125.45',
#     'port': 5672,
#     'username': 'admin',
#     'password': 'admin',
#     # 'username': 'guest',
#     # 'password': 'guest',
# }

# Image XML
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

# Random Code Info
Upper = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
Lower = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
Number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# OSS Connection Info
ACCESS_KEY_ID = 'LTAIH6IHuMj6Fq2h'
ACCESS_KEY_SECRET = 'N5eWsbw8qBkMfPREkgF2JnTsDASelM'
ENDPOINT_OUT = 'oss-cn-shanghai.aliyuncs.com'
BUCKETNAME_APIVERSION = 'fancyqube-all-mainsku-pic'

# Path for Download Images
LOCAL_PATH = 'C:\inetpub\wwwroot\\'


class Server():

    def __init__(self):
        RABBITMQ = self.get_rabbitmq_info()
        credentials = pika.PlainCredentials(RABBITMQ['username'], RABBITMQ['password'])
        self.parameters = pika.ConnectionParameters(RABBITMQ['hostname'], RABBITMQ['port'], '/', credentials, socket_timeout=999999)
        self.connection = pika.BlockingConnection(self.parameters)
        self.realIP = self.get_out_ip(self.get_real_url())

    def listen_client(self):
        channel = self.connection.channel()
        queue = self.realIP + '_' + 'amazon_upload_toy'
        channel.queue_declare(queue=queue, durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(self.callback,
                              queue=queue)
        channel.start_consuming()

    def callback(self, ch, method, properties, body):
        start_time = datetime.datetime.now()
        print " [x] Received %r" % (body,)
        logger.debug(" [x] Received %r" % (body,))
        ch.basic_ack(delivery_tag=method.delivery_tag)

        def publish_response(response):
            ch.basic_publish(
                exchange='',
                routing_key=properties.reply_to,
                properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                body=json.dumps(response)
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        while True:
            db_conn = MySQLdb.connect(DATABASES['HOST'], DATABASES['USER'], DATABASES['PASSWORD'], DATABASES['NAME'])
            data = body.split('||')
            logger.debug('Get all data info: %s' % data)
            auth_info = json.loads(data[0])

            amazon_upload_id = auth_info.get('amazon_upload_id', '')
            amazon_upload_result_id = auth_info.get('amazon_upload_result_id', '')
            print 'amazon_upload_id', amazon_upload_id
            logger.debug('amazon_upload_id %s' % amazon_upload_id)
            print 'amazon_upload_result_id', amazon_upload_result_id
            logger.debug('amazon_upload_result_id %s' % amazon_upload_result_id)

            if not auth_info.get('sku'):
                error_mess = 'Can not get product sku for get product images, auth_info: %s' % data[0]
                logger.error(error_mess)
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.update_error_info_to_db(now, error_mess, amazon_upload_id, amazon_upload_result_id, db_conn)
                db_conn.close()
                break
            product_sku = auth_info.get('sku')
            product_xml_data = data[1]

            variation = str(auth_info.get('variation'))
            upcIds = auth_info.get('upcIds')
            seller_sku_list = auth_info.get('seller_sku_list')
            print 'seller_sku_list', seller_sku_list
            logger.debug('seller_sku_list %s' % seller_sku_list)

            try:
                inventory_xml_data = data[2]
            except Exception as e:
                print 'inventory_xml_data error', e
                logger.error('inventory_xml_data error %s' % e)
                inventory_xml_data = None

            try:
                price_xml_data = data[3]
            except Exception as e:
                print 'price_xml_data error', e
                logger.error('price_xml_data error %s' % e)
                price_xml_data = None

            try:
                relationships_xml_data = data[4]
            except Exception as e:
                print 'relationships_xml_data error', e
                logger.error('relationships_xml_data error %s' % e)
                relationships_xml_data = None

            if not auth_info['IP'] == self.realIP:
                # response = {'error': 'This message is not sended to this ip', 'code': 500}
                # publish_response(response)
                error_mess = 'This VPS ip adderss is %s, but get product shop ip is %s' % (self.realIP, auth_info['IP'])
                logger.error(error_mess)
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.update_error_info_to_db(now, error_mess, amazon_upload_id, amazon_upload_result_id, db_conn)
                db_conn.close()
                break

            if variation == '0':
                shop_sku = product_xml_data.split('<SKU>')[1].split('</SKU>')[0]
            else:
                shop_sku = upcIds
            images = self.get_images(product_sku, variation, upcIds, auth_info['ShopName'])
            if not images:
                # response = {'error': 'Can not get images for this product or this system is not windows', 'code': 404}
                # publish_response(response)
                error_mess = 'Can not get images for product_sku: %s ' % product_sku
                logger.error(error_mess)
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.update_error_info_to_db(now, error_mess, amazon_upload_id, amazon_upload_result_id, db_conn)
                db_conn.close()
                break
            else:
                pass

            image_xml = self.get_image_xml(images, shop_sku, auth_info['SellerId'], variation)
            print data

            response = dict()
            all_submit_result = dict()

            product_submit_data = self.submitfeed(auth_info, product_xml_data, '_POST_PRODUCT_DATA_')
            print('product_submit_data: %s' % product_submit_data)
            logger.debug('product_submit_data: %s' % product_submit_data)
            time.sleep(60)
            product_response_result = self.getsubmitfeedresult(auth_info, product_submit_data)
            if not product_response_result or \
                    not product_response_result['Message']['ProcessingReport']['ProcessingSummary']['MessagesWithError']['value'] == '0':
                logger.error('_POST_PRODUCT_DATA_ error, find reasons to search submitfeed result')
                all_submit_result['_POST_PRODUCT_DATA_'] = product_response_result.get('Message') or 'Get result timeout'
                all_submit_result['_POST_PRODUCT_DATA_'] = str(all_submit_result['_POST_PRODUCT_DATA_']).replace('\"', '\\\"').replace('\'', '\\\'')
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.update_error_info_to_db(now, all_submit_result['_POST_PRODUCT_DATA_'], amazon_upload_id, amazon_upload_result_id, db_conn)
                db_conn.close()
                break
            else:
                response['_POST_PRODUCT_DATA_'] = product_response_result
                all_submit_result['_POST_PRODUCT_DATA_'] = 'all success'
            if inventory_xml_data:
                inventory_submit_data = self.submitfeed(auth_info, inventory_xml_data, '_POST_INVENTORY_AVAILABILITY_DATA_')
                print('inventory_submit_data: %s' % inventory_submit_data)
                logger.debug('inventory_submit_data: %s' % inventory_submit_data)
            if price_xml_data:
                price_submit_data = self.submitfeed(auth_info, price_xml_data, '_POST_PRODUCT_PRICING_DATA_')
                print('price_submit_data: %s' % price_submit_data)
                logger.debug('price_submit_data: %s' % price_submit_data)
            if relationships_xml_data:
                relationships_submit_data = self.submitfeed(auth_info, relationships_xml_data, '_POST_PRODUCT_RELATIONSHIP_DATA_')
                print('relationships_submit_data: %s' % relationships_submit_data)
                logger.debug('relationships_submit_data: %s' % relationships_submit_data)
            image_submit_data = self.submitfeed(auth_info, image_xml, '_POST_PRODUCT_IMAGE_DATA_')
            print('image_submit_data: %s' % image_submit_data)
            logger.debug('submit image xml: %s' % image_xml)
            logger.debug('image_submit_data: %s' % image_submit_data)

            time.sleep(240)

            if inventory_xml_data:
                inventory_response_result = self.getsubmitfeedresult(auth_info, inventory_submit_data)
                response['_POST_INVENTORY_AVAILABILITY_DATA_'] = inventory_response_result
                if inventory_response_result and \
                        inventory_response_result['Message']['ProcessingReport']['ProcessingSummary']['MessagesWithError']['value'] == '0':
                    all_submit_result['_POST_INVENTORY_AVAILABILITY_DATA_'] = 'all success'
                else:
                    all_submit_result['_POST_INVENTORY_AVAILABILITY_DATA_'] = inventory_response_result.get('Message') or 'Get result timeout'
            if price_xml_data:
                price_response_result = self.getsubmitfeedresult(auth_info, price_submit_data)
                response['_POST_PRODUCT_PRICING_DATA_'] = price_response_result
                if price_response_result and \
                        price_response_result['Message']['ProcessingReport']['ProcessingSummary']['MessagesWithError']['value'] == '0':
                    all_submit_result['_POST_PRODUCT_PRICING_DATA_'] = 'all success'
                else:
                    all_submit_result['_POST_PRODUCT_PRICING_DATA_'] = price_response_result.get('Message') or 'Get result timeout'
            if relationships_xml_data:
                relationships_response_result = self.getsubmitfeedresult(auth_info, relationships_submit_data)
                response['_POST_PRODUCT_RELATIONSHIP_DATA_'] = relationships_response_result
                if relationships_response_result and \
                        relationships_response_result['Message']['ProcessingReport']['ProcessingSummary']['MessagesWithError']['value'] == '0':
                    all_submit_result['_POST_PRODUCT_RELATIONSHIP_DATA_'] = 'all success'
                else:
                    all_submit_result['_POST_PRODUCT_RELATIONSHIP_DATA_'] = relationships_response_result.get('Message') or 'Get result timeout'
            image_response_result = self.getsubmitfeedresult(auth_info, image_submit_data)
            response['_POST_PRODUCT_IMAGE_DATA_'] = image_response_result
            if image_response_result and \
                    image_response_result['Message']['ProcessingReport']['ProcessingSummary']['MessagesWithError']['value'] == '0':
                all_submit_result['_POST_PRODUCT_IMAGE_DATA_'] = 'all success'
            else:
                all_submit_result['_POST_PRODUCT_IMAGE_DATA_'] = image_response_result.get('Message') or 'Get result timeout'

            errorMessages = []
            for i in all_submit_result:
                if not all_submit_result[i] == 'all success':
                    errorMessages.append(json.dumps(all_submit_result[i]))

            print 'Start to update amazon upload result db info'
            logger.debug('Start to update amazon upload result db info')
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if not errorMessages:
                sql = "UPDATE t_templet_amazon_upload_result SET updateTime='%s', status='%s', errorMessages='%s' " \
                    "WHERE id='%s';" % (now, 'SUCCESS', '', amazon_upload_result_id)
                self.write_result_to_db(sql, db_conn)
                self.refresh_data_by_seller_sku(auth_info, seller_sku_list, db_conn)
            else:
                error_mess = ','.join(errorMessages)
                error_mess = error_mess.replace('\"', '\\\"').replace('\'', '\\\'')
                self.update_error_info_to_db(now, error_mess, amazon_upload_id, amazon_upload_result_id, db_conn)
            db_conn.close()
            print 'End to update amazon upload result db info'
            logger.debug('End to update amazon upload result db info')

            # TODO callback function
            # print 'properties.correlation_id: ', properties.correlation_id
            # publish_response(response)

            break
        end_time = datetime.datetime.now()
        handle_time = start_time - end_time
        if handle_time.total_seconds() > 120.0:
            pass
        else:
            time.sleep(120)

    def update_error_info_to_db(self, updatetime, error_mess, amazon_upload_id, amazon_upload_result_id, db_conn):
        sql = "UPDATE t_templet_amazon_upload_result SET updateTime='%s', status='%s', errorMessages='%s' " \
            "WHERE id=%s;" % (updatetime, 'FAILED', error_mess, amazon_upload_result_id)
        self.write_result_to_db(sql, db_conn)
        sql_wait = "UPDATE t_templet_amazon_wait_upload SET status='FAILED' WHERE id=%s;" % amazon_upload_id
        self.write_result_to_db(sql_wait, db_conn)

    def get_out_ip(self, url):
        r = requests.get(url)
        txt = r.text
        ip = txt[txt.find("[") + 1: txt.find("]")]
        print('ip:' + ip)

        return ip

    def get_real_url(self, url=r'http://www.ip138.com/'):
        r = requests.get(url)
        txt = r.text
        soup = BeautifulSoup(txt, "html.parser").iframe
        return soup["src"]

    def isWindowsSystem(self):
        return 'Windows' in platform.system()

    def get_image_xml(self, images, shop_sku, sellerid, variation):
        image_xml = {}
        count = 1

        for i in images:
            image_url = 'http://' + self.realIP + '/' + images[i]
            image_num = i.split('.')[0].split('_')
            if variation == '0' and len(image_num) < 2:
                num = 'Main'
            elif not variation == '0' and len(image_num) == 2:
                num = 'Main'
            else:
                num = 'PT' + image_num[-1]
            c = str(count)
            image_xml[c] = IMAGE_BODY_XML
            image_xml[c] = image_xml[c].replace('MESSAGENUM', c)
            image_xml[c] = image_xml[c].replace('IMAGELOCALTIONURL', image_url)
            image_xml[c] = image_xml[c].replace('CHANGE_IMAGE_TYPE', num)
            if variation == '0':
                image_xml[c] = image_xml[c].replace('PRODUCTSKU', shop_sku)
            else:
                pro_son_sku = i.split('.')[0].split('_')[1]
                try:
                    s_sku = shop_sku[pro_son_sku]
                    image_xml[c] = image_xml[c].replace('PRODUCTSKU', s_sku)
                except Exception as e:
                    logger.error('image xml replace error: %s' % e)
                    image_xml.pop(c)
                    continue

                # s_sku = i.split('.')[0].split('_')[1]
                # try:
                #     image_xml[c] = image_xml[c].replace('PRODUCTSKU', s_sku)
                # except Exception as e:
                #     logger.error('image xml replace error: %s' % e)
                #     image_xml.pop(c)
                #     continue
            count += 1

        image_complete_xml = ''
        image_complete_xml += IMAGE_HEAD_XML
        image_complete_xml = image_complete_xml.replace('SELLERID', sellerid)

        for i in image_xml:
            image_complete_xml += image_xml[i]

        image_complete_xml += IMAGE_FEET_XML

        return image_complete_xml

    def get_images(self, product_sku, variation, upcIds, shopname):
        if self.isWindowsSystem():
            shopnames = shopname.split('-')
            last_filename = shopnames[0] + '-' + shopnames[1] + '-' + shopnames[-1].split('/')[0]
            perfix = product_sku + '/Amazon/' + last_filename + '/'
            # perfix = product_sku + '/Amazon/'
            auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
            bucket = oss2.Bucket(auth, ENDPOINT_OUT, BUCKETNAME_APIVERSION)
            image_dict = {}
            for filename2 in oss2.ObjectIterator(bucket, prefix=perfix):
                if product_sku in filename2.key:
                    if variation == '1' and upcIds:
                        for i in upcIds:
                            # if upcIds[i] in filename2.key:
                            if i in filename2.key:
                                print filename2
                                print type(filename2)
                                print filename2.key
                                pid = os.getpid()
                                print pid
                                serverfile = filename2.key.split('/')[-1]
                                code = self.random_code()
                                localfile = code + '.' + serverfile.split('.')[-1]
                                bucket.get_object_to_file(filename2.key, localfile)
                                image_dict[serverfile] = localfile
                    elif variation == '0':
                        if len(filename2.key.split('_')) == 1 or len(filename2.key.split('.')[0].split('_')[1]) < 2:
                            print filename2
                            print type(filename2)
                            print filename2.key
                            pid = os.getpid()
                            print pid
                            serverfile = filename2.key.split('/')[-1]
                            code = self.random_code()
                            localfile = code + '.' + serverfile.split('.')[-1]
                            bucket.get_object_to_file(filename2.key, localfile)
                            image_dict[serverfile] = localfile
                    else:
                        continue

            for i in image_dict.keys():
                if not os.path.exists((LOCAL_PATH + image_dict[i])):
                    image_dict.pop(i)

            return image_dict
        else:
            return None

    def submitfeed(self, auth_info, data, feed_type):
        region = auth_info['ShopName'].split('/')[0].split('-')[-1]
        submitfeed = Feeds(auth_info['AWSAccessKeyId'], auth_info['SecretKey'], auth_info['SellerId'], region=region)
        marketplaceids = [auth_info['MarketplaceId']]
        submitfeed_rsp = submitfeed.submit_feed(data, feed_type, marketplaceids=marketplaceids)
        submitfeed_rsp_dict = submitfeed_rsp.parsed
        return submitfeed_rsp_dict

    def getsubmitfeedresult(self, auth_info, data):
        '''
        _POST_PRODUCT_DATA_:
            {
                'Header': {
                    'MerchantIdentifier': {
                        'value': 'A3E57KPT99E29C'
                    },
                    'DocumentVersion': {'value': '1.02'},
                    'value': '\n\t\t'
                },
                'Message': {
                    'ProcessingReport': {
                        'DocumentTransactionID': {'value': '57844017533'},
                        'ProcessingSummary': {
                            'MessagesProcessed': {'value': '4'},
                            'MessagesWithWarning': {'value': '0'},
                            'MessagesSuccessful': {'value': '4'},
                            'value': '\n\t\t\t\t',
                            'MessagesWithError': {'value': '0'}
                        },
                        'value': '\n\t\t\t',
                        'StatusCode': {'value': 'Complete'}
                    },
                    'value': '\n\t\t',
                    'MessageID': {'value': '1'}
                },
                'noNamespaceSchemaLocation': {
                    'namespace': 'http://www.w3.org/2001/XMLSchema-instance',
                    'value': 'amzn-envelope.xsd'
                },
                'MessageType': {'value': 'ProcessingReport'},
                'value': '\n\t'
            }
        '''
        time.sleep(60)
        region = auth_info['ShopName'].split('/')[0].split('-')[-1]
        submitfeed = Feeds(auth_info['AWSAccessKeyId'], auth_info['SecretKey'], auth_info['SellerId'], region=region)
        feedid = data['FeedSubmissionInfo']['FeedSubmissionId']['value']
        time_sleep = 10
        count = 0
        while True:
            time.sleep(time_sleep)
            time_sleep += time_sleep
            count += 1
            try:
                feedresult = submitfeed.get_feed_submission_result(feedid)
                response = feedresult._response_dict
                if response.get('Message') and \
                        response.get('Message').get('ProcessingReport') and \
                        response.get('Message').get('ProcessingReport').get('StatusCode') and \
                        response.get('Message').get('ProcessingReport').get('StatusCode').get('value'):
                    logger.debug('Get submitfeed result: %s' % response)
                    return response
                # else:
                #     logger.debug('Have got submitfeed result but not complete: %s' % response)
            except Exception as e:
                print 'error: %s' % e
                logger.error('error: %s' % e)
            if count < 7:
                continue
            else:
                # return {'error': 'Get submitfeed reuslt timeout', 'code': 408}
                return {}

    def random_code(self):
        code = []

        for i in range(2):
            code.append(random.choice(Number))

        letter = Upper + Lower

        for i in range(9):
            code.append(random.choice(letter))

        result = ''.join(code)

        return result

    def execute_db(self, sql, db_conn):
        cursor = db_conn.cursor()
        cursor.execute(sql)
        columns = cursor.description
        result = []
        for value in cursor.fetchall():
            tmp = {}
            for (index, column) in enumerate(value):
                tmp[columns[index][0]] = column
            result.append(tmp)

        cursor.close()
        return result

    def write_result_to_db(self, sql, db_conn):
        cursor = db_conn.cursor()
        try:
            print 'write_result_to_db sql: ', sql
            logger.debug('write_result_to_db sql: %s' % sql)
            cursor.execute(sql)
            cursor.execute('commit;')
        except Exception as e:
            logger.error('Update product info faild, Execute sql: %s, Error info: %s' % (sql, e))
        cursor.close()

    def get_product_info_by_seller_sku(self, auth_info, seller_sku_list):
        region = auth_info['ShopName'].split('/')[0].split('-')[-1]
        product_public = Products(auth_info['AWSAccessKeyId'],
                                  auth_info['SecretKey'],
                                  auth_info['SellerId'],
                                  region=region)
        try:
            product_info_response = product_public.get_matching_product_for_id(auth_info['MarketplaceId'], 'SellerSKU', seller_sku_list)
            product_info_response_dic = product_info_response._response_dict
        except Exception as e:
            print e
            time.sleep(2)  # 防止超请求限制，重新提交
            product_info_response = product_public.get_matching_product_for_id(auth_info['MarketplaceId'], 'SellerSKU', seller_sku_list)
            product_info_response_dic = product_info_response._response_dict
        return product_info_response_dic

    def refresh_data_by_seller_sku(self, auth_info, seller_sku_list, db_conn):
        for seller_sku in seller_sku_list:
            product_info = self.get_product_info_by_seller_sku(auth_info, seller_sku_list)
            print product_info
            product_result = product_info['GetMatchingProductForIdResult']
            product_asin = product_result['Products']['Product']['Identifiers']['MarketplaceASIN']['ASIN']['value']
            product_infos = product_result['Products']['Product']['AttributeSets']['ItemAttributes']
            # Publisher = product_infos['Publisher']['value']
            item_name = product_infos['Title']['value']
            if 'ListPrice' in product_infos.keys():
                price = product_infos['ListPrice']['Amount']['value']
                # currency = product_infos['ListPrice']['CurrencyCode']['value']
            else:
                price = None
            # brand = product_infos['Brand']['value']
            image_url = product_infos['SmallImage']['URL']['value']
            # Manufacturer = product_infos['Manufacturer']['value']

            sql = "INSERT INTO t_online_info_amazon(seller_sku, asin1, item_name, price, image_url, ShopName, shopsite) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                  % (seller_sku, product_asin, item_name, price, image_url, auth_info['ShopName'], auth_info['ShopName'].split('-')[-1].split('/')[0])
            self.write_result_to_db(sql, db_conn)

    def get_rabbitmq_info(self):
        db_conn = MySQLdb.connect(DATABASES['HOST'], DATABASES['USER'], DATABASES['PASSWORD'], DATABASES['NAME'])
        sql = "SELECT IP, K, V FROM t_config_mq_info WHERE Name='Amazon-RabbitMQ-Server' AND PlatformName='Amazon';"
        res = self.execute_db(sql, db_conn)
        RABBITMQ = dict()
        for i in res:
            if i.get('K') == 'MQPort':
                RABBITMQ['port'] = i.get('V')
            elif i.get('K') == 'MQUser':
                RABBITMQ['username'] = i.get('V')
            elif i.get('K') == 'MQPassword':
                RABBITMQ['password'] = i.get('V')
            else:
                pass
            RABBITMQ['hostname'] = i.get('IP')
        db_conn.close()
        return RABBITMQ


def retry_server():
    try:
        c = Server()
        c.listen_client()
    except Exception as e:
        print 'Define server error', e
        print 'traceback.format_exc():\n%s' % traceback.format_exc()
        logger.error('Define server error %s' % e)
        logger.error('traceback.format_exc():\n%s' % traceback.format_exc())
        time.sleep(5)
        retry_server()


if __name__ == '__main__':
    # daemonize('/dev/null','/opt/codelib/amazon_api/publish_product_stdout.log','/opt/codelib/amazon_api/publish_product_stderr.log')

    retry_server()
    # c = Server()
    # c.listen_client()
