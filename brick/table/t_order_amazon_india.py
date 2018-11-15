#-*-coding:utf-8-*-
from datetime import datetime
"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_order_amazon_india.py
 @time: 2018/1/5 16:36
"""

class t_order_amazon_india():
    def __init__(self,db_conn=None):
        self.db_conn = db_conn

    def get_order_item_info_by_orderNumber(self, orderNumber):
        cursor = self.db_conn.cursor()
        sql = "select CostPrice,Weight,IsCharged,SellerSKU,ShopSKU from t_order_item_amazon_india where AmazonOrderId='%s'" % orderNumber
        cursor.execute(sql)
        order_items = cursor.fetchall()
        cursor.close()
        order_item_infos = []
        for order_item in order_items:
            if order_item:
                order_item_info = {}
                order_item_info['CostPrice'] = order_item[0]
                order_item_info['Weight'] = order_item[1]
                order_item_info['IsCharged'] = order_item[2]
                order_item_info['SellerSKU'] = order_item[3]
                order_item_info['ShopSKU'] = order_item[4]
                order_item_infos.append(order_item_info)

        return order_item_infos

    def get_Amazon_order_id_for_feed(self):
        cursor = self.db_conn.cursor()
        sql = "select AmazonOrderId,ShopName from t_order_amazon_india where OrderWarningType='feedAmazon';"
        cursor.execute(sql)
        order_items = cursor.fetchall()
        cursor.close()
        order_item_infos = []
        for order_item in order_items:
            if order_item:
                order_item_info = {}
                order_item_info['AmazonOrderId'] = order_item[0]
                order_item_info['ShopName'] = order_item[1]
                order_item_infos.append(order_item_info)

        return order_item_infos

    def get_Amazon_shopName_for_feed(self):
        cursor = self.db_conn.cursor()
        sql = "select DISTINCT ShopName from t_order_amazon_india where OrderWarningType='feedAmazon';"
        cursor.execute(sql)
        order_items = cursor.fetchall()
        cursor.close()
        order_item_infos = []
        for order_item in order_items:
            if order_item:
                order_item_info = {}
                order_item_info['ShopName'] = order_item[0]
                order_item_infos.append(order_item_info)

        return order_item_infos

    def get_lastShipDate_by_AmazonOrderId(self,amazonOrderId):
        cursor = self.db_conn.cursor()
        sql = "select LatestShipDate from t_order_amazon_india where AmazonOrderId='%s'" % amazonOrderId
        cursor.execute(sql)
        order_item = cursor.fetchone()
        cursor.close()
        amazon_lastShipDate = {}
        if order_item:
            amazon_lastShipDate['LatestShipDate'] = order_item[0]
        return amazon_lastShipDate

    def update_status_and_warning(self, amazonOrderIds):
        cursor = self.db_conn.cursor()
        update_time = datetime.now()
        for amazonOrderId in amazonOrderIds:
            sql = "update t_order_amazon_india set OrderWarningDays=NULL,OrderWarningType=NULL,is_sure_feed=1,dealTime='%s'," \
                  "dealUser='automatic',dealAction='feed amazon' where AmazonOrderId='%s';"%(update_time,amazonOrderId)
            cursor.execute(sql)
        cursor.close()

    def getShopNameByOrderId(self, OrderId):
        result = {}
        try:
            cursor = self.db_conn.cursor()
            sql = "select ShopName from t_order_amazon_india where AmazonOrderId = %s limit 1"
            cursor.execute(sql,(OrderId,))
            result['data'] = cursor.fetchone()
            result['code'] = 0
            cursor.close()
            return result
        except Exception, ex:
            result['code'] = -1
            print '%s_%s:%s' % (traceback.print_exc(), Exception, ex)
            return result





