# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: fba_refresh-20180828.py
 @time: 2018/8/28 9:30
"""
import logging.handlers
from mws import Reports, Products
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


def is_windows_system():
    return 'Windows' in platform.system()


def auto_upgrade():
    if is_windows_system():
        access_key_id = 'LTAIH6IHuMj6Fq2h'
        access_key_secret = 'N5eWsbw8qBkMfPREkgF2JnTsDASelM'
        endpoint_out = 'oss-cn-shanghai.aliyuncs.com'
        bucket_name_api_version = 'fancyqube-apiversion'
        print 'this file is: %s' % str(sys.argv[0])
        logging.debug('this file is: %s' % str(sys.argv[0]))
        auth = oss2.Auth(access_key_id, access_key_secret)
        bucket = oss2.Bucket(auth, endpoint_out, bucket_name_api_version)
        for filename2 in oss2.ObjectIterator(bucket, prefix='fba_refresh-'):
            if sys.argv[0].split('\\')[-1] < filename2.key:
                print 'The file in oss: %s  is  newer than current file,we will download it and run it.' % str(filename2.key)
                logging.debug('The file in oss: %s  is  newer than current file,we will download it and run it.' % str(filename2.key))
                bucket.get_object_to_file(filename2.key, filename2.key)
                if win32api.ShellExecute(0, 'open', filename2.key, '', '', 3) > 32:
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


def delete_history_log(file_pattern, file_time_diff, scan_weekday=None):
    if scan_weekday is not None and datetime.datetime.now().weekday() != scan_weekday:
        print 'Not scan time'
        return

    file_url = os.getcwd()
    print 'File scan path is: %s' % file_url
    pattern_file = [f for f in os.listdir(file_url) if file_pattern in f]
    for i in range(len(pattern_file)):
        file_full_path = os.path.join(file_url, pattern_file[i])
        print 'file full path is %s' % file_full_path
        file_date = os.path.getmtime(file_full_path)
        file_time = datetime.datetime.fromtimestamp(file_date).strftime('%Y-%m-%d %H:%M:%S')
        print 'file time is:%s' % file_time
        time_now = time.time()
        time_diff_days = (time_now - file_date) / 60 / 60 / 24
        print 'time diff is: %s' % time_diff_days
        if time_diff_days >= file_time_diff:
            try:
                os.remove(file_full_path)
                print("delete this file：%s ： %s" % (file_time, pattern_file[i]))
            except Exception as e:
                print e
        else:
            print 'not history file'


def refresh_db_tables(auth_info, sql_execute_obj):
    sql_ad_delete = "delete from t_amazon_cpc_ad where shop_name = '%s' and shop_site = '%s'" % (auth_info['ShopName'], auth_info['ShopSite'])
    print 'sql_ad_delete is: %s' % sql_ad_delete
    logging.debug('sql_ad_delete is: %s' % sql_ad_delete)
    sql_ad_insert = "insert into t_amazon_cpc_ad(shop_name,shop_site,seller_sku,title,asin,image_url,price,quantity,create_date,STATUS,Parent_asin,product_id_type) select ShopName,shopsite,seller_sku,item_name,asin1,image_url,price,quantity,open_date,STATUS,Parent_asin,product_id_type from t_online_info_amazon where ShopName = '%s' and ShopSite = '%s';" % (
        auth_info['ShopName'], auth_info['ShopSite'])
    print 'sql_ad_insert is: %s' % sql_ad_insert
    logging.debug('sql_ad_insert is: %s' % sql_ad_insert)
    sql_execute_obj.execute_db(sql_ad_delete)
    sql_execute_obj.execute_db(sql_ad_insert)

    sql_is_fba = '''update t_amazon_cpc_ad a,t_online_amazon_fba_inventory b  set a.is_fba = 1
                           where a.shop_name = b.ShopName
                           and a.seller_sku = b.sku
                           and b.afn_listing_exists ='Yes' 
                           and a.shop_name = '%s' ''' % auth_info['ShopName']
    print "sql_is_fba is : %s" % sql_is_fba
    logging.debug("sql_is_fba is : %s" % sql_is_fba)
    sql_execute_obj.execute_db(sql_is_fba)

    sql_fba_data = '''
                        UPDATE t_amazon_cpc_ad a, t_online_amazon_fba_inventory b
                       SET a.afn_listing_exists             = b.afn_listing_exists,
                           a.afn_warehouse_quantity         = b.afn_warehouse_quantity,
                           a.afn_fulfillable_quantity       = b.afn_fulfillable_quantity,
                           a.afn_unsellable_quantity        = b.afn_unsellable_quantity,
                           a.afn_reserved_quantity          = b.afn_reserved_quantity,
                           a.afn_total_quantity             = b.afn_total_quantity,
                           a.per_unit_volume                = b.per_unit_volume,
                           a.afn_inbound_working_quantity   = b.afn_inbound_working_quantity,
                           a.afn_inbound_shipped_quantity   = b.afn_inbound_shipped_quantity,
                           a.afn_inbound_receiving_quantity = b.afn_inbound_receiving_quantity
                     where a.shop_name = b.ShopName
                       and a.seller_sku = b.sku
                       and a.shop_name = '%s'
                        ''' % auth_info['ShopName']
    print "sql_fba_data is : %s" % sql_fba_data
    logging.debug("sql_fba_data is : %s" % sql_fba_data)
    sql_execute_obj.execute_db(sql_fba_data)

    sql_orders_clear = '''
                        UPDATE t_amazon_cpc_ad a
                       SET a.orders_7days  = 0,
                           a.orders_15days = 0,
                           a.orders_30days = 0,
                           a.orders_total  = 0
                     WHERE a.shop_name = '%s'
                        ''' % auth_info['ShopName']

    if auth_info['ShopSite'] == 'UK':
        sql_order_condition = " and sales_channel = 'Amazon.co.uk'"
    elif auth_info['ShopSite'] == 'DE':
        sql_order_condition = " and sales_channel = 'Amazon.de'"
    elif auth_info['ShopSite'] == 'FR':
        sql_order_condition = " and sales_channel = 'Amazon.fr'"
    else:
        sql_order_condition = ""

    sql_orders_7day = '''update t_amazon_cpc_ad a,
                       (SELECT shop_name shopname, sku shopsku, count(amazon_order_id) sales
                          FROM t_amazon_all_orders_data a
                         WHERE shop_name = '%s'
                           and order_status != 'Cancelled'
                           %s
                           and purchase_date >= DATE_SUB(CURDATE(), INTERVAL + 7*24+8 HOUR)
                         GROUP BY shop_name, sku) b
                   set a.orders_7days = sales
                 where a.shop_name = b.shopname
                   and a.seller_sku = b.shopsku
                   and a.shop_name ='%s';''' % (auth_info['ShopName'], sql_order_condition, auth_info['ShopName'])

    sql_orders_15day = '''update t_amazon_cpc_ad a,
                                  (SELECT shop_name shopname, sku shopsku, count(amazon_order_id) sales
                          FROM t_amazon_all_orders_data a
                         WHERE shop_name = '%s'
                           and order_status != 'Cancelled'
                           %s
                           and purchase_date >= DATE_SUB(CURDATE(), INTERVAL + 15*24+8 HOUR)
                         GROUP BY shop_name, sku) b
                              set a.orders_15days = sales
                            where a.shop_name = b.shopname
                              and a.seller_sku = b.shopsku
                              and a.shop_name = '%s';''' % (auth_info['ShopName'], sql_order_condition, auth_info['ShopName'])

    sql_orders_30day = '''update t_amazon_cpc_ad a,(SELECT shop_name shopname, sku shopsku, count(amazon_order_id) sales
                          FROM t_amazon_all_orders_data a
                         WHERE shop_name = '%s'
                           and order_status != 'Cancelled'
                           %s
                           and purchase_date >= DATE_SUB(CURDATE(), INTERVAL + 30*24+8 HOUR)
                         GROUP BY shop_name, sku) b
                                  set a.orders_30days = sales
                                where a.shop_name = b.shopname
                                  and a.seller_sku = b.shopsku
                                  and a.shop_name = '%s';''' % (auth_info['ShopName'], sql_order_condition, auth_info['ShopName'])

    sql_orders_total = '''update t_amazon_cpc_ad a,
                                          (SELECT shop_name shopname, sku shopsku, count(amazon_order_id) sales
                          FROM t_amazon_all_orders_data a
                         WHERE shop_name = '%s'
                         %s
                         and order_status != 'Cancelled'
                         GROUP BY shop_name, sku) b
                                      set a.orders_total = sales
                                    where a.shop_name = b.shopname
                                      and a.seller_sku = b.shopsku
                                      and a.shop_name ='%s';''' % (auth_info['ShopName'], sql_order_condition, auth_info['ShopName'])

    sql_sku_relation = '''update t_amazon_cpc_ad a, py_db.b_goodsskulinkshop b
                       set a.sku = b.sku
                     where SUBSTRING_INDEX(a.seller_sku,'*',1) = b.shopsku
                     and a.shop_name ='%s' ''' % auth_info['ShopName']

    sql_listing_data = '''update t_online_info_amazon a, t_amazon_cpc_ad b
                       set a.afn_listing_exists     = b.afn_listing_exists,
                           a.afn_warehouse_quantity = b.afn_warehouse_quantity,
                           a.orders_7days           = b.orders_7days,
                           a.is_fba                 = b.is_fba
                     where a.ShopName = b.shop_name
                       and a.seller_sku = b.seller_sku
                       and a.shopname = '%s';
                    ''' % auth_info['ShopName']

    sql_sku_relation_product = '''update t_online_info_amazon a, py_db.b_goodsskulinkshop b
                          set a.sku = b.sku
                        where SUBSTRING_INDEX(a.seller_sku,'*',1) = b.shopsku
                        and a.shopname = '%s' ''' % auth_info['ShopName']

    sql_receive_date = '''
                        update t_online_info_amazon a,
                               (SELECT shop_name, sku, max(received_date) received_date
                                  FROM t_report_fba_fulfillment_inventory_receipts_data a
                                 WHERE shop_name = '%s'
                                 GROUP BY shop_name, sku) b
                           set a.inventory_received_date = received_date
                         where a.shopname = b.shop_name
                           and a.seller_sku = b.sku
                           and a.shopname = '%s';
                    ''' % (auth_info['ShopName'], auth_info['ShopName'])

    sql_receive_date_null = '''
            update t_online_info_amazon a
               set a.inventory_received_date = '2018-01-01'
             where a.inventory_received_date is null
               and is_fba = 1
               and a.shopname = '%s';
            ''' % auth_info['ShopName']

    sql_estimated_fba_fees = '''UPDATE t_online_info_amazon a, t_amazon_estimated_fba_fees b
                   SET a.estimated_fee = b.estimated_fee
                 WHERE a.shopname = b.shop_name
                   AND a.seller_sku = b.sku
                   and a.shopname = '%s'
              ''' % auth_info['ShopName']

    sql_inactive_shop = "update t_online_info_amazon set shop_status = 1 where shopname = '%s' and shopname in (select shop_name from t_amazon_inactive_shop where status = 0)" % auth_info['ShopName']

    print "sql_orders_clear is : %s" % sql_orders_clear
    logging.debug("sql_orders_clear is : %s" % sql_orders_clear)
    sql_execute_obj.execute_db(sql_orders_clear)

    print "sql_orders_7day is : %s" % sql_orders_7day
    logging.debug("sql_orders_7day is : %s" % sql_orders_7day)
    sql_execute_obj.execute_db(sql_orders_7day)

    print "sql_orders_15day is : %s" % sql_orders_15day
    logging.debug("sql_orders_15day is : %s" % sql_orders_15day)
    sql_execute_obj.execute_db(sql_orders_15day)

    print "sql_orders_30day is : %s" % sql_orders_30day
    logging.debug("sql_orders_30day is : %s" % sql_orders_30day)
    sql_execute_obj.execute_db(sql_orders_30day)

    print "sql_orders_total is : %s" % sql_orders_total
    logging.debug("sql_orders_total is : %s" % sql_orders_total)
    get_data_public_obj.execute_db(sql_orders_total)

    print "sql_sku_relation is : %s" % sql_sku_relation
    logging.debug("sql_sku_relation is : %s" % sql_sku_relation)
    sql_execute_obj.execute_db(sql_sku_relation)

    print "sql_listing_data is : %s" % sql_listing_data
    logging.debug("sql_listing_data is : %s" % sql_listing_data)
    sql_execute_obj.execute_db(sql_listing_data)

    print "sql_sku_relation_product is : %s" % sql_sku_relation_product
    logging.debug("sql_sku_relation_product is : %s" % sql_sku_relation_product)
    sql_execute_obj.execute_db(sql_sku_relation_product)

    print "sql_receive_date is : %s" % sql_receive_date
    logging.debug("sql_receive_date is : %s" % sql_receive_date)
    sql_execute_obj.execute_db(sql_receive_date)

    print "sql_receive_date_null is : %s" % sql_receive_date_null
    logging.debug("sql_receive_date_null is : %s" % sql_receive_date_null)
    sql_execute_obj.execute_db(sql_receive_date_null)

    print "sql_estimated_fba_fees is : %s" % sql_estimated_fba_fees
    logging.debug("sql_estimated_fba_fees is : %s" % sql_estimated_fba_fees)
    sql_execute_obj.execute_db(sql_estimated_fba_fees)

    print "sql_inactive_shop is : %s" % sql_inactive_shop
    logging.debug("sql_inactive_shop is : %s" % sql_inactive_shop)
    sql_execute_obj.execute_db(sql_inactive_shop)


class ReportPublic:
    def __init__(self, auth_info_public):
        self.auth_info = auth_info_public
        self.report_public = Reports(self.auth_info['AWSAccessKeyId'],
                                     self.auth_info['SecretKey'],
                                     self.auth_info['SellerId'],
                                     self.auth_info['ShopSite']
                                     )
        self.db_conn = pymysql.connect(DATABASE['HOST'],
                                       DATABASE['USER'],
                                       DATABASE['PASSWORD'],
                                       DATABASE['NAME'],
                                       charset='utf8')

    def close_db_conn(self):
        try:
            if self.db_conn:
                self.db_conn.close()
        except Exception as ex:
            print ex
            logging.error('class  ReportPublic close db connection failed!' )
            logging.error('traceback.format_exc():\n%s' % traceback.format_exc())

    def submit_report_request(self, report_type, start_date, end_date):
        logging.debug('submit report, report type is:%s' % report_type)
        logging.debug('-------------------------------------------------------')
        market_place_ids = [self.auth_info['MarketplaceId']]
        report_response = self.report_public.request_report(report_type,
                                                            start_date=start_date,
                                                            end_date=end_date,
                                                            marketplaceids=market_place_ids)
        request_response_dic = report_response.parsed
        report_request_id = request_response_dic['ReportRequestInfo']['ReportRequestId']['value']
        logging.debug('get submit request id is: %s' % report_request_id)
        return report_request_id

    def get_report_status(self, report_request_id):
        logging.debug('get report status, report_request_id is: %s' % report_request_id)
        report_status = self.report_public.get_report_request_list(requestids=[report_request_id])
        report_status_dic = report_status.parsed
        report_processing_status = report_status_dic['ReportRequestInfo']['ReportProcessingStatus']['value']
        if report_processing_status == '_DONE_':
            generated_report_id = report_status_dic['ReportRequestInfo']['GeneratedReportId']['value']
        else:
            generated_report_id = ''
        logging.debug('get status result, report_processing_status is:%s, generated_report_id is : %s' % (report_processing_status, generated_report_id))
        return [report_processing_status, generated_report_id]

    def get_report_result(self, generated_report_id):
        logging.debug('begin get result data')
        report_result = self.report_public.get_report(generated_report_id)

        if self.auth_info['ShopSite'] == 'JP':
            encode_type = chardet.detect(report_result.original)['encoding']
            report_result_mid = report_result.original.decode(encode_type).encode('utf-8')
            # report_result_mid = report_result.original.decode('SHIFT_JIS').encode('utf-8')
        else:
            report_result_mid = report_result.original
        report_result_data = report_result_mid.splitlines()
        logging.debug('end get result data')
        return report_result_data

    def report_flow(self, report_type, start_date=None, end_date=None):
        try:
            begin_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            report_request_id = self.submit_report_request(report_type, start_date, end_date)
            time_sleep = 10
            count = 0
            print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print 'result id is: %s, now wait for  30 seconds  then check deal status.' % report_request_id
            logging.debug('result id is: %s, now wait for  30 seconds  then check deal status.' % report_request_id)
            while count < 5:
                if count == 0:
                    time.sleep(30)
                else:
                    time.sleep(time_sleep)
                time_sleep += time_sleep  # doubled wait time（10,20,40,80,160）
                count += 1
                try:
                    report_processing_status = self.get_report_status(report_request_id)[0]
                    if report_processing_status == '_DONE_':
                        logging.debug('processing_status is: _DONE_, now get the result')
                        generated_report_id = self.get_report_status(report_request_id)[1]
                        report_result_data = self.get_report_result(generated_report_id)
                        data_cnt = len(report_result_data) - 1
                        logging.debug('there are %s  records in report_result_data, begin insert them into db' % data_cnt)
                        self.insert_public(report_type, report_result_data)
                        self.update_shop_status_public(report_type, self.auth_info, begin_time, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'Success', '')
                        return report_result_data
                    elif report_processing_status in ('_SUBMITTED_', '_IN_PROGRESS_'):
                        logging.debug('processing_status is:%s, we will wait for %s seconds ' % (report_processing_status, time_sleep))
                    else:
                        self.update_shop_status_public(report_type, self.auth_info, begin_time, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'Fail', report_processing_status)
                        return
                except Exception as err:
                    logging.error('traceback.format_exc():\n%s' % traceback.format_exc())
                    self.update_shop_status_public(report_type, self.auth_info, begin_time, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'Fail', str(err).replace("'", "`"))
                    return
            else:  # 循环超过5次，即总等待时长超过 31*time_sleep，则计为超时
                logging.error('Get submit_feed reuslt timeout')
                self.update_shop_status_public(report_type, self.auth_info, begin_time, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'Fail', 'time out')
                return
        except Exception as e:
            print e
            print '----------------------------------refresh_except: %s----------------------------------------------------' % report_type
            logging.error('----------------------------------refresh_except: %s----------------------------------------------------' % report_type)
            logging.error('traceback.format_exc():\n%s' % traceback.format_exc())
            return

    def insert_public(self, report_type, get_report_data):
        if report_type == '_GET_FBA_MYI_ALL_INVENTORY_DATA_':
            self.fba_insert(get_report_data)
        elif report_type == '_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_':
            self.order_insert(get_report_data)
        elif report_type == '_GET_FBA_FULFILLMENT_INVENTORY_RECEIPTS_DATA_':
            self.fba_receive_insert(get_report_data)
        elif report_type == '_GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA_':
            self.fba_fees_insert(get_report_data)
        elif report_type == '_GET_FBA_FULFILLMENT_REMOVAL_ORDER_DETAIL_DATA_':
            self.remove_order_insert(get_report_data)
        elif report_type == '_GET_MERCHANT_LISTINGS_ALL_DATA_':
            table_column = self.get_column(get_report_data)
            for i, value in enumerate(get_report_data):
                if i == 0:
                    continue
                table_val = self.get_value(value)
                self.shop_update_all(table_column, table_val, value.split('\t'))
            self.update_really_table()
        else:
            pass

    def fba_insert(self, get_report_data):
        cursor = self.db_conn.cursor()
        for i, value in enumerate(get_report_data):
            if i == 0:
                continue
            report_data = value.split('\t')

            sku = report_data[0]
            fnsku = report_data[1]
            asin = report_data[2]
            product_name = report_data[3].replace("'", "`")
            condition_a = report_data[4]
            your_price = report_data[5]
            mfn_listing_exists = report_data[6]
            mfn_fulfillable_quantity = report_data[7]
            afn_listing_exists = report_data[8]
            afn_warehouse_quantity = report_data[9]
            afn_fulfillable_quantity = report_data[10]
            afn_unsellable_quantity = report_data[11]
            afn_reserved_quantity = report_data[12]
            afn_total_quantity = report_data[13]
            per_unit_volume = report_data[14]
            afn_inbound_working_quantity = report_data[15]
            afn_inbound_shipped_quantity = report_data[16]
            afn_inbound_receiving_quantity = report_data[17]

            refresh_time = datetime.datetime.now()
            shop_name = self.auth_info['ShopName']

            sql_delete = "delete from t_online_amazon_fba_inventory where ShopName ='%s' and sku ='%s' and fnsku='%s' and asin='%s' " % (self.auth_info['ShopName'], sku, fnsku, asin)
            print sql_delete
            logging.debug(sql_delete)
            cursor.execute(sql_delete)
            sql_insert = '''
               INSERT INTO t_online_amazon_fba_inventory
                (sku, fnsku, asin, product_name, condition_a, your_price, mfn_listing_exists, mfn_fulfillable_quantity, afn_listing_exists, afn_warehouse_quantity, afn_fulfillable_quantity, afn_unsellable_quantity, afn_reserved_quantity, afn_total_quantity, per_unit_volume, afn_inbound_working_quantity, afn_inbound_shipped_quantity, afn_inbound_receiving_quantity, RefreshTime, ShopName)
              VALUES
                ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');
            ''' % (sku,
                   fnsku,
                   asin,
                   product_name,
                   condition_a,
                   your_price,
                   mfn_listing_exists,
                   mfn_fulfillable_quantity,
                   afn_listing_exists,
                   afn_warehouse_quantity,
                   afn_fulfillable_quantity,
                   afn_unsellable_quantity,
                   afn_reserved_quantity,
                   afn_total_quantity,
                   per_unit_volume,
                   afn_inbound_working_quantity,
                   afn_inbound_shipped_quantity,
                   afn_inbound_receiving_quantity,
                   refresh_time,
                   shop_name)
            print sql_insert
            logging.debug(sql_insert)
            cursor.execute(sql_insert)
        self.db_conn.commit()
        cursor.close()

    def get_last_order_time(self):
        cursor = self.db_conn.cursor()
        sql_max_time = "select max(purchase_date) from t_amazon_all_orders_data where shop_name = '%s' " % (self.auth_info['ShopName'])
        print 'sql_max_time is: %s' % sql_max_time
        cursor.execute(sql_max_time)
        max_time_obj = cursor.fetchone()
        cursor.close()

        if max_time_obj is None or len(max_time_obj) == 0 or max_time_obj[0] is None:
            # max_update_time = (datetime.datetime.now() + datetime.timedelta(days=-180)).strftime("%Y-%m-%d")
            max_update_time = datetime.datetime.now() + datetime.timedelta(days=-180)
        else:
            # max_update_time = (max_time_obj[0] + datetime.timedelta(hours=-8)).strftime('%Y-%m-%dT%H:%M:%S')
            max_update_time = max_time_obj[0]

        last_order_time = list()
        if max_update_time < datetime.datetime.now() + datetime.timedelta(days=-30):
            last_order_time.append(max_update_time.strftime('%Y-%m-%d'))
            for i in range(1, 10):
                time_30_days_later = max_update_time + datetime.timedelta(days=30 * i)
                if time_30_days_later < datetime.datetime.now():
                    last_order_time.append(time_30_days_later.strftime('%Y-%m-%d'))
                else:
                    last_order_time.append(datetime.datetime.now().strftime('%Y-%m-%d'))
                    break
        else:
            time_29_days_before = datetime.datetime.now() + datetime.timedelta(days=-10)
            last_order_time.append(time_29_days_before.strftime('%Y-%m-%d'))
            time_this_day_end = datetime.datetime.now() + datetime.timedelta(days=1)
            last_order_time.append(time_this_day_end.strftime('%Y-%m-%d'))
        print 'last_order_time is :'
        print last_order_time
        logging.debug('last_order_time is : %s' % str(last_order_time))
        return last_order_time

    def order_insert(self, get_report_data):
        cursor = self.db_conn.cursor()
        for i, value in enumerate(get_report_data):
            if i == 0:
                continue
            report_data = value.split('\t')

            amazon_order_id = report_data[0]
            merchant_order_id = report_data[1]
            purchase_date = report_data[2]
            last_updated_date = report_data[3]
            order_status = report_data[4]
            fulfillment_channel = report_data[5]
            sales_channel = report_data[6]
            order_channel = report_data[7]
            url = report_data[8]
            ship_service_level = report_data[9]
            product_name = report_data[10].replace("'", "`")
            sku = report_data[11]
            asin = report_data[12]
            item_status = report_data[13]
            quantity = report_data[14]
            currency = report_data[15]
            item_price = report_data[16]
            item_tax = report_data[17]
            shipping_price = report_data[18]
            shipping_tax = report_data[19]
            gift_wrap_price = report_data[20]
            gift_wrap_tax = report_data[21]
            item_promotion_discount = report_data[22]
            ship_promotion_discount = report_data[23]
            ship_city = report_data[24].replace("'", "`")
            ship_state = report_data[25]
            ship_postal_code = report_data[26]
            ship_country = report_data[27]
            promotion_ids = report_data[28]

            # RefreshTime = datetime.datetime.now()
            shop_name = self.auth_info['ShopName']

            sql_delete = "delete from t_amazon_all_orders_data where shop_name ='%s' and sku ='%s' and amazon_order_id='%s' and asin='%s' " % (self.auth_info['ShopName'], sku, amazon_order_id, asin)
            print sql_delete
            logging.debug(sql_delete)
            cursor.execute(sql_delete)
            sql_insert = '''
                INSERT INTO t_amazon_all_orders_data
                  (amazon_order_id,merchant_order_id,purchase_date,last_updated_date,order_status,fulfillment_channel,sales_channel,order_channel,url,ship_service_level,product_name,sku,asin,item_status,quantity,currency,item_price,item_tax,shipping_price,shipping_tax,gift_wrap_price,gift_wrap_tax,item_promotion_discount,ship_promotion_discount,ship_city,ship_state,ship_postal_code,ship_country,promotion_ids,shop_name)
                VALUES
                 ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');''' \
                    % (amazon_order_id,
                       merchant_order_id,
                       purchase_date,
                       last_updated_date,
                       order_status,
                       fulfillment_channel,
                       sales_channel,
                       order_channel,
                       url,
                       ship_service_level,
                       product_name,
                       sku,
                       asin,
                       item_status,
                       quantity,
                       currency,
                       item_price,
                       item_tax,
                       shipping_price,
                       shipping_tax,
                       gift_wrap_price,
                       gift_wrap_tax,
                       item_promotion_discount,
                       ship_promotion_discount,
                       ship_city,
                       ship_state,
                       ship_postal_code,
                       ship_country,
                       promotion_ids,
                       shop_name)
            print sql_insert
            logging.debug(sql_insert)
            cursor.execute(sql_insert)
        self.db_conn.commit()
        cursor.close()

    def get_last_receive_time(self):
        cursor = self.db_conn.cursor()
        sql_max_time = "select max(received_date) from t_report_fba_fulfillment_inventory_receipts_data where shop_name = '%s' " % (self.auth_info['ShopName'])
        print 'sql_max_time is: %s' % sql_max_time
        cursor.execute(sql_max_time)
        max_time_obj = cursor.fetchone()
        cursor.close()

        if max_time_obj is None or len(max_time_obj) == 0 or max_time_obj[0] is None:
            max_update_time = '2018-01-01'
        else:
            max_update_time = (max_time_obj[0] + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
            if max_update_time == '9999-12-30':  # 人工设置需全量刷新的标志日期 9999-12-31
                max_update_time = '2018-01-01'
        print 'last receive time is %s' % max_update_time
        logging.debug('last receive time is %s' % max_update_time)
        return max_update_time

    def fba_receive_insert(self, get_report_data):
        cursor = self.db_conn.cursor()
        for i, value in enumerate(get_report_data):
            if i == 0:
                continue

            report_data = value.split('\t')
            shop_name = self.auth_info['ShopName']
            received_date = time.strftime("%Y-%m-%d %H:%M:%S",time.strptime(report_data[0][0:19], "%Y-%m-%dT%H:%M:%S"))
            fnsku = report_data[1]
            sku = report_data[2]
            product_name = report_data[3].replace("'", "`")
            quantity = report_data[4]
            fba_shipment_id = report_data[5]
            fulfillment_center_id = report_data[6]

            sql_delete = "delete from t_report_fba_fulfillment_inventory_receipts_data where Shop_Name ='%s' and received_date ='%s' and sku = '%s'" % (shop_name, received_date, sku)
            print sql_delete
            logging.debug(sql_delete)
            cursor.execute(sql_delete)
            sql_insert = "INSERT INTO t_report_fba_fulfillment_inventory_receipts_data(Shop_Name, received_date, fnsku, sku, product_name, quantity, fba_shipment_id, fulfillment_center_id) " \
                         "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'); " %(shop_name, received_date, fnsku, sku, product_name, quantity, fba_shipment_id, fulfillment_center_id)
            print sql_insert
            logging.debug(sql_insert)
            cursor.execute(sql_insert)
        self.db_conn.commit()
        cursor.close()

    def fba_fees_insert(self, get_report_data):
        cursor = self.db_conn.cursor()
        for i, value in enumerate(get_report_data):
            if i == 0:
                continue
            report_data = value.split('\t')

            sku = report_data[0]
            fnsku = report_data[1]
            asin = report_data[2]
            product_name = report_data[3].replace("'", "`")
            product_group = report_data[4].replace("'", "`")
            brand = report_data[5]
            fulfilled_by = report_data[6]
            your_price = report_data[7]
            sales_price = report_data[8]
            longest_side = report_data[9]
            median_side = report_data[10]
            shortest_side = report_data[11]
            length_and_girth = report_data[12]
            unit_of_dimension = report_data[13]
            item_package_weight = report_data[14]
            unit_of_weight = report_data[15]
            product_size_tier = report_data[16]
            currency = report_data[17]
            estimated_fee = report_data[18]
            estimated_referral_fee_per_unit = report_data[19]
            estimated_variable_closing_fee = report_data[20]
            estimated_order_handling_fee_per_order = report_data[21]
            estimated_pick_pack_fee_per_unit = report_data[22]
            if self.auth_info['ShopSite'] not in ('IN', 'AU'):
                estimated_weight_handling_fee_per_unit = report_data[23]
                expected_fulfillment_fee_per_unit = report_data[24]

            if self.auth_info['ShopSite'] == 'AU':
                estimated_order_handling_fee_per_order = ''
                estimated_pick_pack_fee_per_unit = report_data[21]
                estimated_weight_handling_fee_per_unit = report_data[22]
                expected_fulfillment_fee_per_unit = ''

            if self.auth_info['ShopSite'] == 'IN':
                product_size_tier = ''
                currency = report_data[16]
                estimated_fee = report_data[17]
                estimated_referral_fee_per_unit = report_data[18]
                estimated_variable_closing_fee = report_data[19]
                estimated_order_handling_fee_per_order = report_data[20]
                estimated_pick_pack_fee_per_unit = report_data[21]
                estimated_weight_handling_fee_per_unit = report_data[22]
                expected_fulfillment_fee_per_unit = ''


            if self.auth_info['ShopSite'] in ('FR', 'DE', 'UK'):
                your_price = report_data[8]
                sales_price = report_data[9]
                longest_side = report_data[10]
                median_side = report_data[11]
                shortest_side = report_data[12]
                length_and_girth = report_data[13]
                unit_of_dimension = report_data[14]
                item_package_weight = report_data[15]
                unit_of_weight = report_data[16]
                product_size_tier = report_data[17]
                currency = report_data[18]
                estimated_fee = report_data[19]
                estimated_referral_fee_per_unit = report_data[20]
                estimated_variable_closing_fee = report_data[21]

            shop_name = self.auth_info['ShopName']

            sql_delete = "delete from t_amazon_estimated_fba_fees where shop_name ='%s' and sku ='%s' and  asin='%s' " % (self.auth_info['ShopName'], sku, asin)
            print sql_delete
            logging.debug(sql_delete)
            cursor.execute(sql_delete)
            sql_insert = '''INSERT INTO t_amazon_estimated_fba_fees (shop_name, sku, fnsku, asin, product_name, product_group, brand, fulfilled_by, your_price, sales_price, longest_side, median_side, shortest_side, length_and_girth, unit_of_dimension, item_package_weight, unit_of_weight, product_size_tier, currency, estimated_fee, estimated_referral_fee_per_unit, estimated_variable_closing_fee, estimated_order_handling_fee_per_order, estimated_pick_pack_fee_per_unit, estimated_weight_handling_fee_per_unit, expected_fulfillment_fee_per_unit)
                                    values ('%s','%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')
                                ''' % (shop_name, sku, fnsku, asin, product_name, product_group, brand, fulfilled_by, your_price, sales_price, longest_side, median_side, shortest_side, length_and_girth, unit_of_dimension, item_package_weight, unit_of_weight, product_size_tier, currency, estimated_fee, estimated_referral_fee_per_unit, estimated_variable_closing_fee, estimated_order_handling_fee_per_order, estimated_pick_pack_fee_per_unit, estimated_weight_handling_fee_per_unit, expected_fulfillment_fee_per_unit)
            print sql_insert
            logging.debug(sql_insert)
            cursor.execute(sql_insert)
        self.db_conn.commit()
        cursor.close()

    def get_last_remove_time(self):
        cursor = self.db_conn.cursor()
        sql_max_time = "select min(request_date) from t_amazon_removal_order_detail where shop_name = '%s' and in_process_quantity != 0 " % (self.auth_info['ShopName'])
        print 'sql_max_time is: %s' % sql_max_time
        cursor.execute(sql_max_time)
        max_time_obj = cursor.fetchone()
        cursor.close()

        if max_time_obj is None or len(max_time_obj) == 0 or max_time_obj[0] is None:
            max_update_time = '2018-01-01'
        else:
            max_update_time = (max_time_obj[0] + datetime.timedelta(days=-10)).strftime('%Y-%m-%d')
            if max_update_time == '9999-12-30':  # 人工设置需全量刷新的标志日期 9999-12-31
                max_update_time = '2018-01-01'
        print 'last remove time is %s' % max_update_time
        logging.debug('last remove time is %s' % max_update_time)
        return max_update_time

    def remove_order_insert(self, get_report_data):
        cursor = self.db_conn.cursor()
        for i, value in enumerate(get_report_data):
            if i == 0:
                continue

            report_data = value.split('\t')
            shop_name = self.auth_info['ShopName']
            request_date = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(report_data[0][0:19], "%Y-%m-%dT%H:%M:%S"))
            order_id = report_data[1]
            order_type = report_data[2]
            if self.auth_info['ShopSite'] in ('UK', 'FR', 'DE', 'IN'):
                order_status = report_data[4].replace("'", "`")
                last_updated_date = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(report_data[5][0:19], "%Y-%m-%dT%H:%M:%S"))
                sku = report_data[6]
                fnsku = report_data[7]
                disposition = report_data[8]
                requested_quantity = report_data[9]
                cancelled_quantity = report_data[10]
                disposed_quantity = report_data[11]
                shipped_quantity = report_data[12]
                in_process_quantity = report_data[13]
                removal_fee = report_data[14]
            else:
                order_status = report_data[3].replace("'", "`")
                last_updated_date = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(report_data[4][0:19], "%Y-%m-%dT%H:%M:%S"))
                sku = report_data[5]
                fnsku = report_data[6]
                disposition = report_data[7]
                requested_quantity = report_data[8]
                cancelled_quantity = report_data[9]
                disposed_quantity = report_data[10]
                shipped_quantity = report_data[11]
                in_process_quantity = report_data[12]
                removal_fee = report_data[13]

            sql_delete = "delete from t_amazon_removal_order_detail where Shop_Name ='%s' and request_date ='%s' and sku = '%s' and order_id ='%s'" % (shop_name, request_date, sku, order_id)
            print sql_delete
            logging.debug(sql_delete)
            cursor.execute(sql_delete)
            sql_insert = "INSERT INTO t_amazon_removal_order_detail(shop_name, request_date, order_id, order_type, order_status, last_updated_date, sku, fnsku, disposition, requested_quantity, cancelled_quantity, disposed_quantity, shipped_quantity, in_process_quantity, removal_fee) " \
                         "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'); " % (shop_name, request_date, order_id, order_type, order_status, last_updated_date, sku, fnsku, disposition, requested_quantity, cancelled_quantity, disposed_quantity, shipped_quantity, in_process_quantity, removal_fee)
            print sql_insert
            logging.debug(sql_insert)
            cursor.execute(sql_insert)
        self.db_conn.commit()
        cursor.close()

    def shop_update_all(self, col, value, value_all):
        if self.auth_info['ShopSite'] == 'JP':
            if self.auth_info['ShopSite'] == 'JP':
                item_name = value_all[0]
                listing_id = value_all[1]
                seller_sku = value_all[2]
                price = value_all[3]
                quantity = value_all[4]
                open_date = value_all[5]
                product_id_type = value_all[6]
                item_note = value_all[7]
                item_condition = value_all[8]
                zshop_category1 = value_all[9]
                expedited_shipping = value_all[10]
                product_id = value_all[11]
                pending_quantity = value_all[12]
                fulfillment_channel = value_all[13]
                merchant_shipping_group = value_all[14]
                status = value_all[15]

                sql_insert = 'insert into %s ( item_name,listing_id,seller_sku,price,quantity,open_date,product_id_type,item_note,item_condition,zshop_category1,expedited_shipping,product_id,pending_quantity,fulfillment_channel,merchant_shipping_group,status, shopname, shopsite) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' \
                             % (self.auth_info['table_name'], item_name, listing_id, seller_sku, price, quantity, open_date, product_id_type, item_note, item_condition, zshop_category1,
                                expedited_shipping, product_id, pending_quantity, fulfillment_channel, merchant_shipping_group, status, self.auth_info['ShopName'], self.auth_info['ShopSite'])
        else:
            sql_insert = "insert into %s ( %s, shopname, shopsite) values (%s, '%s', '%s')" \
                         % (self.auth_info['table_name'], col, value, self.auth_info['ShopName'], self.auth_info['ShopSite'])
        print '\n sql_insert is %s' % sql_insert
        logging.debug('sql_insert is %s' % sql_insert)
        self.execute_db(sql_insert)

    def get_column(self, report_result_data):
        for i, value in enumerate(report_result_data):
            if i == 0:  # get  information's column
                report_result_data_column = value.split('\t')
                table_column = str(report_result_data_column)
                table_column = table_column.replace('[', '')
                table_column = table_column.replace(']', '')
                table_column = table_column.replace("'", '')
                table_column = table_column.replace('-', '_')
                break
        return table_column

    def get_value(self, value):
        report_result_data = value.split('\t')
        table_val = str(report_result_data)
        table_val = table_val[1:-1]
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

        sql_price_history = '''
        insert into t_online_info_amazon_price
          (shopname, ShopSite, seller_sku, asin1, price, UpdateTime)
          SELECT a.shopname,
                 a.ShopSite,
                 a.seller_sku,
                 a.asin1,
                 a.price,
                 a.UpdateTime
            FROM t_online_info_amazon a,
                 (select shopname,
                         ShopSite,
                         seller_sku,
                         asin1,
                         price,
                         UpdateTime,
                         rank
                    from (select price_log.shopname,
                                 price_log.ShopSite,
                                 price_log.seller_sku,
                                 price_log.asin1,
                                 price_log.price,
                                 price_log.UpdateTime,
                                 @rownum := @rownum + 1,
                                 if(@pdept = price_log.seller_sku,
                                    @rank := @rank + 1,
                                    @rank := 1) as rank,
                                 @pdept := price_log.seller_sku
                            from (select shopname,
                                         ShopSite,
                                         seller_sku,
                                         asin1,
                                         price,
                                         UpdateTime
                                    from t_online_info_amazon_price
                                   where ShopName = '%s'
                                   order by seller_sku, UpdateTime desc) price_log,
                                 (select @rownum := 0, @pdept := null, @rank := 0) a) c
                   where rank = 1) b
           WHERE a.ShopName = b.ShopName
             AND a.seller_sku = b.seller_sku
             and a.price != b.price
             AND a.ShopName = '%s';
        ''' % (self.auth_info['ShopName'], self.auth_info['ShopName'])

        sql_del_history = "delete from t_online_info_amazon_history where shopname = '%s';" % self.auth_info['ShopName']

        sql_insert_history  = '''
        INSERT INTO t_online_info_amazon_history (item_name,item_description,listing_id,seller_sku,price,quantity,open_date,image_url,item_is_marketplace,product_id_type,zshop_shipping_fee,item_note,item_condition,zshop_category1,zshop_browse_path,zshop_storefront_feature,asin1,asin2,asin3,will_ship_internationally,expedited_shipping,zshop_boldface,product_id,bid_for_featured_placement,add_delete,pending_quantity,fulfillment_channel,merchant_shipping_group,ShopName,SKU,UpdateTime,order7days,orderydays,ordertdays,ordercdays,allorder,order3days,Status,deal_action,deal_result,deal_result_info,product_type,ShopSite,Parent_asin,bullet_point1,bullet_point2,bullet_point3,bullet_point4,bullet_point5,product_description,sale_price,sale_from_date,sale_end_date,generic_keywords1,generic_keywords2,generic_keywords3,generic_keywords4,generic_keywords5,is_fba,orders_7days,afn_listing_exists,afn_warehouse_quantity,inventory_received_date,refresh_status,refresh_remark,shipping_price,last_price,last_price_time,estimated_fee) 
        SELECT item_name,item_description,listing_id,seller_sku,price,quantity,open_date,image_url,item_is_marketplace,product_id_type,zshop_shipping_fee,item_note,item_condition,zshop_category1,zshop_browse_path,zshop_storefront_feature,asin1,asin2,asin3,will_ship_internationally,expedited_shipping,zshop_boldface,product_id,bid_for_featured_placement,add_delete,pending_quantity,fulfillment_channel,merchant_shipping_group,ShopName,SKU,UpdateTime,order7days,orderydays,ordertdays,ordercdays,allorder,order3days,Status,deal_action,deal_result,deal_result_info,product_type,ShopSite,Parent_asin,bullet_point1,bullet_point2,bullet_point3,bullet_point4,bullet_point5,product_description,sale_price,sale_from_date,sale_end_date,generic_keywords1,generic_keywords2,generic_keywords3,generic_keywords4,generic_keywords5,is_fba,orders_7days,afn_listing_exists,afn_warehouse_quantity,inventory_received_date,refresh_status,refresh_remark,shipping_price,last_price,last_price_time,estimated_fee
        FROM t_online_info_amazon
        WHERE shopname = '%s'
        AND seller_sku not IN (SELECT seller_sku FROM t_online_info_amazon_for_update WHERE shopname = '%s');
        ''' % (self.auth_info['ShopName'], self.auth_info['ShopName'])

        sql_update_history = "update t_online_info_amazon_history set refresh_status = 1 where shopname = '%s';" % self.auth_info['ShopName']

        sql_del = "delete from %s where shopname = '%s'" % (self.auth_info['table_name_really'], self.auth_info['ShopName'])
        # sql_del = "delete from %s where shopname = '%s' and seller_sku in (select seller_sku from %s where shopname = '%s')" \
        #           % (self.auth_info['table_name_really'], self.auth_info['ShopName'], self.auth_info['table_name'], self.auth_info['ShopName'])

        # sql_status_update = "update %s set refresh_status = 1 where shopname = '%s'" % (self.auth_info['table_name_really'], self.auth_info['ShopName'])

        sql_insert = "insert into %s (item_name,item_description,listing_id,seller_sku,price,quantity,open_date,image_url,item_is_marketplace,product_id_type,zshop_shipping_fee,item_note,item_condition,zshop_category1,zshop_browse_path,zshop_storefront_feature,asin1,asin2,asin3,will_ship_internationally,expedited_shipping,zshop_boldface,product_id,bid_for_featured_placement,add_delete,pending_quantity,fulfillment_channel,merchant_shipping_group,ShopName,SKU,UpdateTime,order7days,orderydays,ordertdays,ordercdays,allorder,order3days,Status,deal_action,deal_result,deal_result_info,product_type,ShopSite,Parent_asin,bullet_point1,bullet_point2,bullet_point3,bullet_point4,bullet_point5,product_description,sale_price,sale_from_date,sale_end_date,generic_keywords1,generic_keywords2,generic_keywords3,generic_keywords4,generic_keywords5) select item_name,item_description,listing_id,seller_sku,price,quantity,open_date,image_url,item_is_marketplace,product_id_type,zshop_shipping_fee,item_note,item_condition,zshop_category1,zshop_browse_path,zshop_storefront_feature,asin1,asin2,asin3,will_ship_internationally,expedited_shipping,zshop_boldface,product_id,bid_for_featured_placement,add_delete,pending_quantity,fulfillment_channel,merchant_shipping_group,ShopName,SKU,UpdateTime,order7days,orderydays,ordertdays,ordercdays,allorder,order3days,Status,deal_action,deal_result,deal_result_info,product_type,ShopSite,Parent_asin,bullet_point1,bullet_point2,bullet_point3,bullet_point4,bullet_point5,product_description,sale_price,sale_from_date,sale_end_date,generic_keywords1,generic_keywords2,generic_keywords3,generic_keywords4,generic_keywords5 from  %s where shopname = '%s'" \
                     % (self.auth_info['table_name_really'], self.auth_info['table_name'], self.auth_info['ShopName'])

        sql_remove_record_insert = '''
        INSERT INTO t_online_info_amazon (item_name,item_description,listing_id,seller_sku,price,quantity,open_date,image_url,item_is_marketplace,product_id_type,zshop_shipping_fee,item_note,item_condition,zshop_category1,zshop_browse_path,zshop_storefront_feature,asin1,asin2,asin3,will_ship_internationally,expedited_shipping,zshop_boldface,product_id,bid_for_featured_placement,add_delete,pending_quantity,fulfillment_channel,merchant_shipping_group,ShopName,SKU,UpdateTime,order7days,orderydays,ordertdays,ordercdays,allorder,order3days,Status,deal_action,deal_result,deal_result_info,product_type,ShopSite,Parent_asin,bullet_point1,bullet_point2,bullet_point3,bullet_point4,bullet_point5,product_description,sale_price,sale_from_date,sale_end_date,generic_keywords1,generic_keywords2,generic_keywords3,generic_keywords4,generic_keywords5,is_fba,orders_7days,afn_listing_exists,afn_warehouse_quantity,inventory_received_date,refresh_status,refresh_remark,shipping_price,last_price,last_price_time,estimated_fee) 
        SELECT item_name,item_description,listing_id,seller_sku,price,quantity,open_date,image_url,item_is_marketplace,product_id_type,zshop_shipping_fee,item_note,item_condition,zshop_category1,zshop_browse_path,zshop_storefront_feature,asin1,asin2,asin3,will_ship_internationally,expedited_shipping,zshop_boldface,product_id,bid_for_featured_placement,add_delete,pending_quantity,fulfillment_channel,merchant_shipping_group,ShopName,SKU,UpdateTime,order7days,orderydays,ordertdays,ordercdays,allorder,order3days,Status,deal_action,deal_result,deal_result_info,product_type,ShopSite,Parent_asin,bullet_point1,bullet_point2,bullet_point3,bullet_point4,bullet_point5,product_description,sale_price,sale_from_date,sale_end_date,generic_keywords1,generic_keywords2,generic_keywords3,generic_keywords4,generic_keywords5,is_fba,orders_7days,afn_listing_exists,afn_warehouse_quantity,inventory_received_date,refresh_status,refresh_remark,shipping_price,last_price,last_price_time,estimated_fee
        FROM t_online_info_amazon_history
        where shopname = '%s'
        ''' % self.auth_info['ShopName']

        sql_update_history_price2 = '''
                  update t_online_info_amazon a,
                       (select shopname,
                               ShopSite,
                               seller_sku,
                               asin1,
                               price,
                               UpdateTime,
                               rank
                          from (select price_log.shopname,
                                       price_log.ShopSite,
                                       price_log.seller_sku,
                                       price_log.asin1,
                                       price_log.price,
                                       price_log.UpdateTime,
                                       @rownum := @rownum + 1,
                                       if(@pdept = price_log.seller_sku,
                                          @rank := @rank + 1,
                                          @rank := 1) as rank,
                                       @pdept := price_log.seller_sku
                                  from (select shopname,
                                               ShopSite,
                                               seller_sku,
                                               asin1,
                                               price,
                                               UpdateTime
                                          from t_online_info_amazon_price
                                         where ShopName = '%s'
                                         order by seller_sku, UpdateTime desc) price_log,
                                       (select @rownum := 0, @pdept := null, @rank := 0) a) c
                         where rank = 2) b
                   set a.last_price = b.price, a.last_price_time = b.UpdateTime
                 WHERE a.ShopName = b.ShopName
                   AND a.seller_sku = b.seller_sku
                   and a.price != b.price
                   AND a.ShopName = '%s';
                   ''' % (self.auth_info['ShopName'], self.auth_info['ShopName'])

        sql_update_history_price1 = '''
          update t_online_info_amazon a,
               (select shopname,
                       ShopSite,
                       seller_sku,
                       asin1,
                       price,
                       UpdateTime,
                       rank
                  from (select price_log.shopname,
                               price_log.ShopSite,
                               price_log.seller_sku,
                               price_log.asin1,
                               price_log.price,
                               price_log.UpdateTime,
                               @rownum := @rownum + 1,
                               if(@pdept = price_log.seller_sku,
                                  @rank := @rank + 1,
                                  @rank := 1) as rank,
                               @pdept := price_log.seller_sku
                          from (select shopname,
                                       ShopSite,
                                       seller_sku,
                                       asin1,
                                       price,
                                       UpdateTime
                                  from t_online_info_amazon_price
                                 where ShopName = '%s'
                                 order by seller_sku, UpdateTime desc) price_log,
                               (select @rownum := 0, @pdept := null, @rank := 0) a) c
                 where rank = 1) b
           set a.last_price = b.price, a.last_price_time = b.UpdateTime
         WHERE a.ShopName = b.ShopName
           AND a.seller_sku = b.seller_sku
           and a.price != b.price
           AND a.ShopName = '%s';
           ''' % (self.auth_info['ShopName'], self.auth_info['ShopName'])

        print 'sql_relation is: %s' % sql_relation
        logging.debug('sql_relation is: %s' % sql_relation)
        self.execute_db(sql_relation)

        # print 'sql_price_delete is: %s' % sql_price_delete
        # logging.debug('sql_price_delete is: %s' % sql_price_delete)
        # self.execute_db(sql_price_delete)

        print 'sql_price_history is: %s' % sql_price_history
        logging.debug('sql_price_history is: %s' % sql_price_history)
        self.execute_db(sql_price_history)

        print 'sql_del_history is: %s' % sql_del_history
        logging.debug('sql_del_history is: %s' % sql_del_history)
        self.execute_db(sql_del_history)

        print 'sql_insert_history is: %s' % sql_insert_history
        logging.debug('sql_insert_history is: %s' % sql_insert_history)
        self.execute_db(sql_insert_history)

        print 'sql_update_history is: %s' % sql_update_history
        logging.debug('sql_update_history is: %s' % sql_update_history)
        self.execute_db(sql_update_history)

        print 'sql_del is: %s' % sql_del
        logging.debug('sql_del is: %s' % sql_del)
        self.execute_db(sql_del)

        print 'sql_insert is: %s' % sql_insert
        logging.debug('sql_insert is: %s' % sql_insert)
        self.execute_db(sql_insert)

        print 'sql_remove_record_insert is: %s' % sql_remove_record_insert
        logging.debug('sql_remove_record_insert is: %s' % sql_remove_record_insert)
        self.execute_db(sql_remove_record_insert)

        print 'sql_update_history_price2 is: %s' % sql_update_history_price2
        logging.debug('sql_update_history_price2 is: %s' % sql_update_history_price2)
        self.execute_db(sql_update_history_price2)

        print 'sql_update_history_price1 is: %s' % sql_update_history_price1
        logging.debug('sql_update_history_price1 is: %s' % sql_update_history_price1)
        self.execute_db(sql_update_history_price1)

    def execute_db(self, sql):
        cursor = self.db_conn.cursor()
        try:
            cursor.execute(sql)
            cursor.execute('commit;')
            cursor.close()
            logging.debug('sql execute success')
        except Exception as e:
            cursor.close()
            logging.error('sql execute failed!')
            logging.error('traceback.format_exc():\n%s' % traceback.format_exc())
            print e

    def update_shop_status_public(self, report_type, auth_info_public, begin_time, end_time, status, remark):
        if report_type == '_GET_FBA_MYI_ALL_INVENTORY_DATA_':
            column_name = 'fba'
        elif report_type == '_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_':
            column_name = 'order'
        elif report_type == '_GET_MERCHANT_LISTINGS_ALL_DATA_':
            column_name = 'product'
        elif report_type == '_GET_FBA_FULFILLMENT_INVENTORY_RECEIPTS_DATA_':
            column_name = 'receive'
        elif report_type == '_GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA_':
            column_name = 'fee'
        elif report_type == '_GET_FBA_FULFILLMENT_REMOVAL_ORDER_DETAIL_DATA_':
            column_name = 'remove'
        else:
            column_name = ''

        cursor = self.db_conn.cursor()
        sql_record_exists = "select  name from t_perf_amazon_refresh_status where name = '%s'" % auth_info['ShopName']
        cursor.execute(sql_record_exists)
        shop_exists_obj = cursor.fetchone()
        if shop_exists_obj is None or shop_exists_obj[0] is None:
            sql_insert = '''
                insert into t_perf_amazon_refresh_status
                  (name,
                   shop_name,
                   shop_site,
                   IP,
                   %s,
                   %s,
                   %s,
                   %s)
                values
                  ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
                ''' % (column_name + '_refresh_begin_time',
                       column_name + '_refresh_end_time',
                       column_name + '_refresh_status',
                       column_name + '_refresh_remark',
                       auth_info_public['ShopName'],
                       auth_info_public['ShopName'][0:8],
                       auth_info_public['ShopSite'],
                       auth_info_public['ShopIP'],
                       begin_time,
                       end_time,
                       status,
                       remark)
            logging.debug(sql_insert)
            cursor.execute(sql_insert)
            cursor.execute('commit;')
        else:
            sql_update = '''
            update t_perf_amazon_refresh_status
               set %s = '%s',
                   %s   = '%s',
                   %s     = '%s',
                   %s     = '%s'
             where name = '%s'
            ''' % (column_name + '_refresh_begin_time',
                   begin_time,
                   column_name + '_refresh_end_time',
                   end_time,
                   column_name + '_refresh_status',
                   status,
                   column_name + '_refresh_remark',
                   remark,
                   auth_info_public['ShopName'])
            logging.debug(sql_update)
            cursor.execute(sql_update)
            cursor.execute('commit;')
        cursor.close()


class GetProductInfoBySellerSku:
    """
    按seller_sku值获取产品图片及主、变体关系
    """

    def __init__(self, auth_info, DATABASE):
        self.db_conn = pymysql.connect(DATABASE['HOST'],
                                       DATABASE['USER'],
                                       DATABASE['PASSWORD'],
                                       DATABASE['NAME'])
        self.auth_info = auth_info
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
            logging.error('class GetProductInfoBySellerSku close db connection failed!' )
            logging.error('traceback.format_exc():\n%s' % traceback.format_exc())

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
                  % (self.auth_info['table_name'], this_asin, image_url, seller_sku, self.auth_info['ShopName'])
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
            try:
                self.update_db_by_product_info(product_info, seller_sku)
            except Exception as e:
                print 'exception seller_sku is：%s' % str(seller_sku)
                logging.debug('exception seller_sku is：%s' % str(seller_sku))
                logging.error('traceback.format_exc():\n%s' % traceback.format_exc())
                print e
        else:
            print 'get product_info by seller_sku fail'
            logging.debug('get product_info by seller_sku error')


class GetProductInfoByAsin:
    """
     按asin值获取产品图片及主、变体关系
    """

    def __init__(self, auth_info):
        self.db_conn = pymysql.connect(DATABASE['HOST'],
                                       DATABASE['USER'],
                                       DATABASE['PASSWORD'],
                                       DATABASE['NAME'])
        self.auth_info = auth_info
        self.product_public = Products(self.auth_info['AWSAccessKeyId'],
                                       self.auth_info['SecretKey'],
                                       self.auth_info['SellerId'],
                                       self.auth_info['ShopSite']
                                       )

    def close_db_conn(self):
        try:
            if self.db_conn:
                self.db_conn.close()
        except Exception as ex:
            print ex
            logging.error('class  GetProductInfoByAsin close db connection failed!' )
            logging.error('traceback.format_exc():\n%s' % traceback.format_exc())

    def get_product_info(self, asin_list):
        try:
            product_info_response = self.product_public.get_matching_product(self.auth_info['MarketplaceId'], asin_list)
            product_info_response_dic = product_info_response._response_dict
        except Exception as e:
            logging.error(e)
            time.sleep(30)  # 防止超请求限制，重新提交
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
        logging.debug('connect_image sql is: %s' % sql)
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
        try:
            cursor = self.db_conn.cursor()
            if seller_sku_list is None:
                sql = "select asin1,seller_sku, status from %s where shopname = '%s' and refresh_status != 1" \
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
                asin_list = []
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
                        sku_obj = GetProductInfoBySellerSku(self.auth_info, DATABASE)
                        sku_obj.refresh_data_by_seller_sku(asin_status[1])
                        sku_obj.close_db_conn()
                print asin_list
                asin_list = list(set(asin_list))
                print 'asin_list is: %s' % str(asin_list)
                logging.debug('asin_list is: %s' % str(asin_list))
                if asin_list:
                    product_info = self.get_product_info(asin_list)
                    logging.debug('product_info is: %s' % str(product_info))
                    self.update_db_by_product_info(product_info)
                self.refresh_product()
        except Exception as e:
            print e
            logging.debug('----------------------------------get_image fail-----------------------------------------------')
            logging.error('traceback.format_exc():\n%s' % traceback.format_exc())


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

            sql = "select seller_sku, status from %s where shopname = '%s' and refresh_status != 1" \
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
                    # rank_list = resp_each.get('Product').get('SalesRankings').get('SalesRank')
                    # if isinstance(rank_list, list):
                    #     for rank in rank_list:
                    #         print rank.get('Rank').get('value')
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
                # rank_list = resp_dict.get('Product').get('SalesRankings').get('SalesRank')
                # if isinstance(rank_list, list):
                #     for rank in rank_list:
                #         print rank.get('Rank').get('value')

    def execute_db(self, sql):
        cursor = self.db_conn.cursor()
        try:
            cursor.execute(sql)
            cursor.execute('commit;')
            cursor.close()
        except Exception as e:
            cursor.close()
            print e
            logging.error('traceback.format_exc():\n%s' % traceback.format_exc())


class GetLocalIPAndAuthInfo:
    """
    获取当前vps服务器IP；从数据库获取MQ信息
    """

    def __init__(self):
        self.db_conn = pymysql.connect(DATABASE['HOST'],
                                       DATABASE['USER'],
                                       DATABASE['PASSWORD'],
                                       DATABASE['NAME'])

    def close_db_conn(self):
        try:
            if self.db_conn:
                self.db_conn.close()
        except Exception as ex:
            print ex
            logging.error('class  GetLocalIPAndAuthInfo close db connection failed!' )
            logging.error('traceback.format_exc():\n%s' % traceback.format_exc())

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

    def get_auth_info_by_ip(self, ip):
        cursor = self.db_conn.cursor()
        sql = "select IP,Name,K,V, site from t_config_online_amazon  where IP= '%s'" % ip
        print sql
        cursor.execute(sql)
        t_config_online_amazon_objs = cursor.fetchall()
        print t_config_online_amazon_objs
        cursor.close()
        auth_info_all = dict()
        for t_config_obj in t_config_online_amazon_objs:
            if t_config_obj[1] in auth_info_all:
                auth_info_all[t_config_obj[1]]['ShopIP'] = ip
                auth_info_all[t_config_obj[1]]['update_type'] = 'refresh_ad_data'
                auth_info_all[t_config_obj[1]]['table_name'] = 't_online_info_amazon'
                auth_info_all[t_config_obj[1]]['ShopName'] = t_config_obj[1]
                auth_info_all[t_config_obj[1]]['ShopSite'] = t_config_obj[4]
                auth_info_all[t_config_obj[1]][t_config_obj[2]] = t_config_obj[3]
            else:
                auth_info_all[t_config_obj[1]] = dict()
                auth_info_all[t_config_obj[1]][t_config_obj[2]] = t_config_obj[3]
        return auth_info_all


auto_upgrade()

try:
    delete_history_log('.log', 7)
except Exception as e:
    logging.error('delete history log file failed')
    logging.error('traceback.format_exc():\n%s' % traceback.format_exc())

get_info_obj = GetLocalIPAndAuthInfo()
while True:
    try:
        local_ip = get_info_obj.get_out_ip(get_info_obj.get_real_url())
        if local_ip is not None:
            if local_ip == '47.254.83.145':
                local_ip = '210.16.103.56'  # 160
            elif local_ip == '47.251.3.95':
                local_ip = '103.95.13.105'  # 201
            else:
                pass
            print 'local ip is: %s' % local_ip
            logging.debug('local ip is: %s' % local_ip)
            break
    except Exception as e:
        print e
        local_ip = None


auth_info_all = get_info_obj.get_auth_info_by_ip(local_ip)
get_info_obj.close_db_conn()
print 'auth_info_all is: %s' % str(auth_info_all)
logging.debug('auth_info_all is: %s' % str(auth_info_all))
for key, val in auth_info_all.items():
    auth_info = val
    print 'auth_info now is: %s ' % str(auth_info)
    logging.debug('auth_info now is: %s ' % str(auth_info))
    try:
        print '----------------------------------site begin-----------------------------------------------'
        logging.debug('----------------------------------site begin-----------------------------------------------')
        auth_info['table_name_really'] = auth_info['table_name']
        auth_info['table_name'] = auth_info['table_name'] + '_for_update'
        get_data_public_obj = ReportPublic(auth_info)

        get_data_public_obj.report_flow('_GET_FBA_MYI_ALL_INVENTORY_DATA_')

        submit_time_list = get_data_public_obj.get_last_order_time()
        for i in range(len(submit_time_list) - 1):
            start_date_order = submit_time_list[i]
            end_date_order = submit_time_list[i + 1]
            get_data_public_obj.report_flow('_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_', start_date_order, end_date_order)

        start_date_receive = get_data_public_obj.get_last_receive_time()
        end_date_receive = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        get_data_public_obj.report_flow('_GET_FBA_FULFILLMENT_INVENTORY_RECEIPTS_DATA_', start_date_receive, end_date_receive)

        get_data_public_obj.report_flow('_GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA_')

        start_date_remove = get_data_public_obj.get_last_remove_time()
        end_date_remove = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        get_data_public_obj.report_flow('_GET_FBA_FULFILLMENT_REMOVAL_ORDER_DETAIL_DATA_', start_date_remove, end_date_remove)

        get_data_public_obj.delete_mid_table()
        get_data_public_obj.report_flow('_GET_MERCHANT_LISTINGS_ALL_DATA_')
        auth_info['table_name'] = auth_info['table_name_really']

        refresh_db_tables(auth_info, get_data_public_obj)

        get_data_public_obj.close_db_conn()

        ship_price_obj = GetShippingPrice(auth_info, DATABASE)
        ship_price_obj.get_seller_sku_list()
        ship_price_obj.close_db_conn()

        get_product_info_obj = GetProductInfoByAsin(auth_info)
        get_product_info_obj.get_parent_asin_and_image()
        get_product_info_obj.close_db_conn()

        print '----------------------------------site end-----------------------------------------------'
        logging.debug('----------------------------------site end-----------------------------------------------')
    except Exception as e:
        logging.debug('----------------------------------site fail-----------------------------------------------')
        logging.error('traceback.format_exc():\n%s' % traceback.format_exc())


