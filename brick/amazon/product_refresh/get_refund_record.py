# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: get_refund_record.py
 @time: 2018/9/14 9:06
"""
import mws
import pymysql
import datetime
import logging.handlers
import time

log_day = datetime.datetime.now().strftime("%Y%m%d")
log_file_name = 'get_finance' + log_day + '.log'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(filename)s %(funcName)s:%(lineno)d] %(thread)d %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=log_file_name,
                    filemode='a')

logging.handlers.RotatingFileHandler(log_file_name,
                                     maxBytes=20 * 1024 * 1024,
                                     backupCount=10)


class FinancesPublic:
    def __init__(self, auth_info_public, data_base=None):
        self.auth_info = auth_info_public
        self.finance_public = mws.Finances(self.auth_info['AWSAccessKeyId'],
                                           self.auth_info['SecretKey'],
                                           self.auth_info['SellerId'],
                                           self.auth_info['ShopSite']
                                          )
        self.db_conn = pymysql.connect(data_base['HOST'],
                                       data_base['USER'],
                                       data_base['PASSWORD'],
                                       data_base['NAME'],
                                       charset='utf8')

    def get_finance_report(self, begin_time=None, next_token=None):
        finance_report = self.finance_public.list_financial_events(posted_after=begin_time, next_token=next_token)
        finance_report_dict = finance_report._response_dict
        logging.debug('get data raw:%s' % finance_report_dict)
        return finance_report_dict

    def get_last_refund_time(self):
        cursor = self.db_conn.cursor()
        sql_max_time = "select max(posted_date) from t_amazon_finance_record where shop_name = '%s' " % (self.auth_info['ShopName'])
        print 'sql_max_time is: %s' % sql_max_time
        cursor.execute(sql_max_time)
        max_time_obj = cursor.fetchone()
        cursor.close()

        if max_time_obj is None or len(max_time_obj) == 0 or max_time_obj[0] is None:
            max_update_time = '2018-08-01'
        else:
            max_update_time = (max_time_obj[0] + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
            if max_update_time == '9999-12-30':  # 人工设置需全量刷新的标志日期 9999-12-31
                max_update_time = '2018-08-01'
        print 'last refund time is %s' % max_update_time
        logging.debug('last refund time is %s' % max_update_time)
        return max_update_time

    def execute_db(self, sql):
        cursor = self.db_conn.cursor()
        try:
            cursor.execute(sql)
            cursor.execute('commit;')
            cursor.close()
            logging.debug('sql execute success')
        except Exception as ex:
            cursor.close()
            logging.error('sql execute failed!')
            logging.error('traceback.format_exc():\n%s' % traceback.format_exc())
            print ex

    def insert_finance_record(self, finance_data):
        sql_delete = '''delete from t_amazon_finance_record where shop_name ="%s" and amazon_order_id ="%s" and seller_sku ="%s" and order_adjustment_item_id="%s" and fee_type="%s" and posted_date ="%s" ''' \
                     % (self.auth_info['ShopName'], finance_data[1], finance_data[3], finance_data[5], finance_data[6], finance_data[0])
        print sql_delete
        logging.debug('sql_delete is: %s' % sql_delete)
        self.execute_db(sql_delete)
        sql_insert = '''insert into t_amazon_finance_record
            (posted_date, amazon_order_id, marketplace_name, seller_sku, quantity_shipped, order_adjustment_item_id, fee_type, fee_currency, fee_amount, shop_name, finance_type, refresh_time)
            values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")
            ''' % (finance_data[0],finance_data[1],finance_data[2],finance_data[3],finance_data[4],finance_data[5],finance_data[6],finance_data[7],finance_data[8],self.auth_info['ShopName'], 'Refund', datetime.datetime.now())
        print sql_insert
        logging.debug('sql_insert is: %s' % sql_insert)
        self.execute_db(sql_insert)

    def parse_item(self, posted_date, amazon_order_id, marketplace_name, shipment_item):
        seller_sku = shipment_item.get('SellerSKU').get('value')
        quantity_shipped = shipment_item.get('QuantityShipped').get('value')
        order_adjustment_item_id = shipment_item.get('OrderAdjustmentItemId').get('value')

        fee_component_dict = shipment_item.get('ItemFeeAdjustmentList')
        if fee_component_dict:
            fee_component = fee_component_dict.get('FeeComponent')
            for ind, val in enumerate(fee_component):
                feed_type = val.get('FeeType').get('value')
                feed_currency_code = val.get('FeeAmount').get('CurrencyCode').get('value')
                feed_currency_amount = val.get('FeeAmount').get('CurrencyAmount').get('value')
                data_list_feed = [posted_date, amazon_order_id, marketplace_name, seller_sku, quantity_shipped, order_adjustment_item_id, feed_type, feed_currency_code, feed_currency_amount]
                self.insert_finance_record(data_list_feed)

        charge_component_dict = shipment_item.get('ItemChargeAdjustmentList')
        if charge_component_dict:
            charge_component = charge_component_dict.get('ChargeComponent')
            for ind, val in enumerate(charge_component):
                feed_type = val.get('ChargeType').get('value')
                charge_currency_code = val.get('ChargeAmount').get('CurrencyCode').get('value')
                charge_currency_amount = val.get('ChargeAmount').get('CurrencyAmount').get('value')
                data_list_charge = [posted_date, amazon_order_id, marketplace_name, seller_sku, quantity_shipped, order_adjustment_item_id, feed_type, charge_currency_code, charge_currency_amount]
                self.insert_finance_record(data_list_charge)

    def parse_report(self, refund_report_each):
        if not refund_report_each:
            print 'no refund data'
            logging.debug('no refund data')
            return
        posted_date = refund_report_each.get('PostedDate').get('value')
        posted_date = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(posted_date[0:19], "%Y-%m-%dT%H:%M:%S"))
        amazon_order_id = refund_report_each.get('AmazonOrderId').get('value')
        marketplace_name = refund_report_each.get('MarketplaceName').get('value')
        shipment_item = refund_report_each.get('ShipmentItemAdjustmentList').get('ShipmentItem')
        if isinstance(shipment_item, list):
            for ship_item in shipment_item:
                self.parse_item(posted_date, amazon_order_id, marketplace_name, ship_item)
        else:
            self.parse_item(posted_date, amazon_order_id, marketplace_name, shipment_item)

    def finance_flow(self, begin_time):
        print 'begin flow'
        logging.debug('begin flow')
        refunc_report_raw = self.get_finance_report(begin_time=begin_time)
        print 'get data'
        logging.debug('get data')

        next_token = None
        next_token_dict = refunc_report_raw.get('ListFinancialEventsResult').get('NextToken')
        if next_token_dict:
            next_token = next_token_dict.get('value')

        refunc_report = refunc_report_raw.get('ListFinancialEventsResult').get('FinancialEvents').get('RefundEventList').get('ShipmentEvent')
        if isinstance(refunc_report, list):
            for report in refunc_report:
                self.parse_report(report)
        else:
            self.parse_report(refunc_report)

        while next_token:
            refunc_report_raw = self.get_finance_report(next_token=next_token)
            next_token = None
            next_token_dict = refunc_report_raw.get('ListFinancialEventsByNextTokenResult').get('NextToken')
            if next_token_dict:
                next_token = next_token_dict.get('value')
            refunc_report = refunc_report_raw.get('ListFinancialEventsByNextTokenResult').get('FinancialEvents').get('RefundEventList').get('ShipmentEvent')
            if isinstance(refunc_report, list):
                for report in refunc_report:
                    print '---------------------------------------------'
                    self.parse_report(report)
            else:
                self.parse_report(refunc_report)


DATABASE = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'hq_db',
    'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
    'PORT': '3306',
    'USER': 'by15161458383',
    'PASSWORD': 'K120Esc1'
}
auth_info = {'AWSAccessKeyId': 'AKIAIP5T3XYETWAWHHDA', 'ShopName': 'AMZ-0052-Bohonan-US/PJ', 'SecretKey': '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', 'table_name': 't_online_info_amazon', 'ShopSite': 'US', 'ShopIP': u'118.89.143.150', 'SellerId': 'ARBNA8Y4OL6TV', 'MarketplaceId': 'ATVPDKIKX0DER', 'update_type': 'refresh_ad_data'}
finace_obj = FinancesPublic(auth_info,DATABASE)
max_refund_time = finace_obj.get_last_refund_time()
finace_obj.finance_flow('2018-07-01')