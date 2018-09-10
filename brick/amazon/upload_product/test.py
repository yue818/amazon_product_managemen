# -*- coding:utf-8 -*-

"""
 @desc:
 @author: wuchongxiang
 @site:
 @software: PyCharm
 @file: fba_refresh-20180801.py
 @time: 2018/8/1 14:51
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
                                       DATABASE['NAME'])

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
        report_result_data = report_result.original.splitlines()
        logging.debug('end get result data')
        return report_result_data

    def report_flow(self, report_type, start_date=None, end_date=None):
        begin_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_request_id = self.submit_report_request(report_type, start_date, end_date)
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

    def insert_public(self, report_type, get_report_data):
        if report_type == '_GET_FBA_MYI_ALL_INVENTORY_DATA_':
            self.fba_insert(get_report_data)
        elif report_type == '_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_':
            self.order_insert(get_report_data)
        elif report_type == '_GET_FBA_FULFILLMENT_INVENTORY_RECEIPTS_DATA_':
            self.fba_receive_insert(get_report_data)
        elif report_type == '_GET_MERCHANT_LISTINGS_ALL_DATA_':
            table_column = self.get_column(get_report_data)
            for i, value in enumerate(get_report_data):
                if i == 0:
                    continue
                table_val = self.get_value(value)
                self.shop_update_all(table_column, table_val)
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
                (sku,
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
                 RefreshTime,
                 ShopName)
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
            ship_city = report_data[24]
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
                  (amazon_order_id,
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

    def shop_update_all(self, col, value):
        if self.auth_info['ShopSite'] == 'JP':
            sql_insert = "insert into %s ( item_name,listing_id,seller_sku,price,quantity,open_date,product_id_type,item_note,item_condition,zshop_category1,expedited_shipping,product_id,pending_quantity,fulfillment_channel,merchant_shipping_group,status, shopname, shopsite) values (%s, '%s', '%s')" \
                         % (self.auth_info['table_name'], value, self.auth_info['ShopName'], self.auth_info['ShopSite'])
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

        sql_del = "delete from %s where shopname = '%s'" % (self.auth_info['table_name_really'], self.auth_info['ShopName'])
        sql_insert = "insert into %s (item_name,item_description,listing_id,seller_sku,price,quantity,open_date,image_url,item_is_marketplace,product_id_type,zshop_shipping_fee,item_note,item_condition,zshop_category1,zshop_browse_path,zshop_storefront_feature,asin1,asin2,asin3,will_ship_internationally,expedited_shipping,zshop_boldface,product_id,bid_for_featured_placement,add_delete,pending_quantity,fulfillment_channel,merchant_shipping_group,ShopName,SKU,UpdateTime,order7days,orderydays,ordertdays,ordercdays,allorder,order3days,Status,deal_action,deal_result,deal_result_info,product_type,ShopSite,Parent_asin,bullet_point1,bullet_point2,bullet_point3,bullet_point4,bullet_point5,product_description,sale_price,sale_from_date,sale_end_date,generic_keywords1,generic_keywords2,generic_keywords3,generic_keywords4,generic_keywords5) select item_name,item_description,listing_id,seller_sku,price,quantity,open_date,image_url,item_is_marketplace,product_id_type,zshop_shipping_fee,item_note,item_condition,zshop_category1,zshop_browse_path,zshop_storefront_feature,asin1,asin2,asin3,will_ship_internationally,expedited_shipping,zshop_boldface,product_id,bid_for_featured_placement,add_delete,pending_quantity,fulfillment_channel,merchant_shipping_group,ShopName,SKU,UpdateTime,order7days,orderydays,ordertdays,ordercdays,allorder,order3days,Status,deal_action,deal_result,deal_result_info,product_type,ShopSite,Parent_asin,bullet_point1,bullet_point2,bullet_point3,bullet_point4,bullet_point5,product_description,sale_price,sale_from_date,sale_end_date,generic_keywords1,generic_keywords2,generic_keywords3,generic_keywords4,generic_keywords5 from  %s where shopname = '%s'" \
                     % (self.auth_info['table_name_really'], self.auth_info['table_name'], self.auth_info['ShopName'])
        print 'sql_relation is: %s' % sql_relation
        logging.debug('sql_relation is: %s' % sql_relation)
        self.execute_db(sql_relation)
        print 'sql_del is: %s' % sql_del
        logging.debug('sql_del is: %s' % sql_del)
        self.execute_db(sql_del)
        print 'sql_insert is: %s' % sql_insert
        logging.debug('sql_insert is: %s' % sql_insert)
        self.execute_db(sql_insert)

    def execute_db(self, sql):
        cursor = self.db_conn.cursor()
        try:
            cursor.execute(sql)
            cursor.execute('commit;')
            cursor.close()
        except Exception as e:
            cursor.close()
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
            print asin_list
            asin_list = list(set(asin_list))
            print 'asin_list is: %s' % str(asin_list)
            logging.debug('asin_list is: %s' % str(asin_list))
            if asin_list:
                product_info = self.get_product_info(asin_list)
                logging.debug('product_info is: %s' % str(product_info))
                self.update_db_by_product_info(product_info)
            self.refresh_product()


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
        cursor = self.db_conn.cursor()

        sql = "select seller_sku, status from %s where shopname = '%s'" \
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

    def update_db_by_price_info(self, price_info):
        resp_obj = price_info.get('GetCompetitivePricingForSKUResult')
        if isinstance(resp_obj, list):
            resp_list = resp_obj
            for resp_each in resp_list:
                print resp_each.get('status').get('value')
                if resp_each.get('status').get('value') == 'Success':
                    sku = resp_each.get('Product').get('Identifiers').get('SKUIdentifier').get('SellerSKU').get('value')
                    if resp_each.get('Product').get('CompetitivePricing').get('CompetitivePrices').get('CompetitivePrice') is not None:
                        ship_price = resp_each.get('Product').get('CompetitivePricing').get('CompetitivePrices').get('CompetitivePrice').get('Price').get('Shipping').get('Amount').get('value')
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
        sql = "select IP,Name,K,V, site from t_config_online_amazon  where IP= '%s' and site != 'JP' " % ip
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
            print 'local ip is: %s' % local_ip
            logging.debug('local ip is: %s' % local_ip)
            break
    except Exception as e:
        print e
        local_ip = None

auth_info_all = get_info_obj.get_auth_info_by_ip(local_ip)
print 'auth_info_all is: %s' % str(auth_info_all)
logging.debug('auth_info_all is: %s' % str(auth_info_all))
for key, val in auth_info_all.items():
    auth_info = val
    print 'auth_info now is: %s ' % str(auth_info)
    logging.debug('auth_info now is: %s ' % str(auth_info))
    try:
        print '----------------------------------site begin-----------------------------------------------'
        ship_price_obj = GetShippingPrice(auth_info, DATABASE)
        ship_price_obj.get_seller_sku_list()
        print '----------------------------------site end-----------------------------------------------'
        logging.debug('----------------------------------site end-----------------------------------------------')
    except Exception as e:
        logging.debug('----------------------------------site fail-----------------------------------------------')
        logging.error('traceback.format_exc():\n%s' % traceback.format_exc())


