#!/usr/bin/python
# -*- coding: utf-8 -*-

from brick.db.dbconnect import run
from brick.function.Rabbit_MQ_Server import Rabbit_MQ_Server
from brick.table.t_config_online_joom import t_config_online_joom
from brick.table.t_joom_cutprice_log import t_joom_cutprice_log
from brick.table.t_config_mq_info import t_config_mq_info
from joom_app.table.t_joom_price_parity_log import t_joom_price_parity_log


def Joom_Change_Product_Price_Client(shop_name=None, product_id='', cutprice_flag=0):
    # 降价销售
    db_res = run({})
    if db_res['errorcode'] == -1:
        print "result['errortext']: %s" % db_res['errortext']
        return
    t_config_mq_info_obj = t_config_mq_info(db_cnxn=db_res['db_conn'])
    RABBITMQ = t_config_mq_info_obj.get_rabbitmq_info_by_name_platform('Amazon-RabbitMQ-Server', 'Amazon')
    rabbitmq_server = Rabbit_MQ_Server(db_conn=db_res['db_conn'], RABBITMQ=RABBITMQ)

    datainfo = dict()
    joom_cutprice_log = t_joom_cutprice_log(db_conn=db_res['db_conn'])
    product_res = joom_cutprice_log.getlogbyproductid(product_id)
    # product_res = joom_cutprice_log.get_cutpricing_products()
    print 'product_res', len(product_res)
    # print product_res
    if not product_res:
        return {'code': -1, 'message': 'Can not get cut price product info for sending to mq, product id: %s, please connect with administrator' % product_id}
    product_info = dict()
    for i in product_res:
        # shop_name = i['ShopName']
        # product_id = i['ProductID']
        product_info['ShopSKU'] = i['ShopSKU'].split(',')
        product_info['OldPrice'] = i['OldPrice'].split(',')
        product_info['Discount'] = float(i['Discount'])
        print product_info
        ProductInfo = dict()
        for k, v in enumerate(product_info['ShopSKU']):
            ProductInfo[v] = dict()
            if cutprice_flag == 0:
                ProductInfo[v]['price'] = float(product_info['OldPrice'][k]) * (product_info['Discount'] / 100.0)
                datainfo['flag'] = 'cutprice'
            else:
                ProductInfo[v]['price'] = float(product_info['OldPrice'][k])
                datainfo['flag'] = 'recoverprice'

        datainfo['ShopName'] = shop_name
        datainfo['productinfo'] = ProductInfo
        datainfo['product_id'] = product_id

        joom_config = t_config_online_joom(db_conn=db_res['db_conn'])
        if shop_name:
            shop_res = [joom_config.getauthByShopName(shop_name)]
        else:
            shop_res = joom_config.getalljoomauth()
        queue = ''
        for i in shop_res:
            queue = str(i['IP']) + '_joom_change_product_info'
        if queue:
            print queue
            print datainfo
            rabbitmq_server.Send_Mess_To_MQ(str(datainfo), queue)
    rabbitmq_server.close_connection()

    return {'code': 0, 'message': ''}


def Joom_Price_Parity_Client(ShopName, ProductID):
    db_res = run({})
    if db_res['errorcode'] == -1:
        print "result['errortext']: %s" % db_res['errortext']
        return
    t_config_mq_info_obj = t_config_mq_info(db_cnxn=db_res['db_conn'])
    RABBITMQ = t_config_mq_info_obj.get_rabbitmq_info_by_name_platform('Amazon-RabbitMQ-Server', 'Amazon')
    rabbitmq_server = Rabbit_MQ_Server(db_conn=db_res['db_conn'], RABBITMQ=RABBITMQ)

    joom_config = t_config_online_joom(db_conn=db_res['db_conn'])
    shop_res = joom_config.getauthByShopName(ShopName)
    queue = str(shop_res['IP']) + '_joom_change_product_info'

    datainfo = dict()
    datainfo['ShopName'] = ShopName
    datainfo['product_id'] = ProductID
    datainfo['flag'] = 'price_parity'

    ProductInfo = dict()
    pro_info = t_joom_price_parity_log.objects.filter(ProductID=ProductID, ChangeFlag='False').values('ShopSKU', 'NewPrice', 'id')
    if pro_info:
        for i in pro_info:
            ProductInfo[i['ShopSKU']] = dict()
            ProductInfo[i['ShopSKU']]['price'] = i['NewPrice']
            ProductInfo[i['ShopSKU']]['log_id'] = i['id']
    else:
        return {'code': -1, 'message': 'No joom price parity log.'}

    if ProductInfo:
        datainfo['productinfo'] = ProductInfo

        rabbitmq_server.Send_Mess_To_MQ(str(datainfo), queue)
        rabbitmq_server.close_connection()
    else:
        return {'code': -1, 'message': 'No joom price parity log.'}

    return {'code': 0, 'message': ''}
