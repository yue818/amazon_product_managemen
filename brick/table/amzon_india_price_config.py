# -*- coding: utf-8 -*-
import traceback

class amzon_india_price_config():

    def __init__(self, db_conn):
        self.db_conn = db_conn

    def getAmazonPriceCofig(self, ShopName):
        result = {}
        price_config = {}
        try:
            cursor = self.db_conn.cursor()
            sql = "select EXCHANGE_RATE,PROFIT_RATE,TRACK_PRICE_ELEC,TRACK_PRICE_UNELEC,TRACK_DEAL_WEIGHT,TRACK_DEAL_PRICE,MARKETED,MANUFACTURED,MRP_START,MRP_END,CUSTOMER_PHONE,END_MESSAGE, TABLE_WIDTH from amzon_india_price_config where ShopName = %s"
            cursor.execute(sql,(ShopName,))
            datasrc = cursor.fetchone()
            if datasrc:
                price_config['ShopName'] = ShopName
                price_config['EXCHANGE_RATE'] = datasrc[0]
                price_config['PROFIT_RATE'] = datasrc[1]
                price_config['TRACK_PRICE_ELEC'] = datasrc[2]
                price_config['TRACK_PRICE_UNELEC'] = datasrc[3]
                price_config['TRACK_DEAL_WEIGHT'] = datasrc[4]
                price_config['TRACK_DEAL_PRICE'] = datasrc[5]
                price_config['MARKETED'] = datasrc[6]
                price_config['MANUFACTURED'] = datasrc[7]
                price_config['MRP_START'] = datasrc[8]
                price_config['MRP_END'] = datasrc[9]
                price_config['CUSTOMER_PHONE'] = datasrc[10]
                price_config['END_MESSAGE'] = datasrc[11]
                price_config['TABLE_WIDTH'] = datasrc[12]
                cursor.close()
                result['data'] = price_config
                result['code'] = 0
            elif not datasrc:
                result['code'] = -1
            return result
        except Exception, ex:
            result['code'] = -1
            print '%s_%s:%s' % (traceback.print_exc(), Exception, ex)
            return result


# from brick.db.dbconnect import run
# from brick.table.t_order_amazon_india import t_order_amazon_india
# a = t_order_amazon_india(run({})['db_conn'])
# b = a.getShopNameByOrderId('403-1477131-1652300')
# 
# print b['code']
# print b['data'][0]
# from brick.db.dbconnect import run
# a = amzon_india_price_config(run({})['db_conn'])
# price_config = a.getAmazonPriceCofig(ShopName='AMZ-0201-Cberty-IN/HF')
# print price_config['data']['EXCHANGE_RATE']
