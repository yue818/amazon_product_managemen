# -*- coding: utf-8 -*-

"""
 @desc:
 @author: 张浩
 @site:
 @请用 Shopee_info_all.py 更新
"""

import time
import datetime
import MySQLdb
import json

from django_redis import get_redis_connection
from django.db import connection
from brick.classredis.classsku import classsku
from brick.classredis.classshopsku import classshopsku
from brick.shopee.api.Shopee_Public_API import Shopee_Public_API
from shopee_app.table.t_shopee_online_info import t_shopee_online_info
from shopee_app.table.t_shopee_online_info_detail import t_shopee_online_info_detail
from skuapp.table.t_store_configuration_file import t_store_configuration_file
from Project.settings import BASE_DIR

# def connect_sql(sql, kw):
#     db = MySQLdb.connect("192.168.105.111", "root", "root123", "hq", charset='utf8')
#     cursor = db.cursor()
#     cursor.executemany(sql, kw)
#     db.close()

def update_shopee_info(shopname='', partner_id='', shopid=''):
    db_conn = connection
    cursor = db_conn.cursor()
    redis_conn = get_redis_connection(alias='product')

    classsku_obj = classsku(db_cnxn=db_conn, redis_cnxn=redis_conn)
    classshopsku_obj = classshopsku(db_conn=db_conn, redis_conn=redis_conn)
    shopee_p = Shopee_Public_API(shopname)
    count = 0
    item_data = dict()
    item_data['cursor'] = cursor
    item_data['datas'] = list()
    while True:
        if count > 0:
            num = count * 100
        else:
            num = count
        timestamp = int(time.time())
        pagination_offset = num
        pagination_entries_per_page = 100
        Item_data = shopee_p.item_GetItemsList(pagination_offset, pagination_entries_per_page, partner_id, shopid, timestamp).json()
        try:
            more = Item_data['more']
            Item_data = Item_data['items']
        except Exception as e:
            if Item_data.get('error'):
                error = Item_data.get('error')
                msg = Item_data.get('msg')
                print u'partner_id: %s, shopid: %s 错误: %s, 错误信息: %s' % (str(partner_id), str(shopid), error, msg)
                break
            else:
                print u'partner_id: %s, shopid: %s, pagination_offset: %s 报错' %  (str(partner_id), str(shopid), str(pagination_offset))
                with open(BASE_DIR + '/brick/shopee/error_item.txt', 'a') as f:
                    f.write(str(e) + ' ||| ' + str(pagination_offset) + '\n')
                    count += 1
                    continue
        for i in Item_data:
            item_dict = dict()
            item_dict['ItemID'] = i.get('item_id')
            item_dict['Shopid'] = i.get('shopid')
            item_dict['ShopName'] = shopname
            item_dict['LastUpdated'] = i.get('update_time')
            if item_dict['LastUpdated']:
                item_dict['LastUpdated'] = (datetime.datetime.utcfromtimestamp(i.get('update_time'))+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
            item_dict['ItemSKU'] = i.get('item_sku')
            sku = classshopsku_obj.getSKU(item_dict['ItemSKU'])
            item_dict['SKU'] = sku
            item_dict['MainSKU'] = classsku_obj.get_bemainsku_by_sku(sku)
            if i.get('status') == 'NORMAL':
                item_dict['Status'] = '1'
            elif i.get('status') == 'BANNED':
                item_dict['Status'] = '0'
            else:
                item_dict['Status'] = '2'
            seller = ''
            published = ''
            try:
                shopee_info = t_store_configuration_file.objects.get(ShopName=shopname)
                seller = shopee_info.Seller
                published = shopee_info.Published
            except t_store_configuration_file.DoesNotExist:
                pass
            item_dict['Seller'] = seller
            item_dict['Published'] = published
            item_dict_tuple = (
                item_dict['ItemID'], item_dict['Shopid'], item_dict['ShopName'], item_dict['LastUpdated'], item_dict['SKU'], item_dict['MainSKU'], item_dict['ItemSKU'],
                item_dict['Status'], item_dict['Seller'], item_dict['Published'],  item_dict['Shopid'], item_dict['ShopName'], item_dict['LastUpdated'], item_dict['SKU'], item_dict['MainSKU'], item_dict['ItemSKU'],
                item_dict['Status'], item_dict['Seller'], item_dict['Published']
            )
            item_data['datas'].append(item_dict_tuple)
        try:
            save_item_info(**item_data)
        except Exception as e:
            print u'partner_id: %s, shopid: %s, pagination_offset: %s 报错' %  (str(partner_id), str(shopid), str(pagination_offset))
            with open(BASE_DIR + '/brick/shopee/error_item.txt', 'a') as f:
                f.write(str(e) + ' ||| ' + str(pagination_offset) + '\n')
                count += 1
                continue
        item_data['datas'] = []
        count += 1
        if not more:
            break

def update_shopee_info_detail(shopname='', partner_id='', shopid=''):
    db_conn = connection
    cursor = db_conn.cursor()
    redis_conn = get_redis_connection(alias='product')

    classsku_obj = classsku(db_cnxn=db_conn, redis_cnxn=redis_conn)
    classshopsku_obj = classshopsku(db_conn=db_conn, redis_conn=redis_conn)
    shopee_p = Shopee_Public_API(shopname)

    item_data = dict()
    item_data['cursor'] = cursor
    item_data['datas'] = list()
    item_detail_data = dict()
    item_detail_data['cursor'] = cursor
    item_detail_data['datas'] = list()
    item_list = t_shopee_online_info.objects.filter(ShopName=shopname).values('ItemID', 'ItemSKU')

    for i in item_list:
        item_dict = dict()
        item_id = i['ItemID']
        timestamp = int(time.time())
        try:
            Item_detail = shopee_p.item_GetItemDetail(item_id, partner_id, shopid, timestamp)
            Item_detail = Item_detail.json()['item']
        except Exception as e:
            print u"partner_id: %s, shopid: %s, 产品ID为: %s, 获取平台数据报错; %s" % (str(partner_id), str(shopid), str(item_id), str(e))
            with open(BASE_DIR + '/brick/shopee/get_Iteminfo_error.txt', 'a') as f:
                f.write(str(e) + ' ||| ' + str(item_id) + '\n')
                continue

        item_dict['Price'] = Item_detail.get('price')
        item_dict['Original_price'] = Item_detail.get('original_price')
        item_dict['PackageWidth'] = Item_detail.get('package_width')
        item_dict['PackageLength'] = Item_detail.get('package_length')
        item_dict['PackageHeight'] = Item_detail.get('package_height')
        item_dict['CmtCount'] = Item_detail.get('cmt_count')
        item_dict['Conditions'] = Item_detail.get('condition')
        item_dict['SizeChart'] = Item_detail.get('size_chart')
        item_dict['Currency'] = Item_detail.get('currency')
        item_dict['Weight'] = Item_detail.get('weight')
        item_dict['Likes'] = Item_detail.get('likes')
        item_dict['Image'] = Item_detail.get('images')[0] if Item_detail.get('images') else ''
        item_dict['ExtraImages'] = ','.join(Item_detail.get('images')) if Item_detail.get('images') else ''
        item_dict['Views'] = Item_detail.get('views')
        item_dict['DaysToShip'] = Item_detail.get('days_to_ship')
        item_dict['HasVariation'] = Item_detail.get('has_variation')
        item_dict['RatingStar'] = Item_detail.get('rating_star')
        item_dict['Sales'] = Item_detail.get('sales')
        item_dict['Title'] = Item_detail.get('name')
        item_dict['CategoryId'] = Item_detail.get('category_id')
        item_dict['DateUploaded'] = Item_detail.get('create_time')
        if item_dict['DateUploaded']:
            item_dict['DateUploaded'] = (datetime.datetime.utcfromtimestamp(Item_detail.get('create_time'))+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        item_dict['LastUpdated'] = Item_detail.get('update_time')
        if item_dict['LastUpdated']:
            item_dict['LastUpdated'] = (datetime.datetime.utcfromtimestamp(Item_detail.get('update_time'))+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        item_dict['RefreshTime'] = datetime.datetime.now()
        item_dict['Stock'] = Item_detail.get('stock')
        item_dict['Description'] = Item_detail.get('description')
        if Item_detail.get('status') == 'NORMAL':
            item_dict['Status'] = '1'
        elif Item_detail.get('status') == 'BANNED':
            item_dict['Status'] = '0'
        elif Item_detail.get('DELETED'):
            item_dict['Status'] = '2'
        else:
            item_dict['Status'] = ''
        orders7Days = 0

        for i_d_v in Item_detail['variations']:
            var_dict = dict()
            var_dict['ItemID'] = item_id
            var_dict['VariantID'] = i_d_v.get('variation_id')
            var_dict['ItemSKU'] = i['ItemSKU']
            orders7Days_shupsku = classsku_obj.get_shopsevensale_by_sku(i_d_v.get('variation_sku'))
            if orders7Days_shupsku:
                try:
                    orders7Days += int(orders7Days_shupsku)
                except:
                    pass

            var_dict['VariationSKU'] = i_d_v.get('variation_sku')
            sku = classshopsku_obj.getSKU(var_dict['VariationSKU'])
            var_dict['SKU'] = sku
            var_dict['MainSKU'] = classsku_obj.get_bemainsku_by_sku(sku)
            var_dict['Price'] = i_d_v.get('price')
            var_dict['Original_price'] = i_d_v.get('original_price')
            var_dict['Stock'] = i_d_v.get('stock')
            var_dict['Different'] = i_d_v.get('name')
            if i_d_v.get('status') == 'MODEL_NORMAL':
                var_dict['Status'] = '1'
            elif i_d_v.get('status') == 'MODEL_DELETED':
                var_dict['Status'] = '0'
            else:
                var_dict['Status'] = i_d_v.get('status')

            var_dict['CreateTime'] = i_d_v.get('create_time')
            if var_dict['CreateTime']:
                var_dict['CreateTime'] = (datetime.datetime.utcfromtimestamp(i_d_v.get('create_time'))+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
            var_dict['UpdateTime'] = i_d_v.get('update_time')
            if var_dict['UpdateTime']:
                var_dict['UpdateTime'] = (datetime.datetime.utcfromtimestamp(i_d_v.get('update_time'))+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
            var_dict_tuple = (
                var_dict['ItemID'], var_dict['VariantID'], var_dict['SKU'], var_dict['MainSKU'], var_dict['ItemSKU'],
                var_dict['VariationSKU'], var_dict['Price'], var_dict['Original_price'], var_dict['Stock'], var_dict['Different'],
                var_dict['Status'], var_dict['CreateTime'], var_dict['UpdateTime'], var_dict['Price'], var_dict['Original_price'],
                var_dict['Stock'], var_dict['Different'], var_dict['Status'], var_dict['CreateTime'], var_dict['UpdateTime']
            )
            item_detail_data['datas'].append(var_dict_tuple)
        
        if len(item_detail_data['datas']) > 0:
            try:
                save_variant_infos(**item_detail_data)
            except Exception as e:
                print u"partner_id: %s, shopid: %s, 产品ID为: %s, 新增 t_shopee_online_detail 表报错; %s" % (str(partner_id), str(shopid), str(item_id), str(e))
                with open(BASE_DIR + '/brick/shopee/error_info_detail.txt', 'a') as f:
                    f.write(str(e) + ' ||| ' + str(item_id) + '\n')
                    continue
            
            item_detail_data['datas'] = []
        item_dict['Orders7Days'] = orders7Days
        item_dict_tuple = (
            item_dict['Price'], item_dict['Original_price'], item_dict['PackageWidth'], item_dict['PackageLength'], item_dict['PackageHeight'],
            item_dict['CmtCount'], item_dict['Conditions'], item_dict['SizeChart'], item_dict['Currency'], item_dict['Weight'], item_dict['Likes'],
            item_dict['Image'], item_dict['ExtraImages'], item_dict['Views'], item_dict['DaysToShip'], item_dict['HasVariation'],
            item_dict['RatingStar'], item_dict['Sales'], item_dict['Title'], item_dict['CategoryId'], item_dict['DateUploaded'], item_dict['LastUpdated'],
            item_dict['RefreshTime'], item_dict['Stock'], item_dict['Description'], item_dict['Status'], item_dict['Orders7Days'], item_id
        )
        item_data['datas'].append(item_dict_tuple)
        
        try:
            update_item_infos(**item_data)
        except Exception as e:
            print u"partner_id: %s, shopid: %s, 产品ID为: %s, 更新 t_shopee_online_info 表报错; %s" % (str(partner_id), str(shopid), str(item_id), str(e))
            with open(BASE_DIR + '/brick/shopee/error_info_detail.txt', 'a') as f:
                f.write(str(e) + ' ||| ' + str(item_id) + '\n')
                continue
        item_data['datas'] = []


def save_item_info(**kw):
    cursor = kw['cursor']
    sql = 'INSERT INTO t_shopee_online_info (ItemID, Shopid, ShopName, LastUpdated, SKU, MainSKU, ItemSKU, Status, Seller, Published) ' \
          'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ' \
          'ON DUPLICATE KEY UPDATE ' \
          'Shopid=%s, ShopName=%s, LastUpdated=%s, SKU=%s, MainSKU=%s, ItemSKU=%s, Status=%s, Seller=%s, Published=%s; '
    cursor.executemany(sql, kw['datas'])

def save_variant_infos(**kw):
    cursor = kw['cursor']
    sql = 'INSERT INTO t_shopee_online_info_detail (ItemID, VariantID, SKU, MainSKU, ItemSKU, VariationSKU, ' \
          'Price, Original_price, Stock, Different, Status, CreateTime, UpdateTime) ' \
          'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ' \
          'ON DUPLICATE KEY UPDATE ' \
          'Price=%s, Original_price=%s, Stock=%s, Different=%s, Status=%s, CreateTime=%s, UpdateTime=%s; '
    cursor.executemany(sql, kw['datas'])

def update_item_infos(**kw):
    cursor = kw['cursor']
    data = kw['datas'][0]
    sql = 'UPDATE t_shopee_online_info SET Price=%s, Original_price=%s, PackageWidth=%s, PackageLength=%s, ' \
        'PackageHeight=%s, CmtCount=%s, Conditions=%s, SizeChart="%s", Currency="%s", Weight=%s, Likes=%s, ' \
        'Image=%s, ExtraImages=%s, Views=%s, DaysToShip=%s, HasVariation=%s, RatingStar=%s, Sales=%s, Title=%s, CategoryId=%s, ' \
        'DateUploaded=%s, LastUpdated=%s, RefreshTime=%s, Stock=%s, Description=%s, Status=%s, Orders7Days=%s where ItemID=%s; '
    cursor.execute(sql, data)

def update_else_info():
    item_ids = [1376156177]
    partner_id = 10041
    shopid = 13399960
    shopname = 'SHP-002-Kuhong-MY/EB'
    timestamp = int(time.time())

    db_conn = connection
    cursor = db_conn.cursor()
    redis_conn = get_redis_connection(alias='product')

    classsku_obj = classsku(db_cnxn=db_conn, redis_cnxn=redis_conn)
    classshopsku_obj = classshopsku(db_conn=db_conn, redis_conn=redis_conn)
    shopee_p = Shopee_Public_API(shopname)

    for item_id in item_ids:
        Item_detail = shopee_p.item_GetItemDetail(item_id, partner_id, shopid, timestamp)
        Item_detail = Item_detail.json()['item']
        item_data = dict()
        item_data['cursor'] = cursor
        item_data['datas'] = list()
        item_detail_data = dict()
        item_detail_data['cursor'] = cursor
        item_detail_data['datas'] = list()

        item_dict = dict()
        item_dict['Price'] = Item_detail.get('price')
        item_dict['Original_price'] = Item_detail.get('original_price')
        item_dict['PackageWidth'] = Item_detail.get('package_width')
        item_dict['PackageLength'] = Item_detail.get('package_length')
        item_dict['PackageHeight'] = Item_detail.get('package_height')
        item_dict['CmtCount'] = Item_detail.get('cmt_count')
        item_dict['Conditions'] = Item_detail.get('condition')
        item_dict['SizeChart'] = Item_detail.get('size_chart')
        item_dict['Currency'] = Item_detail.get('currency')
        item_dict['Weight'] = Item_detail.get('weight')
        item_dict['Likes'] = Item_detail.get('likes')
        item_dict['Image'] = Item_detail.get('images')[0] if Item_detail.get('images') else ''
        item_dict['ExtraImages'] = ','.join(Item_detail.get('images')) if Item_detail.get('images') else ''
        item_dict['Views'] = Item_detail.get('views')
        item_dict['DaysToShip'] = Item_detail.get('days_to_ship')
        item_dict['HasVariation'] = Item_detail.get('has_variation')
        item_dict['RatingStar'] = Item_detail.get('rating_star')
        item_dict['Sales'] = Item_detail.get('sales')
        item_dict['Title'] = Item_detail.get('name')
        item_dict['CategoryId'] = Item_detail.get('category_id')
        item_dict['DateUploaded'] = Item_detail.get('create_time')
        if item_dict['DateUploaded']:
            item_dict['DateUploaded'] = (datetime.datetime.utcfromtimestamp(Item_detail.get('create_time'))+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        item_dict['LastUpdated'] = Item_detail.get('update_time')
        if item_dict['LastUpdated']:
            item_dict['LastUpdated'] = (datetime.datetime.utcfromtimestamp(Item_detail.get('update_time'))+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        item_dict['RefreshTime'] = datetime.datetime.now()
        item_dict['Stock'] = Item_detail.get('stock')
        item_dict['Description'] = Item_detail.get('description')
        if Item_detail.get('status') == 'NORMAL':
            item_dict['Status'] = '1'
        elif Item_detail.get('status') == 'BANNED':
            item_dict['Status'] = '0'
        else:
            item_dict['Status'] = '2'
        orders7Days = 0
        for i_d_v in Item_detail['variations']:
            var_dict = dict()
            var_dict['ItemID'] = item_id
            var_dict['VariantID'] = i_d_v.get('variation_id')
            var_dict['ItemSKU'] = i['ItemSKU']
            orders7Days_shupsku = classsku_obj.get_shopsevensale_by_sku(i_d_v.get('variation_sku'))
            if orders7Days_shupsku:
                try:
                    orders7Days += int(orders7Days_shupsku)
                except:
                    pass

            var_dict['VariationSKU'] = i_d_v.get('variation_sku')
            sku = classshopsku_obj.getSKU(var_dict['VariationSKU'])
            var_dict['SKU'] = sku
            var_dict['MainSKU'] = classsku_obj.get_bemainsku_by_sku(sku)
            var_dict['Price'] = i_d_v.get('price')
            var_dict['Original_price'] = i_d_v.get('original_price')
            var_dict['Stock'] = i_d_v.get('stock')
            var_dict['Different'] = i_d_v.get('name')
            if i_d_v.get('status') == 'MODEL_NORMAL':
                var_dict['Status'] = '1'
            elif i_d_v.get('status') == 'MODEL_DELETED':
                var_dict['Status'] = '0'

            var_dict['CreateTime'] = i_d_v.get('create_time')
            if var_dict['CreateTime']:
                var_dict['CreateTime'] = (datetime.datetime.utcfromtimestamp(i_d_v.get('create_time'))+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
            var_dict['UpdateTime'] = i_d_v.get('update_time')
            if var_dict['UpdateTime']:
                var_dict['UpdateTime'] = (datetime.datetime.utcfromtimestamp(i_d_v.get('update_time'))+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
            var_dict_tuple = (
                var_dict['ItemID'], var_dict['VariantID'], var_dict['SKU'], var_dict['MainSKU'], var_dict['ItemSKU'],
                var_dict['VariationSKU'], var_dict['Price'], var_dict['Original_price'], var_dict['Stock'], var_dict['Different'],
                var_dict['Status'], var_dict['CreateTime'], var_dict['UpdateTime'], var_dict['Price'], var_dict['Original_price'],
                var_dict['Stock'], var_dict['Different'], var_dict['Status'], var_dict['CreateTime'], var_dict['UpdateTime']
            )
            item_detail_data['datas'].append(var_dict_tuple)

        try:
            save_variant_infos(**item_detail_data)
        except Exception as e:
            print u"产品ID为: %s, 新增 t_shopee_online_detail 表报错; %s" % (str(item_id), str(e))
            with open(BASE_DIR + '/brick/shopee/error_info_detail.txt', 'a') as f:
                f.write(str(e) + ' ||| ' + str(item_id) + '\n')
                continue
        item_detail_data['datas'] = []

        item_dict['Orders7Days'] = orders7Days
        item_dict_tuple = (
            item_dict['Price'], item_dict['Original_price'], item_dict['PackageWidth'], item_dict['PackageLength'], item_dict['PackageHeight'],
            item_dict['CmtCount'], item_dict['Conditions'], item_dict['SizeChart'], item_dict['Currency'], item_dict['Weight'], item_dict['Likes'],
            item_dict['Image'], item_dict['ExtraImages'], item_dict['Views'], item_dict['DaysToShip'], item_dict['HasVariation'],
            item_dict['RatingStar'], item_dict['Sales'], item_dict['Title'], item_dict['CategoryId'], item_dict['DateUploaded'], item_dict['LastUpdated'],
            item_dict['RefreshTime'], item_dict['Stock'], item_dict['Description'], item_dict['Status'], item_dict['Orders7Days'], item_id
        )
        item_data['datas'].append(item_dict_tuple)

        try:
            update_item_infos(**item_data)
        except Exception as e:
            print u"产品ID为: %s, 更新 t_shopee_online_info 表报错; %s" % (str(item_id), str(e))
            with open(BASE_DIR + '/brick/shopee/error_info_detail.txt', 'a') as f:
                f.write(str(e) + ' ||| ' + str(item_id) + '\n')
                continue
        item_data['datas'] = []
