#!/usr/bin/python
# -*- coding: utf-8 -*-

from brick.db.dbconnect import run
from brick.function.Rabbit_MQ_Server import Rabbit_MQ_Server
from brick.table.t_config_online_joom import t_config_online_joom
from brick.table.t_config_mq_info import t_config_mq_info
from datetime import datetime
import time


def Joom_Get_Source_Products_Client(shop_name=None, product_id='', flag=0):
    # flag=1 增量, flag=0 全量
    db_res = run({})
    if db_res['errorcode'] == -1:
        print "result['errortext']: %s" % db_res['errortext']
        return
    t_config_mq_info_obj = t_config_mq_info(db_cnxn=db_res['db_conn'])
    RABBITMQ = t_config_mq_info_obj.get_rabbitmq_info_by_name_platform('Amazon-RabbitMQ-Server', 'Amazon')
    rabbitmq_server = Rabbit_MQ_Server(db_conn=db_res['db_conn'], RABBITMQ=RABBITMQ)
    joom_config = t_config_online_joom(db_conn=db_res['db_conn'])
    if shop_name:
        res = [joom_config.getauthByShopName(shop_name)]
    else:
        res = joom_config.getalljoomauth()
    joom_ip_shop = dict()
    for i in res:
        queue = str(i['IP']) + '_joom_get_product_callback'
        shop_dict = dict()
        shop_dict['ShopName'] = i['ShopName']
        shop_dict['flag'] = flag
        shop_dict['PlatformName'] = 'Joom'
        shop_dict['CMDID'] = ['GetShopSKUInfo']
        shop_dict['ScheduleTime'] = datetime.now()
        shop_dict['ActualBeginTime'] = datetime.now()
        shop_dict['ActualEndTime'] = ''
        shop_dict['Status'] = 0
        shop_dict['ProcessingStatus'] = ''
        shop_dict['Processed'] = 0
        shop_dict['Successful'] = 0
        shop_dict['WithError'] = 0
        shop_dict['WithWarning'] = 0
        shop_dict['TransactionID'] = ''
        shop_dict['InsertTime'] = datetime.now()
        shop_dict['UpdateTime'] = datetime.now()
        shop_dict['Params'] = ''
        shop_dict['Timedelta'] = 0
        shop_dict['RetryCount'] = 0
        shop_dict['pid'] = ''
        shop_dict['cmdtext'] = ''
        shop_dict['errorinfo'] = ''
        shop_dict['productid'] = product_id
        if joom_ip_shop.get(queue):
            joom_ip_shop[queue].append(shop_dict)
        else:
            joom_ip_shop[queue] = list()
            joom_ip_shop[queue].append(shop_dict)

    for i in joom_ip_shop.keys():
        # Now only get joom2 & joom3
        if i == '114.115.161.21_joom_get_product_callback':
            for j in joom_ip_shop[i]:
                rabbitmq_server.Send_Mess_To_MQ(str([j, ]), i)
                time.sleep(0.2)
    rabbitmq_server.close_connection()
