# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: amazon_auto_load.py
 @time: 2018/11/2 9:22
"""  
import uuid
import redis
from brick.amazon.product_refresh.get_auth_info import GetAuthInfo
from brick.amazon.product_refresh.generate_feed_xml import GenerateFeedXml
from brick.amazon.upload_product.message_to_rabbitmq import MessageToRabbitMq
import json
import datetime
from django.db import connection
# import chardet


class AmazonAutoLoad:
    def __init__(self):
        # self.batch_id = str(uuid.uuid4())
        self.batch_id = '42021767-18ff-412c-b1f1-5980516de75c'
        self.online_conn = connection
        self.rd_conn = redis.Redis(host='r-uf6206e9df36e854.redis.rds.aliyuncs.com',
                                   password='K120Esc1',
                                   port=6379,
                                   db=0)
        self.pipe = self.rd_conn.pipeline(transaction=False)

    def close_db_conn(self):
        try:
            if self.online_conn:
                self.online_conn.close()
        except Exception as ex:
            print ex

    def get_operate_records(self):
        # 组合的产品不自动（zh, +）; AMZ-0042-Anjun-US/PJ 这个店铺不自动上下架
        unload_record = '''insert into t_amazon_auto_load
                                      (batch_id, shop_name, seller_sku, sku, status, product_sku_status, deal_type, deal_user)
                                      select "''' + self.batch_id + '''", ShopName, seller_sku, sku,status,product_status,'unload' deal_type, 'system' deal_user
                                            FROM t_online_info_amazon
                                         WHERE is_fba = 0
                                           AND STATUS = 'Active'
                                           AND product_status IN (2, 3, 4)
                                           AND SKU NOT LIKE 'ZH%'
                                           AND seller_sku NOT LIKE '%+%'
                                           AND shopname IN
                                               (SELECT ShopName FROM t_config_shop_alias WHERE is_auto_unload = 1 and ShopStatus=1) 
                                          and shopname in (select name from t_config_online_amazon  where shop_name like 'AMZ-%' and name is not null)'''
        # 亚马逊精品事业部人员的账号不自动上架; 跟卖账号不自动上架; 组合的产品不自动（zh,+）; AMZ-0042-Anjun-US/PJ 这个店铺不自动上下架
        load_record = '''insert into t_amazon_auto_load
                                      (batch_id, shop_name, seller_sku, sku, status, product_sku_status, deal_type, deal_user, seller)
                                      SELECT "''' + self.batch_id + '''", ShopName, seller_sku, sku, status, product_status, 'load' deal_type, 'system' deal_user, seller
                                      FROM t_online_info_amazon
                                     WHERE is_fba = 0
                                       AND STATUS = 'Inactive'
                                       AND product_status = 1
                                       AND SKU NOT LIKE 'ZH%'
                                       AND seller_sku NOT LIKE '%+%'
                                       AND shopname IN
                                           (SELECT ShopName FROM t_config_shop_alias WHERE is_auto_load = 1 and ShopStatus=1)
                                       and shopname in (select name from t_config_online_amazon  where shop_name like 'AMZ-%' and name is not null)
                                      '''
        # and shopname not in (
        # 'AMZ-0042-Anjun-US/PJ', 'AMZ-0013-GBY-US/PJ', 'AMZ-0017-LXY-US/PJ', 'AMZ-0052-Bohonan-US/PJ', 'AMZ-0056-Chengcaifengye01-US/PJ', 'AMZ-0061-Peoria-US/PJ', 'AMZ-0078-Fuyamp-US/PJ',
        # 'AMZ-0099-Fuguan-US/PJ', 'AMZ-0143-KZXX-US/PJ', 'AMZ-0145-SH-US/PJ', 'AMZ-0152-DL-US/PJ', 'AMZ-0154-HY-US/PJ', 'AMZ-0162-ZS-US/PJ', 'AMZ-0173-XL-US/PJ', 'AMZ-0182-FXXR-JP/HF',
        # 'AMZ-0186-BL-US/HF', 'AMZ-0208-CHT-US/HF', 'AMZ-9900-YWGM-US/HF')
        # and seller not in ('陈赛', '周梦梅', '马曼曼', '夏娟 ', '葛冰雪', '马静', '苏蕊 ', '周园园', '郑丽', '刘丹阳', '罗洁', '彭立康 ', '陈梦', '孙竹', '徐梅');
        with self.online_conn.cursor() as cursor:
            # char_set = chardet.detect(record_sql_com)['encoding']
            # print char_set
            # record_sql_com = record_sql_com.decode(char_set).encode('utf-8')
            # print record_sql_com
            print unload_record
            cursor.execute(unload_record)
            print load_record
            cursor.execute(load_record)
            self.online_conn.commit()

    def get_com_sku_quantity(self, com_sku):
        sku_list = com_sku.split('+')
        cnt = 0
        for sku in sku_list:
            print sku.split("*")[0]
            self.pipe.hget(sku.split("*")[0], 'Number')
            self.pipe.hget(sku.split("*")[0], 'ReservationNum')
            cnt += 1
        quantity_result = self.pipe.execute()
        quantity_list = []
        for i in range(cnt):
            quantity_list.append((int(quantity_result[i * 2]) if quantity_result[i * 2] else 0) - (int(quantity_result[i * 2 + 1]) if quantity_result[i * 2 + 1] else 0))
        return min(quantity_list)

    def get_product_sku_quantity(self):
        sql_quantity = "select id, sku, com_pro_sku from t_amazon_auto_load where  batch_id = '%s' and deal_type = 'unload'" % self.batch_id
        sql_update = "update t_amazon_auto_load set quantity = %s where id = %s"
        update_list = list()
        with self.online_conn.cursor() as cursor:
            cursor.execute(sql_quantity)
            quantity_obj = cursor.fetchall()
            quantity_record_list = list()
            for obj in quantity_obj:
                quantity_record_list.append((obj[0], obj[1], obj[2]))
                self.pipe.hget(obj[1], 'Number')
                self.pipe.hget(obj[1], 'ReservationNum')
            # print quantity_record_list
            quantity_result = self.pipe.execute()

            for ind, id_sku in enumerate(quantity_record_list):
                if id_sku[2]:
                    quantity = self.get_com_sku_quantity(id_sku[2])
                elif id_sku[1] and '+' in id_sku[1]:
                    quantity = self.get_com_sku_quantity(id_sku[1])
                else:
                    quantity = (int(quantity_result[ind * 2]) if quantity_result[ind * 2] else 0) - (int(quantity_result[ind * 2 + 1]) if quantity_result[ind * 2 + 1] else 0)
                update_list.append((quantity, id_sku[0]))
            print update_list
            cursor.executemany(sql_update, update_list)
            # 售完下架只下架库存为0的
            sql_remain = "update t_amazon_auto_load set deal_type = 'remain' where batch_id = '%s' and deal_type ='unload'  and quantity > 0" % self.batch_id
            print sql_remain
            cursor.execute(sql_remain)
            self.online_conn.commit()

    def deal_feed_record(self):
        sql_upload = "select shop_name,seller_sku from t_amazon_auto_load where deal_type = 'load' and batch_id = '%s' and  deal_result is null" % self.batch_id
        sql_unload = "select shop_name,seller_sku from t_amazon_auto_load where deal_type = 'unload' and batch_id = '%s' and 1=2" % self.batch_id

        print sql_upload
        with self.online_conn.cursor() as cursor_upload:
            cursor_upload.execute(sql_upload)
            print cursor_upload.rowcount
            if cursor_upload.rowcount > 0:
                upload_records = cursor_upload.fetchall()
            else:
                upload_records = None
        self.get_feed_xml(upload_records, 'auto_load_product')

        print sql_unload
        with self.online_conn.cursor() as cursor_unload:
            cursor_unload.execute(sql_unload)
            print cursor_unload.rowcount
            if cursor_unload.rowcount > 0:
                unload_records = cursor_unload.fetchall()
            else:
                unload_records = None
        self.get_feed_xml(unload_records, 'auto_unload_product')

    def get_feed_xml(self, record_obj, load_type):
        shop_sku = dict()
        if record_obj:
            for record in record_obj:
                shop_name = record[0]
                seller_sku = record[1]
                if shop_name not in shop_sku:
                    shop_sku[shop_name] = [seller_sku]
                else:
                    shop_sku[shop_name].append(seller_sku)

            for key, value in shop_sku.items():
                get_auth_info_ins = GetAuthInfo(self.online_conn)
                auth_info = get_auth_info_ins.get_auth_info_by_shop_name(str(key))
                auth_info['IP'] = auth_info['ShopIP']
                auth_info['table_name'] = 't_online_info_amazon'
                auth_info['update_type'] = load_type
                auth_info['product_list'] = value
                auth_info['batch_id'] = self.batch_id

                if load_type == 'auto_load_product':
                    feed_xml_ins = GenerateFeedXml(auth_info)
                    feed_xml = feed_xml_ins.get_inventory_xml(value, 999)
                elif load_type == 'auto_unload_product':
                    feed_xml_ins = GenerateFeedXml(auth_info)
                    feed_xml = feed_xml_ins.get_inventory_xml(value, 0)
                else:
                    feed_xml = None
                auth_info['feed_xml'] = feed_xml
                print auth_info
                self.put_message_to_mq(auth_info)

    def put_message_to_mq(self, auth_info):
        message_to_rabbit_obj = MessageToRabbitMq(auth_info, self.online_conn)
        auth_info = json.dumps(auth_info)
        message_to_rabbit_obj.put_message(auth_info)

    def auto_start(self):
        # self.get_operate_records()
        # self.get_product_sku_quantity()
        self.deal_feed_record()


if __name__ == '__main__':
    auto_load_obj = AmazonAutoLoad()
    print datetime.datetime.now()
    auto_load_obj.auto_start()
    auto_load_obj.close_db_conn()
    print datetime.datetime.now()
