# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: amazon_refresh_product-20180628.py
 @time: 2018-06-28 17:22
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
import platform
import sys
import oss2
import random


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(filename)s %(funcName)s:%(lineno)d] %(thread)d %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='amazon_refresh_product.log',
                    filemode='a')

logging.handlers.RotatingFileHandler('amazon_refresh_product.log',
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


def is_windows_system():
    return 'Windows' in platform.system()


def auto_upgrade():
    if is_windows_system():
        import time
        import os
        import sys
        import win32api
        import oss2
        access_key_id = 'LTAIH6IHuMj6Fq2h'
        access_key_secret = 'N5eWsbw8qBkMfPREkgF2JnTsDASelM'
        endpoint_out = 'oss-cn-shanghai.aliyuncs.com'
        bucket_name_api_version = 'fancyqube-apiversion'
        print 'this file is: %s' % str(sys.argv[0])
        logging.debug('this file is: %s' % str(sys.argv[0]))
        auth = oss2.Auth(access_key_id, access_key_secret)
        bucket = oss2.Bucket(auth, endpoint_out, bucket_name_api_version)
        for filename2 in oss2.ObjectIterator(bucket, prefix='amazon_refresh_product-'):
            if sys.argv[0].split('\\')[-1] < filename2.key:
                print 'The file in oss: %s  is  newer than current file,we will download it and run it.'  % str(filename2.key)
                logging.debug('The file in oss: %s  is  newer than current file,we will download it and run it.'  % str(filename2.key))
                bucket.get_object_to_file(filename2.key,filename2.key)
                if win32api.ShellExecute(0, 'open', filename2.key, '','',3)>32:
                    print 'Run new file and close the current one.'
                    logging.debug('Run new file and close the current one.')
                    os._exit(0)
                else:
                    print 'Download the new file, but can not run it!'
                    logging.error('Download the new file, but can not run it!')
            else:
                print 'The file in oss: %s  is older  than current file,we will ignore it.' % str(filename2.key)
                logging.debug('The file in oss: %s  is older  than current file,we will ignore it.' % str(filename2.key))
    else:
        pass


class GetShopProductInfo:
    """
    产品信息刷新
    """
    def __init__(self, auth_info):
        self.auth_info = auth_info
        self.report_public = Reports(self.auth_info['AWSAccessKeyId'],
                                     self.auth_info['SecretKey'],
                                     self.auth_info['SellerId'],
                                     self.auth_info['ShopSite']
                                     )
        self.db_conn = MySQLdb.connect(DATABASE['HOST'],
                                       DATABASE['USER'],
                                       DATABASE['PASSWORD'],
                                       DATABASE['NAME'])

    def submit_report_request(self, report_type):
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print 'submit'
        logging.debug('submit report, report type is:%s' % report_type)
        market_place_ids = [self.auth_info['MarketplaceId']]

        if self.auth_info['update_type'] == 'refresh_shop_increment':
            start_date = self.get_max_update_time()
            end_date = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        else:
            start_date = None
            end_date = None

        report_response = self.report_public.request_report(report_type,
                                                            start_date=start_date,
                                                            end_date=end_date,
                                                            marketplaceids=market_place_ids)

        request_response_dic = report_response.parsed
        report_request_id = request_response_dic['ReportRequestInfo']['ReportRequestId']['value']
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print 'get submit request id'
        logging.debug('get submit request id is: %s' % report_request_id)
        return report_request_id

    def get_report_status(self, report_request_id):
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print 'get status'
        logging.debug('get report status, report_request_id is: %s' % report_request_id)
        report_status = self.report_public.get_report_request_list(requestids=[report_request_id])
        report_status_dic = report_status.parsed
        report_processing_status = report_status_dic['ReportRequestInfo']['ReportProcessingStatus']['value']
        if report_processing_status == '_DONE_':
            generated_report_id = report_status_dic['ReportRequestInfo']['GeneratedReportId']['value']
        else:
            generated_report_id = ''
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print 'get status result'
        logging.debug('get status result, report_processing_status is:%s, generated_report_id is : %s' % (report_processing_status, generated_report_id))
        return [report_processing_status, generated_report_id]

    def get_report_result(self, generated_report_id):
        logging.debug('begin get result data')
        report_result = self.report_public.get_report(generated_report_id)
        report_result_datas = report_result.original.splitlines()
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print 'get result data'
        logging.debug('end get result data')
        return report_result_datas

    def shop_update_all(self, col, val):
        sql_insert = "insert into %s ( %s, shopname, shopsite) values (%s, '%s', '%s')" \
                     % (self.auth_info['table_name'], col, val, self.auth_info['ShopName'], self.auth_info['ShopSite'])
        print '\n sql_insert is %s' % sql_insert
        logging.debug('sql_insert is %s' % sql_insert)
        self.execute_db(sql_insert)

    def shop_update_increment(self, col, val, seller_sku):
        sql_delete = "delete from %s where shopname = '%s' and seller_sku = '%s' " \
                     %(self.auth_info['table_name'], self.auth_info['ShopName'], seller_sku)
        sql_insert = "insert into %s ( %s, shopname, shopsite) values (%s, '%s', '%s')" \
                     % (self.auth_info['table_name'], col, val, self.auth_info['ShopName'], self.auth_info['ShopSite'])
        print '\n sql_delete is %s' % sql_delete
        logging.debug('sql_delete is %s' % sql_delete)
        self.execute_db(sql_delete)
        print '\n sql_insert is %s' % sql_insert
        logging.debug('sql_insert is %s' % sql_insert)
        self.execute_db(sql_insert)

    def update_shop_status(self, auth_info, status):
        """
        记录店铺的刷新状态
        """
        cursor = self.db_conn.cursor()
        sql_record_exists = "select  name from t_config_amazon_shop_status where name = '%s'" % auth_info['ShopName']
        cursor.execute(sql_record_exists)
        shop_exists_obj = cursor.fetchone()
        if shop_exists_obj is None or shop_exists_obj[0] is None :
            sql_insert = "insert into t_config_amazon_shop_status (name,shop_name,shop_site,IP,uuid,synType,status) " \
                         "values ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                         %(auth_info['ShopName'], auth_info['ShopName'][0:9], auth_info['ShopSite'], auth_info['ShopIP'], auth_info['uuid'], auth_info['update_type'],status)
            print 'sql_insert: %s' % sql_insert
            logging.debug('update shop status sql_insert_1 is: %s' % sql_insert)
            cursor.execute(sql_insert)
            cursor.execute('commit;')
        else:
            sql_update = "update t_config_amazon_shop_status set uuid = '%s', synType = '%s', status = '%s' where name = '%s'" \
                         %(auth_info['uuid'], auth_info['update_type'], status, auth_info['ShopName'])
            print 'sql_update: %s' % sql_update
            logging.debug('update shop status sql_insert_2 is: %s' % sql_update)
            cursor.execute(sql_update)
            cursor.execute('commit;')
        cursor.close()

    def product_update(self, col, val, product_sku):
        sql_delete = "delete from %s where seller_sku = '%s'  and shopname = '%s'" \
                     %(self.auth_info['table_name'], product_sku, self.auth_info['ShopName'])
        sql_insert = "insert into %s (%s, shopname, shopsite, deal_action, deal_result) values (%s, '%s','%s', 'refresh_product', 'Success')" \
                     % (self.auth_info['table_name'], col, val, self.auth_info['ShopName'], self.auth_info['ShopSite'])
        print '\n sql_delete is %s' %sql_delete
        logging.debug('sql_delete is %s' %sql_delete)
        self.execute_db(sql_delete)
        print '\n sql_insert is %s' % sql_insert
        logging.debug('sql_insert is %s' % sql_insert)
        self.execute_db(sql_insert)

    def update_db_when_error(self, auth_info, error_msg):
        cursor = self.db_conn.cursor()
        for sku in auth_info['product_list']:
            sql = "update %s set deal_result = 'Fail', deal_result_info = '%s', updatetime = '%s'  where shopname = '%s' and seller_sku = '%s'" \
                  % (auth_info['table_name'], error_msg, datetime.datetime.now(), auth_info['ShopName'], sku)
            print 'error sql: %s' % sql
            logging.debug('error sql: %s' % sql)
            cursor.execute(sql)
            cursor.execute('commit;')
        cursor.close()

    def execute_db(self, sql):
        cursor = self.db_conn.cursor()
        try:
            cursor.execute(sql)
            cursor.execute('commit;')
            cursor.close()
        except Exception as e:
            cursor.close()
            print e

    def insert_progress_status(self, auth_info, status):
        """
        记录进度，供进度条使用
        """
        try:
            if auth_info.has_key('uuid'):
                cursor = self.db_conn.cursor()
                sql = "insert into t_config_amazon_progress_bar(uuid, ip, shopname, status, syntype) values ('%s', '%s', '%s', '%s', '%s')" \
                      % (auth_info['uuid'], auth_info['ShopIP'], auth_info['ShopName'], status, auth_info['update_type'])
                cursor.execute(sql)
                logging.debug('insert_progress_status sql is: %s' % sql)
                cursor.execute('commit;')
                cursor.close()
        except Exception, ex:
            cursor.close()
            print '%s_%s:%s' % (traceback.print_exc(), Exception, ex)

    def get_max_update_time(self):
            cursor = self.db_conn.cursor()
            sql_max_time = "select min(updatetime) from %s where ShopName = '%s' " \
                           %(self.auth_info['table_name'], self.auth_info['ShopName'])
            print 'sql_max_time is: %s' % sql_max_time
            cursor.execute(sql_max_time)
            max_time_obj = cursor.fetchone()
            if max_time_obj is None or len(max_time_obj) == 0 or max_time_obj[0] is None:
                max_update_time = (datetime.datetime.now() + datetime.timedelta(days=-15)).strftime("%Y-%m-%d")
            else:
                max_update_time = (max_time_obj[0] + datetime.timedelta(hours=-8)).strftime('%Y-%m-%dT%H:%M:%S')
            cursor.close()
            print 'max_update_time is :'
            print max_update_time
            return max_update_time

    def get_column(self, report_result_datas):
        for i, val in enumerate(report_result_datas):
            if i == 0:  # get  information's column
                report_result_data_column = val.split('\t')
                table_column = str(report_result_data_column)
                table_column = table_column.replace('[', '')
                table_column = table_column.replace(']', '')
                table_column = table_column.replace("'", '')
                table_column = table_column.replace('-', '_')
                break
        return table_column

    def get_value(self, val):
        report_result_data = val.split('\t')
        table_val = str(report_result_data)
        table_val = table_val.replace('[', '')
        table_val = table_val.replace(']', '')
        return table_val

    def delete_mid_table(self):
        sql_del = "delete from %s where ShopName = '%s' " % (self.auth_info['table_name'], self.auth_info['ShopName'])
        print 'sql_mid_table_del is: %s' % sql_del
        logging.debug('sql_mid_table_del is: %s' % sql_del)
        self.execute_db(sql_del)

    def update_really_table(self):
        sql_relation = "update %s a, %s b " \
                       "set  a.parent_asin = b.parent_asin, a.product_type = b.product_type, a.image_url=b.image_url " \
                       "where a.asin1=b.asin1 and  a.ShopName = b.ShopName and a.ShopName = '%s'" \
                       % (self.auth_info['table_name'], self.auth_info['table_name_really'], self.auth_info['ShopName'])

        sql_del = "delete from %s where shopname = '%s'" % (self.auth_info['table_name_really'], self.auth_info['ShopName'])
        sql_insert = "insert into %s select * from  %s where shopname = '%s'" \
                     %(self.auth_info['table_name_really'], self.auth_info['table_name'], self.auth_info['ShopName'])
        print 'sql_relation is: %s' % sql_relation
        logging.debug('sql_relation is: %s' % sql_relation)
        self.execute_db(sql_relation)
        print 'sql_del is: %s' % sql_del
        logging.debug('sql_del is: %s' % sql_del)
        self.execute_db(sql_del)
        print 'sql_insert is: %s' % sql_insert
        logging.debug('sql_insert is: %s' % sql_insert)
        self.execute_db(sql_insert)

    def report_flow(self, report_type):
        report_request_id = self.submit_report_request(report_type)
        time_sleep = 10
        count = 0
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print 'result id is: %s, now wait for  10 seconds  then check deal status.' % report_request_id
        logging.debug('result id is: %s, now wait for  10 seconds  then check deal status.' % report_request_id)
        while count < 5:
            time.sleep(time_sleep)
            time_sleep += time_sleep  # doubled wait time（10,20,40,80,160）
            count += 1
            try:
                report_processing_status = self.get_report_status(report_request_id)[0]
                if report_processing_status == '_DONE_':
                    self.insert_progress_status(self.auth_info, 'done')
                    generated_report_id = self.get_report_status(report_request_id)[1]
                    self.insert_progress_status(self.auth_info, 'getdata')
                    report_result_datas = self.get_report_result(generated_report_id)
                    date1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    data_cnt = len(report_result_datas) - 1
                    table_column = self.get_column(report_result_datas)
                    self.insert_progress_status(self.auth_info, 'backfill-' + str(data_cnt))
                    if self.auth_info['update_type'] in ('refresh_shop_all', 'refresh_ad_data'):
                        for i, val in enumerate(report_result_datas):
                            if i == 0:
                                continue
                            table_val = self.get_value(val)
                            self.shop_update_all(table_column, table_val)
                        self.update_really_table()
                        self.update_shop_status(self.auth_info, 'success')
                    elif self.auth_info['update_type'] == 'refresh_shop_increment':
                        for i, val in enumerate(report_result_datas):
                            if i == 0:
                                continue
                            table_val = self.get_value(val)
                            self.shop_update_increment(table_column, table_val, val.split('\t')[3])
                        self.update_shop_status(self.auth_info, 'success')
                    else:
                        try:
                            for i, val in enumerate(report_result_datas):
                                if i == 0:
                                    continue
                                table_val = self.get_value(val)
                                if val.split('\t')[3] in self.auth_info['product_list']:
                                    self.product_update(table_column, table_val, val.split('\t')[3])
                                else:
                                    pass
                        except Exception, ex:
                            traceback.print_exc()
                            self.update_db_when_error(self.auth_info, ex)
                    self.insert_progress_status(self.auth_info, 'success')
                    print date1
                    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    return report_result_datas
                else:
                    if report_processing_status == '_SUBMITTED_':
                        self.insert_progress_status(self.auth_info, 'submit')
                    elif report_processing_status == '_IN_PROGRESS_':
                        self.insert_progress_status(self.auth_info, 'progress')
                    elif report_processing_status == '_CANCELLED_':
                        self.insert_progress_status(self.auth_info, 'cancel')

                    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print 'processing_status is:%s, we will wait for %s seconds ' % (report_processing_status, time_sleep)
                    logging.debug('processing_status is:%s, we will wait for %s seconds ' % (report_processing_status, time_sleep))
            except Exception as e:
                self.insert_progress_status(self.auth_info, 'fail')
                print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                traceback.print_exc()
                logging.error('traceback.format_exc():\n%s' % traceback.format_exc())

        else:  # 循环超过5次，即总等待时长超过 31*time_sleep，则计为超时
            print 'Get submit_feed reuslt timeout'
            if self.auth_info['update_type'] in ('refresh_shop_all', 'refresh_ad_data','refresh_shop_increment'):
                self.insert_progress_status(self.auth_info, 'timeout')
            else:
                self.update_db_when_error(self.auth_info, 'timeout')
            logging.error('Get submit_feed reuslt timeout')
            return None


class UpdateProductInfo:
    """
    产品信息修改
    """
    def __init__(self):
        self.db_conn = MySQLdb.connect(DATABASE['HOST'],
                                       DATABASE['USER'],
                                       DATABASE['PASSWORD'],
                                       DATABASE['NAME'])

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
        feed_id = data['FeedSubmissionInfo']['FeedSubmissionId']['value']

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
            #product_list = str(auth_info['product_list']).replace('[','').replace(']','')
            for sku in auth_info['product_list']:
                sql = "update %s set quantity = 999, deal_result = 'Success', status = 'Active', updatetime= '%s' where shopname = '%s' and seller_sku = '%s'" \
                      %(auth_info['table_name'], datetime.datetime.now(), auth_info['ShopName'], sku)
                print 'load sql: %s' % sql
                logging.debug('load sql: %s' % sql)
                cursor.execute(sql)
                cursor.execute('commit;')
            cursor.close()
        elif auth_info['update_type'] == 'unload_product':
            #product_list = str(auth_info['product_list']).replace('[', '').replace(']', '')
            for sku in auth_info['product_list']:
                sql = "update %s set quantity = 0 , deal_result = 'Success', status = 'Inactive', updatetime= '%s' where shopname = '%s' and seller_sku = '%s'" \
                      % (auth_info['table_name'], datetime.datetime.now(), auth_info['ShopName'], sku)
                print 'unload sql: %s' % sql
                logging.debug('unload sql: %s' % sql)
                cursor.execute(sql)
                cursor.execute('commit;')
            cursor.close()
        else:
            pass

    def update_db_when_error(self, auth_info, error_msg):
        cursor = self.db_conn.cursor()
        try:
            if auth_info['update_type'] in ('product_info_modify', 'product_price_modify', 'product_image_modify'):
                sql = "update %s set deal_result = 'Fail', deal_result_info = '%s', updatetime= '%s' where shopname = '%s' and seller_sku = '%s'" \
                      % (auth_info['table_name'], error_msg, datetime.datetime.now(), auth_info['ShopName'], auth_info['seller_sku'])
                print 'sql is:%s' % sql
                cursor.execute(sql)
                cursor.execute('commit;')
            else:
                for sku in auth_info['product_list']:
                    sql = "update %s set deal_result = 'Fail', deal_result_info = '%s', updatetime= '%s' where shopname = '%s' and seller_sku = '%s'" \
                          % (auth_info['table_name'], error_msg, datetime.datetime.now(), auth_info['ShopName'], sku)
                    print 'error sql: %s' % sql
                    logging.debug('error sql: %s' % sql)
                    cursor.execute(sql)
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

    def get_images_new(self,db_connect, upload_id):
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
        cursor = db_connect.cursor()
        try:
            # 主体图片信息
            sql_main = "select seller_sku, image_url from t_online_info_amazon where 	id = %s" % upload_id
            cursor.execute(sql_main)
            main_image_info = cursor.fetchone()

            image_path = LOCAL_PATH  # 本地图片根目录


            image_all_dic = {}

            image_each_dic = {}

            if main_image_info[1]:
                image_url = main_image_info[1].split('/', 3)[-1]
                code = self.random_code()
                image_url_local = code + '.' + main_image_info[1].split('.')[-1]
                bucket.get_object_to_file(image_url, image_path + image_url_local)
                image_each_dic['main_url'] = image_url_local

            image_all_dic[main_image_info[0]] = image_each_dic
            return image_all_dic
        except Exception as e:
            print e
            traceback.print_exc()
            logging.error('get_image_new: traceback.format_exc():\n%s' % traceback.format_exc())
            return None
        finally:
            cursor.close()

    def get_image_xml_new(self, image_info, seller_id):
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

        try:
            num = 1
            image_xml = {}
            for key, value in image_info.items():
                for key_child in sorted(value.keys()):
                    if key_child == 'main_url':
                        image_type = 'Main'
                    else:
                        image_type = 'PT' + key_child[-1]
                    image_url = 'http://' + self.realIP + '/' + value[key_child]
                    image_xml[num] = IMAGE_BODY_XML
                    image_xml[num] = image_xml[num].replace('MESSAGENUM', str(num))
                    image_xml[num] = image_xml[num].replace('PRODUCTSKU', key)
                    image_xml[num] = image_xml[num].replace('CHANGE_IMAGE_TYPE', image_type)
                    image_xml[num] = image_xml[num].replace('IMAGELOCALTIONURL', image_url)
                    num += 1

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
            if auth_info['update_type'] in ('load_product', 'unload_product'):
                feed_type = '_POST_INVENTORY_AVAILABILITY_DATA_'
            elif auth_info['update_type'] == 'product_info_modify':
                feed_type = '_POST_PRODUCT_DATA_'
            elif auth_info['update_type'] == 'product_price_modify':
                feed_type = '_POST_PRODUCT_PRICING_DATA_'
            elif auth_info['update_type'] == 'product_image_modify':
                images = self.get_images_new(self.db_conn, auth_info['pri_id'])
                image_xml = self.get_image_xml_new(images, auth_info['SellerId'])
                print 'image_xml is :%s' % image_xml
                logging.debug('image_xml is :%s' % image_xml)

                feed_data = image_xml
                feed_type = '_POST_PRODUCT_IMAGE_DATA_'
                return
            else:
                feed_type = ''

            submit_feed_response = self.submit_feed(auth_info, feed_data, feed_type)
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
            logging.debug(ex)
            self.update_db_when_error(auth_info, ex)


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
            time.sleep(10)  # 防止超请求限制，重新提交
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


class GetLocalIPAndMqInfo:
    """
    获取当前vps服务器IP；从数据库获取MQ信息
    """
    def __init__(self):
        self.db_conn = MySQLdb.connect(DATABASE['HOST'],
                                       DATABASE['USER'],
                                       DATABASE['PASSWORD'],
                                       DATABASE['NAME'])

    @staticmethod
    def get_real_url(url=r'http://www.ip138.com/'):
        r = requests.get(url)
        txt = r.text
        soup = BeautifulSoup(txt, "html.parser").iframe
        return soup["src"]

    @staticmethod
    def get_out_ip(url):
        r = requests.get(url)
        txt = r.text
        ip = txt[txt.find("[") + 1: txt.find("]")]
        print('ip:' + ip)
        return ip

    def get_mq_info(self):
        cursor = self.db_conn.cursor()
        try:
            rabbit_mq = {}
            sql = "select ip, k, v from t_config_mq_info where name = 'Amazon-RabbitMQ-Server'"
            cursor.execute(sql)
            mq_config_info = cursor.fetchall()
            cursor.close()
            for mq_config_info_obj in mq_config_info:
                rabbit_mq['hostname'] = mq_config_info_obj[0]
                k = mq_config_info_obj[1]
                v = mq_config_info_obj[2]
                rabbit_mq[k] = v
            return rabbit_mq
        except Exception as e:
            cursor.close()
            print e
            return None


get_info_obj = GetLocalIPAndMqInfo()
local_ip = get_info_obj.get_out_ip(get_info_obj.get_real_url())
print 'local_ip is:%s' % local_ip
RABBIT_MQ = get_info_obj.get_mq_info()
print 'RABBIT_MQ is: %s' % str(RABBIT_MQ)


def deal_and_response_request(ch, method, props, body):
    logging.debug('get message from mq, message is: %s' % body)

    if body == 'auto_upgrade':
        try:
            auto_upgrade()
            return
        except Exception as e:
            print e
            print 'auto_upgrade failed when get message'
            print 'traceback.format_exc():\n%s' % traceback.format_exc()
            logging.error('traceback.format_exc():\n%s' % traceback.format_exc())
            return

    auth_info = eval(body)
    print auth_info
    if local_ip == auth_info['ShopIP']:
        # refresh_shop, refresh_product, load_product, unload_product
        if auth_info['update_type'] in ('refresh_shop_all', 'refresh_shop_increment', 'refresh_product', 'refresh_ad_data'):
            # 全量刷新时先更新中间表，中间表更新完成后一次性更新实际业务表（此时保留之前的图片和主体、变体关系）
            if auth_info['update_type'] in ('refresh_shop_all', 'refresh_ad_data'):
                auth_info['table_name_really'] = auth_info['table_name']
                auth_info['table_name'] = auth_info['table_name'] + '_for_update'

            get_product_info_ins = GetShopProductInfo(auth_info)
            # 全量更新时先清理中间表数据
            if auth_info['update_type'] in ('refresh_shop_all', 'refresh_ad_data'):
                get_product_info_ins.delete_mid_table()
            get_product_info_ins.report_flow('_GET_MERCHANT_LISTINGS_ALL_DATA_')

            # 全量数据刷新完后，查找图片及主变体关系时直接对实际业务表进行更新
            if auth_info['update_type']  in ('refresh_shop_all', 'refresh_ad_data'):
                auth_info['table_name'] = auth_info['table_name_really']
            get_product_info_obj = GetProductInfoByAsin(auth_info)

            # 全量增量全表更新图片及主、变体关系， 指定商品刷新时只刷新特定商品
            if auth_info['update_type'] in ('refresh_shop_all', 'refresh_shop_increment', 'refresh_ad_data'):
                get_product_info_obj.get_parent_asin_and_image()
                if auth_info['update_type'] == 'refresh_ad_data':
                    sql_ad_delete ="delete from t_amazon_cpc_ad where shop_name = '%s' and shop_site = '%s'" %(auth_info['ShopName'], auth_info['ShopSite'])
                    print 'sql_ad_delete is: %s' % sql_ad_delete
                    sql_ad_insert = "insert into t_amazon_cpc_ad(shop_name,shop_site,seller_sku,asin,image_url,price,create_date) select ShopName,shopsite,seller_sku,asin1,image_url,price,open_date from t_online_info_amazon where ShopName = '%s' and ShopSite = '%s';" %(auth_info['ShopName'], auth_info['ShopSite'])
                    print 'sql_ad_insert is: %s' % sql_ad_insert
                    get_product_info_ins.execute_db(sql_ad_delete)
                    get_product_info_ins.execute_db(sql_ad_insert)
            else:
                get_product_info_obj.get_parent_asin_and_image(auth_info['product_list'])

        elif auth_info['update_type'] in ('load_product', 'unload_product', 'product_info_modify', 'product_price_modify', 'product_image_modify'):
            server = UpdateProductInfo()
            response = server.feed_start(auth_info)
            print response
    else:
        logging.error('The ip in auth_info:%s does not match local ip: %s' % (auth_info['ShopIP'], local_ip))
        print 'The ip in auth_info:%s does not match local ip: %s' % (auth_info['ShopIP'], local_ip)


def listen_client():

    credentials = pika.PlainCredentials(RABBIT_MQ['MQUser'], RABBIT_MQ['MQPassword'])
    parameters = pika.ConnectionParameters(RABBIT_MQ['hostname'], RABBIT_MQ['MQPort'], '/', credentials, heartbeat=0)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    queue = 'amazon_' + local_ip + '_refresh_product_data'
    print 'queue is: %s' % queue
    channel.queue_declare(queue=queue)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(deal_and_response_request, queue=queue, no_ack=True)
    print(" [x] Awaiting RPC requests")
    channel.start_consuming()


def retry_listen():
    try:
        auto_upgrade()
    except Exception as e:
        print e
        print 'auto_upgrade failed when start server'
        print 'traceback.format_exc():\n%s' % traceback.format_exc()
        logging.error('traceback.format_exc():\n%s' % traceback.format_exc())

    try:
        listen_client()
    except Exception as e:
        print e
        traceback.print_exc()
        logging.debug(e)
        time.sleep(5)
        retry_listen()


if __name__ == '__main__':
    print 'The file running now is: %s' % sys.argv[0].split('\\')[-1]
    retry_listen()







