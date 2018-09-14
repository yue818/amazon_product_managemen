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

    def get_finance_report(self, begin_time):
        finance_report = self.finance_public.list_financial_events(posted_after=begin_time)
        finance_report_dict = finance_report._response_dict
        return finance_report_dict.get('ListFinancialEventsResult').get('FinancialEvents').get('RefundEventList').get('ShipmentEvent')

    def execute_db(self, sql):
        cursor = self.db_conn.cursor()
        try:
            cursor.execute(sql)
            cursor.execute('commit;')
            cursor.close()
            # logging.debug('sql execute success')
        except Exception as e:
            cursor.close()
            # logging.error('sql execute failed!')
            # logging.error('traceback.format_exc():\n%s' % traceback.format_exc())
            print e

    def insert_finance_record(self, finance_data):
        sql_insert = '''insert into t_amazon_finance_record
            (posted_date, amazon_order_id, marketplace_name, seller_sku, quantity_shipped, order_adjustment_item_id, fee_type, fee_currency, fee_amount, shop_name, finance_type, refresh_time)
            values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")
            ''' % (finance_data[0],finance_data[1],finance_data[2],finance_data[3],finance_data[4],finance_data[5],finance_data[6],finance_data[7],finance_data[8],finance_data[9],self.auth_info['ShopName'], 'Refund', datetime.datetime.now())
        print sql_insert
        self.execute_db(sql_insert)

    def parse_item(self, posted_date, amazon_order_id, marketplace_name, shipment_item):
        seller_sku = shipment_item.get('SellerSKU').get('value')
        quantity_shipped = shipment_item.get('QuantityShipped').get('value')
        order_adjustment_item_id = shipment_item.get('OrderAdjustmentItemId').get('value')

        fee_component = shipment_item.get('ItemFeeAdjustmentList').get('FeeComponent')
        for ind, val in enumerate(fee_component):
            feed_type = val.get('FeeType').get('value')
            feed_currency_code = val.get('FeeAmount').get('CurrencyCode').get('value')
            feed_currency_amount = val.get('FeeAmount').get('CurrencyAmount').get('value')
            data_list_feed = [posted_date, amazon_order_id, marketplace_name, seller_sku, quantity_shipped, order_adjustment_item_id, feed_type, feed_currency_code, feed_currency_amount]
            self.insert_finance_record(data_list_feed)

        charge_component = shipment_item.get('ItemChargeAdjustmentList').get('ChargeComponent')
        for ind, val in enumerate(charge_component):
            feed_type = val.get('ChargeType').get('value')
            charge_currency_code = val.get('ChargeAmount').get('CurrencyCode').get('value')
            charge_currency_amount = val.get('ChargeAmount').get('CurrencyAmount').get('value')
            data_list_charge = [posted_date, amazon_order_id, marketplace_name, seller_sku, quantity_shipped, order_adjustment_item_id, feed_type, charge_currency_code, charge_currency_amount]
            self.insert_finance_record(data_list_charge)

    def parse_report(self, refunc_report_each):
        posted_date = refunc_report_each.get('PostedDate').get('value')
        amazon_order_id = refunc_report_each.get('AmazonOrderId').get('value')
        marketplace_name = refunc_report_each.get('MarketplaceName').get('value')
        shipment_item = refunc_report_each.get('ShipmentItemAdjustmentList').get('ShipmentItem')
        if isinstance(shipment_item, list):
            for ship_item in shipment_item:
                self.parse_item(posted_date, amazon_order_id, marketplace_name, ship_item)
        else:
            self.parse_item(posted_date, amazon_order_id, marketplace_name, shipment_item)

    def finance_flow(self, begin_time):
        refunc_report = self.get_finance_report(begin_time)
        if isinstance(refunc_report, list):
            for report in refunc_report:
                print '---------------------------------------------'
                self.parse_report(report)
        else:
            self.parse_report(refunc_report)


auth_info = {'AWSAccessKeyId': 'AKIAIP5T3XYETWAWHHDA', 'ShopName': 'AMZ-0052-Bohonan-US/PJ', 'SecretKey': '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', 'table_name': 't_online_info_amazon', 'ShopSite': 'US', 'ShopIP': u'118.89.143.150', 'SellerId': 'ARBNA8Y4OL6TV', 'MarketplaceId': 'ATVPDKIKX0DER', 'update_type': 'refresh_ad_data'}
finace_obj = FinancesPublic(auth_info)
finace_obj.finance_flow('2018-08-01')