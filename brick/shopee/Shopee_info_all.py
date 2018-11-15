# -*- coding: utf-8 -*-

"""
 @desc:
 @author: 张浩
 @site:
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
from brick.shopee.Shopee_info_shopname import get_AvailableNum
from brick.shopee.t_shopee_oplogs import t_shopee_oplogs
from shopee_app.table.t_shopee_online_info import t_shopee_online_info
from shopee_app.table.t_shopee_online_info_detail import t_shopee_online_info_detail
from skuapp.table.t_store_configuration_file import t_store_configuration_file


def update_shopee_info(shopname='', partner_id='', shopid='', flag='', opid=''):
    # flag=1是增量同步店铺，为0或无值为全量更新
    db_conn = connection
    cursor = db_conn.cursor()
    redis_conn = get_redis_connection(alias='product')
    classsku_obj = classsku(db_cnxn=db_conn, redis_cnxn=redis_conn)
    classshopsku_obj = classshopsku(db_conn=db_conn, redis_conn=redis_conn)
    classskuobjs = classsku(db_cnxn=db_conn, redis_cnxn=redis_conn)
    shopee_p = Shopee_Public_API(shopname)
    item_data = dict()
    item_data['cursor'] = cursor
    item_data['datas'] = list()
    if opid != '':
        t_shopee_oplogs_obj = t_shopee_oplogs(connection)
    error_data = dict()
    error_data['cursor'] = cursor
    error_data['datas'] = list()
    item_detail_data = dict()
    item_detail_data['cursor'] = cursor
    item_detail_data['datas'] = list()
    if flag == '1':
        now = datetime.datetime.now()
        last_time = now + datetime.timedelta(days=-15)
    count = 0
    while True:
        timestamp = int(time.time())
        pagination_offset = count
        pagination_entries_per_page = 100
        update_time_from = None
        update_time_to = None
        if flag == '1':
            get_shopname_time(cursor, partner_id, shopname, shopid)
            # api接口给的最大时间差就是15天，所以已最大时间差取增量更新
            update_time_from = int(time.mktime(last_time.timetuple()))
            update_time_to = int(time.mktime(now.timetuple()))

        try:
            Item_data = shopee_p.item_GetItemsList(pagination_offset, pagination_entries_per_page,
                partner_id, shopid, timestamp, update_time_from, update_time_to)
        except Exception as e:
            print "item_GetItemsList获取数据报错：shopid: %s, partner_id: %s" % (shopid, partner_id)
            print repr(e)
            if opid != '':
                isResult = t_shopee_oplogs_obj.MoreupdateNum(opid, repr(e))
                assert isResult['errorcode'] == 0, "upload log error."
            break
        try:
            Item_data = json.loads(Item_data.content)
        except Exception as e:
            print "item_GetItemsList报错：shopid: %s, partner_id: %s" % (shopid, partner_id)
            print Item_data.content
            if opid != '':            
                isResult = t_shopee_oplogs_obj.MoreupdateNum(opid, repr(e))
                assert isResult['errorcode'] == 0, "upload log error."
            break
        try:
            more = Item_data['more']
            Item_data = Item_data['items']
        except Exception as e:
            print repr(e)
            print Item_data
            print "shopid: %s, partner_id: %s, error: %s" % (shopid, partner_id, repr(e))
            if opid != '':
                isResult = t_shopee_oplogs_obj.MoreupdateNum(opid, repr(e))
                assert isResult['errorcode'] == 0, "upload log error."
            break

        for i in Item_data:
            item_dict = dict()
            item_id = i.get('item_id')
            item_dict['ItemID'] = item_id
            item_dict['Shopid'] = i.get('shopid')
            item_dict['ShopName'] = shopname
            item_dict['ItemSKU'] = i.get('item_sku')
            sku = classshopsku_obj.getskueach(item_dict['ItemSKU'])
            item_dict['SKU'] = sku
            item_dict['MainSKU'] = classsku_obj.get_bemainsku_by_sku(sku)
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

            # 变体数据
            timestamp2 = int(time.time())
            try:
                var_data = shopee_p.item_GetItemDetail(item_id, partner_id, shopid, timestamp2)
            except Exception as e:
                print "item_GetItemDetail获取数据报错：shopid: %s, partner_id: %s, item_id: %s" % (shopid, partner_id, item_id)
                print repr(e)
                error_dict = dict()
                error_dict['ShopName'] = shopname
                error_dict['Shopid'] = shopid
                error_dict['ItemID'] = item_id
                error_dict['RefreshTime'] = datetime.datetime.now()
                error_dict['Description'] = repr(e)
                error_dict['Status'] = '-1'
                if error_dict:
                    save_error_info_detail2(**error_dict)
                continue
            try:
                var_data = json.loads(var_data.content)
            except Exception as e:
                print "item_GetItemDetail报错：shopid: %s, partner_id: %s, item_id: %s" % (shopid, partner_id, item_id)
                print var_data.content
                error_dict = dict()
                error_dict['ShopName'] = shopname
                error_dict['Shopid'] = shopid
                error_dict['ItemID'] = item_id
                error_dict['RefreshTime'] = datetime.datetime.now()
                error_dict['Description'] = repr(e)
                error_dict['Status'] = '-1'
                if error_dict:
                    save_error_info_detail2(**error_dict)
                continue
            try:
                var_d = var_data['item']
            except Exception as e:
                print "shopid: %s, partner_id: %s, item_id: %s, error: %s" % (shopid, partner_id, item_id,  repr(e))
                if var_data.get('error') == 'error_auth':
                    delete_ItemID(item_id, shopid)
                    continue
                error_dict = dict()
                error_dict['ShopName'] = shopname
                error_dict['Shopid'] = shopid
                error_dict['ItemID'] = item_id
                error_dict['ItemSKU'] = item_dict['ItemSKU']
                error_dict['SKU'] = item_dict['SKU']
                error_dict['MainSKU'] = item_dict['MainSKU']
                error_dict['RefreshTime'] = datetime.datetime.now()
                error_dict['Description'] = json.dumps(var_data) + '||||' + repr(e)
                error_dict['Status'] = '-1'
                error_dict_tuple = (
                    error_dict['ShopName'], error_dict['Shopid'], error_dict['ItemID'], error_dict['ItemSKU'], error_dict['SKU'],
                    error_dict['MainSKU'], error_dict['RefreshTime'], error_dict['Description'], error_dict['Status'],
                    error_dict['ShopName'], error_dict['Shopid'], error_dict['SKU'], error_dict['MainSKU'], error_dict['RefreshTime'],
                    error_dict['Description'], error_dict['Status']
                )
                error_data['datas'].append(error_dict_tuple)
                if error_data['datas']:
                    save_error_info_detail(**error_data)
                continue
            if var_d:
                item_dict['Price'] = var_d.get('price')
                item_dict['Original_price'] = var_d.get('original_price')
                item_dict['PackageWidth'] = var_d.get('package_width')
                item_dict['PackageLength'] = var_d.get('package_length')
                item_dict['PackageHeight'] = var_d.get('package_height')
                item_dict['CmtCount'] = var_d.get('cmt_count')
                item_dict['Conditions'] = var_d.get('condition')
                item_dict['SizeChart'] = var_d.get('size_chart')
                item_dict['Currency'] = var_d.get('currency').replace("'", "")
                item_dict['Weight'] = var_d.get('weight')
                item_dict['Likes'] = var_d.get('likes')
                item_dict['Image'] = var_d.get('images')[0] if var_d.get('images') else ''
                item_dict['ExtraImages'] = ','.join(var_d.get('images')) if var_d.get('images') else ''
                item_dict['Views'] = var_d.get('views')
                item_dict['DaysToShip'] = var_d.get('days_to_ship')
                item_dict['HasVariation'] = var_d.get('has_variation')
                item_dict['RatingStar'] = var_d.get('rating_star')
                item_dict['Sales'] = var_d.get('sales')
                item_dict['Title'] = var_d.get('name')
                item_dict['CategoryId'] = var_d.get('category_id')
                item_dict['DateUploaded'] = var_d.get('create_time')
                if item_dict['DateUploaded']:
                    item_dict['DateUploaded'] = (datetime.datetime.utcfromtimestamp(var_d.get('create_time'))+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
                item_dict['LastUpdated'] = var_d.get('update_time')
                if item_dict['LastUpdated']:
                    item_dict['LastUpdated'] = (datetime.datetime.utcfromtimestamp(var_d.get('update_time'))+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
                item_dict['RefreshTime'] = datetime.datetime.now()
                item_dict['Stock'] = var_d.get('stock')
                item_dict['Description'] = var_d.get('description')
                if var_d.get('status') == 'NORMAL':
                    item_dict['Status'] = '1'
                elif var_d.get('status') == 'BANNED':
                    item_dict['Status'] = '0'
                elif var_d.get('Status') == 'DELETED':
                    item_dict['Status'] = '2'
                else:
                    item_dict['Status'] = var_d.get('status')
                orders7Days = 0
                Item_Shopstatus = []
                for v_d_v in var_d.get('variations', []):
                    var_dict = dict()
                    var_dict['ItemID'] = item_id
                    var_dict['VariantID'] = v_d_v.get('variation_id')
                    var_dict['ItemSKU'] = var_d.get('item_sku')
                    orders7Days_shupsku = classsku_obj.get_shopsevensale_by_sku(v_d_v.get('variation_sku'))
                    if orders7Days_shupsku:
                        try:
                            orders7Days += int(orders7Days_shupsku)
                        except:
                            pass
                    var_dict['VariationSKU'] = v_d_v.get('variation_sku')
                    sku = classshopsku_obj.getskueach(var_dict['VariationSKU'])
                    var_dict['SKU'] = sku
                    var_dict['MainSKU'] = classsku_obj.get_bemainsku_by_sku(sku)
                    var_dict['Shopstatus'] = classskuobjs.get_goodsstatus_by_sku(sku)
                    if var_dict['Shopstatus']:
                        Item_Shopstatus.append(var_dict['Shopstatus'])
                    var_dict['Price'] = v_d_v.get('price')
                    var_dict['Original_price'] = v_d_v.get('original_price')
                    var_dict['Stock'] = v_d_v.get('stock')
                    var_dict['Different'] = v_d_v.get('name')
                    if v_d_v.get('status') == 'MODEL_NORMAL':
                        var_dict['Status'] = '1'
                    elif v_d_v.get('status') == 'MODEL_DELETED':
                        var_dict['Status'] = '0'
                    else:
                        var_dict['Status'] = v_d_v.get('status')
                    var_dict['CreateTime'] = v_d_v.get('create_time')
                    if var_dict['CreateTime']:
                        var_dict['CreateTime'] = (datetime.datetime.utcfromtimestamp(v_d_v.get('create_time'))+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
                    var_dict['UpdateTime'] = v_d_v.get('update_time')
                    if var_dict['UpdateTime']:
                        var_dict['UpdateTime'] = (datetime.datetime.utcfromtimestamp(v_d_v.get('update_time'))+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
                    try:
                        get_num = get_AvailableNum(var_dict['VariantID'], item_id, var_dict['SKU'], var_dict['VariationSKU'])
                        var_dict['AvailableNum'] = get_num[0]
                        var_dict['SellDays'] = get_num[1]
                    except Exception as e:
                        var_dict['AvailableNum'] = ''
                        var_dict['SellDays'] = ''
                    var_dict_tuple = (
                        var_dict['ItemID'], var_dict['VariantID'], var_dict['SKU'], var_dict['MainSKU'], var_dict['ItemSKU'],
                        var_dict['VariationSKU'], var_dict['Price'], var_dict['Original_price'], var_dict['Stock'], var_dict['Different'],
                        var_dict['Status'], var_dict['CreateTime'], var_dict['UpdateTime'], var_dict['Shopstatus'], var_dict['AvailableNum'],
                        var_dict['SellDays'], var_dict['ItemID'], var_dict['ItemSKU'], var_dict['Price'], var_dict['Original_price'],
                        var_dict['Stock'], var_dict['Different'], var_dict['Status'], var_dict['CreateTime'], var_dict['UpdateTime'],
                        var_dict['Shopstatus'], var_dict['AvailableNum'], var_dict['SellDays']
                    )
                    item_detail_data['datas'].append(var_dict_tuple)
                if len(item_detail_data['datas']) > 0:
                    save_variant_infos(**item_detail_data)
                    item_detail_data['datas'] = []
            else:
                # print "shopid: %s, partner_id: %s, item_id: %s" % (shopid, partner_id, item_id)
                # error_dict = dict()
                # error_dict['ShopName'] = shopname
                # error_dict['Shopid'] = shopid
                # error_dict['ItemID'] = item_id
                # error_dict['ItemSKU'] = item_dict['ItemSKU']
                # error_dict['SKU'] = item_dict['SKU']
                # error_dict['MainSKU'] = item_dict['MainSKU']
                # error_dict['RefreshTime'] = datetime.datetime.now()
                # error_dict['Description'] = u"暂没有商品信息"
                # error_dict['Status'] = '-1'
                # error_dict_tuple = (
                #     error_dict['ShopName'], error_dict['Shopid'], error_dict['ItemID'], error_dict['ItemSKU'], error_dict['SKU'],
                #     error_dict['MainSKU'], error_dict['RefreshTime'], error_dict['Description'], error_dict['Status'],
                #     error_dict['ShopName'], error_dict['Shopid'], error_dict['SKU'], error_dict['MainSKU'], error_dict['RefreshTime'],
                #     error_dict['Description'], error_dict['Status']
                # )
                # error_data['datas'].append(error_dict_tuple)
                # if error_data['datas']:
                #     save_error_info_detail(**error_data)
                delete_ItemID(item_id, shopid)
                continue
            item_dict['Orders7Days'] = orders7Days
            if not Item_Shopstatus:
                if int(item_dict['HasVariation']) == 0 or item_dict['HasVariation'] == False:
                    Item_Shopstatus.append(classskuobjs.get_goodsstatus_by_sku(item_dict['SKU']))
            item_dict['Shopstatus'] = ','.join(Item_Shopstatus)
            item_dict_tuple = (
                item_dict['ItemID'], item_dict['Shopid'], item_dict['ShopName'], item_dict['SKU'], item_dict['MainSKU'],
                item_dict['ItemSKU'], item_dict['Seller'], item_dict['Published'], item_dict['Price'], item_dict['Original_price'],
                item_dict['PackageWidth'], item_dict['PackageLength'], item_dict['PackageHeight'], item_dict['CmtCount'], item_dict['Conditions'],
                item_dict['SizeChart'], item_dict['Currency'], item_dict['Weight'], item_dict['Likes'], item_dict['Image'], item_dict['ExtraImages'],
                item_dict['Views'], item_dict['DaysToShip'], item_dict['HasVariation'], item_dict['RatingStar'], item_dict['Sales'], item_dict['Title'],
                item_dict['CategoryId'], item_dict['DateUploaded'], item_dict['LastUpdated'], item_dict['RefreshTime'], item_dict['Stock'],
                item_dict['Description'], item_dict['Status'], item_dict['Orders7Days'],item_dict['Shopstatus'],
                item_dict['Shopid'], item_dict['ShopName'], item_dict['SKU'], item_dict['MainSKU'], item_dict['ItemSKU'], item_dict['Seller'],
                item_dict['Published'], item_dict['Price'], item_dict['Original_price'], item_dict['PackageWidth'],
                item_dict['PackageLength'], item_dict['PackageHeight'], item_dict['CmtCount'], item_dict['Conditions'],
                item_dict['SizeChart'], item_dict['Currency'], item_dict['Weight'], item_dict['Likes'], item_dict['Image'], item_dict['ExtraImages'],
                item_dict['Views'], item_dict['DaysToShip'], item_dict['HasVariation'], item_dict['RatingStar'], item_dict['Sales'], item_dict['Title'],
                item_dict['CategoryId'], item_dict['DateUploaded'], item_dict['LastUpdated'], item_dict['RefreshTime'], item_dict['Stock'],
                item_dict['Description'], item_dict['Status'], item_dict['Orders7Days'],item_dict['Shopstatus']
            )
            item_data['datas'].append(item_dict_tuple)
        save_item_info(**item_data)
        if opid != '':
            isResult = t_shopee_oplogs_obj.MoreupdateNum(opid)
            assert isResult['errorcode'] == 0, "upload log error."
        item_data['datas'] = []
        count += 100
        try:
            if not more:
                if opid != '':
                    isResult = t_shopee_oplogs_obj.MoreupdateStatus(opid, 'over')
                    assert isResult['errorcode'] == 0, "upload log error."
                break
        except Exception as e:
            if len(Item_data) < 100:
                if opid != '':
                    isResult = t_shopee_oplogs_obj.MoreupdateStatus(opid, 'over')
                    assert isResult['errorcode'] == 0, "upload log error."
                break

def save_item_info(**kw):
    cursor = kw['cursor']
    sql = 'INSERT INTO t_shopee_online_info (ItemID, Shopid, ShopName, SKU, MainSKU, ItemSKU, Seller, Published, Price, ' \
          'Original_price, PackageWidth, PackageLength, PackageHeight, CmtCount, Conditions, SizeChart, Currency, Weight, Likes, Image, ' \
          'ExtraImages, Views, DaysToShip, HasVariation, RatingStar, Sales, Title, CategoryId, DateUploaded, LastUpdated, RefreshTime, ' \
          'Stock, Description, Status, Orders7Days, Shopstatus) ' \
          'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '\
          '%s, %s, %s, %s, %s, %s) ' \
          'ON DUPLICATE KEY UPDATE ' \
          'Shopid=%s, ShopName=%s, SKU=%s, MainSKU=%s, ItemSKU=%s, Seller=%s, Published=%s, Price=%s, Original_price=%s, '\
          'PackageWidth=%s, PackageLength=%s, PackageHeight=%s, CmtCount=%s, Conditions=%s, SizeChart=%s, Currency=%s, Weight=%s, Likes=%s, '\
          'Image=%s, ExtraImages=%s, Views=%s, DaysToShip=%s, HasVariation=%s, RatingStar=%s, Sales=%s, Title=%s, CategoryId=%s, '\
          'DateUploaded=%s, LastUpdated=%s, RefreshTime=%s, Stock=%s, Description=%s, Status=%s, Orders7Days=%s, Shopstatus=%s; '
    cursor.executemany(sql, kw['datas'])

def save_variant_infos(**kw):
    cursor = kw['cursor']
    sql = 'INSERT INTO t_shopee_online_info_detail (ItemID, VariantID, SKU, MainSKU, ItemSKU, VariationSKU, ' \
          'Price, Original_price, Stock, Different, Status, CreateTime, UpdateTime, Shopstatus, AvailableNum, SellDays) ' \
          'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ' \
          'ON DUPLICATE KEY UPDATE ' \
          'ItemID=%s, ItemSKU=%s, Price=%s, Original_price=%s, Stock=%s, Different=%s, Status=%s, CreateTime=%s, UpdateTime=%s,' \
          'Shopstatus=%s, AvailableNum=%s, SellDays=%s; '
    cursor.executemany(sql, kw['datas'])

def update_item_infos(**kw):
    cursor = kw['cursor']
    data = kw['datas'][0]
    sql = 'UPDATE t_shopee_online_info SET Price=%s, Original_price=%s, PackageWidth=%s, PackageLength=%s, ' \
        'PackageHeight=%s, CmtCount=%s, Conditions=%s, SizeChart="%s", Currency="%s", Weight=%s, Likes=%s, ' \
        'Image=%s, ExtraImages=%s, Views=%s, DaysToShip=%s, HasVariation=%s, RatingStar=%s, Sales=%s, Title=%s, CategoryId=%s, ' \
        'DateUploaded=%s, LastUpdated=%s, RefreshTime=%s, Stock=%s, Description=%s, Status=%s, Orders7Days=%s where ItemID=%s; '
    cursor.execute(sql, data)

def save_error_info(**kw):
    cursor = kw['cursor']
    sql = 'INSERT INTO t_shopee_online_info (ShopName, Shopid, Status, Description, RefreshTime)' \
          'VALUES (%s, %s, %s, %s, %s)'
    cursor.executemany(sql, kw['datas'])

def save_error_info_detail(**kw):
    cursor = kw['cursor']
    sql = 'INSERT INTO t_shopee_online_info (ShopName, Shopid, ItemID, ItemSKU, SKU, MainSKU, RefreshTime, Description, Status) ' \
          'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ' \
          'ON DUPLICATE KEY UPDATE ' \
          'ShopName=%s, Shopid=%s, SKU=%s, MainSKU=%s, Refreshtime=%s, Description=%s, Status=%s; '
    cursor.executemany(sql, kw['datas'])

def save_error_info_detail2(**kw):
    # cursor = kw['cursor']
    # sql = 'INSERT INTO t_shopee_online_info (ShopName, Shopid, ItemID, RefreshTime, Description, Status) ' \
    #       'VALUES (%s, %s, %s, %s, %s, %s) ' \
    #       'ON DUPLICATE KEY UPDATE ' \
    #       'ShopName=%s, Shopid=%s, Refreshtime=%s, Description=%s, Status=%s; '
    # cursor.executemany(sql, kw['datas'])
    try:
        td = t_shopee_online_info.objects.get(ItemID=kw.get('ItemID'))
        td.ShopName = kw.get('ShopName')
        td.Shopid = kw.get('Shopid')
        td.RefreshTime = kw.get('RefreshTime')
        td.Description = kw.get('Description')
        td.Status = kw.get('Status')
        td.save()
    except Exception as e:
        td = t_shopee_online_info(
            ItemID=kw.get('ItemID'),
            ShopName=kw.get('ShopName'),
            Shopid=kw.get('Shopid'),
            RefreshTime=kw.get('RefreshTime'),
            Description=kw.get('Description'),
            Status=kw.get('Status')
        )
        td.save()

def delete_ItemID(item_id, shopid):
    try:
        td = t_shopee_online_info.objects.get(ItemID=item_id, Shopid=shopid)
        td.delete()
        td_detail = t_shopee_online_info_detail.objects.filter(ItemID=item_id)
        for t_d in td_detail:
            t_d.delete()
    except Exception as e:
        pass

def get_shopname_time(cursor, partner_id, shopname, shopid):
    # cursor.execute('SELECT ItemId, RefreshTime FROM t_shopee_online_info WHERE ShopName=%s and RefreshTime is not NULL order by RefreshTime;', (shopname,))
    # last_time = cursor.fetchone()[1]
    cursor.execute('SELECT ItemId FROM t_shopee_online_info WHERE ShopName=%s and RefreshTime is NULL', (shopname,))
    itemId_list = list()
    for i in cursor.fetchall():
        itemId_list.append(i[0])
    if itemId_list:
        # RefreshTime为空的产品重新更新
        update_shopee_info_detail(shopname, partner_id, shopid, itemId_list)

def update_shopee_info_detail(shopname, partner_id, shopid, itemids):
    db_conn = connection
    cursor = db_conn.cursor()
    redis_conn = get_redis_connection(alias='product')
    classsku_obj = classsku(db_cnxn=db_conn, redis_cnxn=redis_conn)
    classshopsku_obj = classshopsku(db_conn=db_conn, redis_conn=redis_conn)
    classskuobjs = classsku(db_cnxn=db_conn, redis_cnxn=redis_conn)
    item_data = dict()
    item_data['cursor'] = cursor
    item_data['datas'] = list()
    item_detail_data = dict()
    item_detail_data['cursor'] = cursor
    item_detail_data['datas'] = list()
    shopee_p = Shopee_Public_API(shopname)
    for item_id in itemids:
        item_dict = dict()
        item_dict['ItemID'] = item_id
        item_dict['ShopName'] = shopname
        item_dict['Shopid'] = shopid
        timestamp = int(time.time())
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
        try:
            var_data = shopee_p.item_GetItemDetail(item_id, partner_id, shopid, timestamp)
        except Exception as e:
            print "item_GetItemDetail获取数据报错：shopid: %s, partner_id: %s, item_id: %s" % (shopid, partner_id, item_id)
            print repr(e)
            error_dict = dict()
            error_dict['ShopName'] = shopname
            error_dict['Shopid'] = shopid
            error_dict['ItemID'] = item_id
            error_dict['RefreshTime'] = datetime.datetime.now()
            error_dict['Description'] = repr(e)
            error_dict['Status'] = '-1'
            if error_dict:
                save_error_info_detail2(**error_dict)
            continue
        try:
            var_data = json.loads(var_data.content)
        except Exception as e:
            print "item_GetItemDetail报错：shopid: %s, partner_id: %s, item_id: %s" % (shopid, partner_id, item_id)
            print var_data.content
            error_dict = dict()
            error_dict['ShopName'] = shopname
            error_dict['Shopid'] = shopid
            error_dict['ItemID'] = item_id
            error_dict['RefreshTime'] = datetime.datetime.now()
            error_dict['Description'] = repr(e)
            error_dict['Status'] = '-1'
            if error_dict:
                save_error_info_detail2(**error_dict)
            continue
        try:
            var_d = var_data['item']
        except Exception as e:
            print "shopid: %s, partner_id: %s, item_id: %s, error: %s" % (shopid, partner_id, item_id,  repr(e))
            if var_data.get('error') == 'error_auth':
                delete_ItemID(item_id, shopid)
                continue
            error_dict = dict()
            error_dict['ShopName'] = shopname
            error_dict['Shopid'] = shopid
            error_dict['ItemID'] = item_id
            error_dict['ItemSKU'] = item_dict['ItemSKU']
            error_dict['SKU'] = item_dict['SKU']
            error_dict['MainSKU'] = item_dict['MainSKU']
            error_dict['RefreshTime'] = datetime.datetime.now()
            error_dict['Description'] = json.dumps(var_data) + '||||' + repr(e)
            error_dict['Status'] = '-1'
            error_dict_tuple = (
                error_dict['ShopName'], error_dict['Shopid'], error_dict['ItemID'], error_dict['ItemSKU'], error_dict['SKU'],
                error_dict['MainSKU'], error_dict['RefreshTime'], error_dict['Description'], error_dict['Status'],
                error_dict['ShopName'], error_dict['Shopid'], error_dict['SKU'], error_dict['MainSKU'], error_dict['RefreshTime'],
                error_dict['Description'], error_dict['Status']
            )
            error_data['datas'].append(error_dict_tuple)
            if error_data['datas']:
                save_error_info_detail(**error_data)
            continue
        if var_d:
            item_dict['ItemSKU'] = var_d.get('item_sku')
            item_sku = classshopsku_obj.getskueach(item_dict['ItemSKU'])
            item_dict['SKU'] = item_sku
            item_dict['MainSKU'] = classsku_obj.get_bemainsku_by_sku(item_sku)
            item_dict['Price'] = var_d.get('price')
            item_dict['Original_price'] = var_d.get('original_price')
            item_dict['PackageWidth'] = var_d.get('package_width')
            item_dict['PackageLength'] = var_d.get('package_length')
            item_dict['PackageHeight'] = var_d.get('package_height')
            item_dict['CmtCount'] = var_d.get('cmt_count')
            item_dict['Conditions'] = var_d.get('condition')
            item_dict['SizeChart'] = var_d.get('size_chart')
            item_dict['Currency'] = var_d.get('currency').replace("'", "")
            item_dict['Weight'] = var_d.get('weight')
            item_dict['Likes'] = var_d.get('likes')
            item_dict['Image'] = var_d.get('images')[0] if var_d.get('images') else ''
            item_dict['ExtraImages'] = ','.join(var_d.get('images')) if var_d.get('images') else ''
            item_dict['Views'] = var_d.get('views')
            item_dict['DaysToShip'] = var_d.get('days_to_ship')
            item_dict['HasVariation'] = var_d.get('has_variation')
            item_dict['RatingStar'] = var_d.get('rating_star')
            item_dict['Sales'] = var_d.get('sales')
            item_dict['Title'] = var_d.get('name')
            item_dict['CategoryId'] = var_d.get('category_id')
            item_dict['DateUploaded'] = var_d.get('create_time')
            if item_dict['DateUploaded']:
                item_dict['DateUploaded'] = (datetime.datetime.utcfromtimestamp(var_d.get('create_time'))+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
            item_dict['LastUpdated'] = var_d.get('update_time')
            if item_dict['LastUpdated']:
                item_dict['LastUpdated'] = (datetime.datetime.utcfromtimestamp(var_d.get('update_time'))+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
            item_dict['RefreshTime'] = datetime.datetime.now()
            item_dict['Stock'] = var_d.get('stock')
            item_dict['Description'] = var_d.get('description')
            if var_d.get('status') == 'NORMAL':
                item_dict['Status'] = '1'
            elif var_d.get('status') == 'BANNED':
                item_dict['Status'] = '0'
            elif var_d.get('status') == 'DELETED':
                item_dict['Status'] = '2'
            else:
                item_dict['Status'] = var_d.get('status')
            orders7Days = 0
            Item_Shopstatus = []
            for v_d_v in var_d.get('variations', []):
                var_dict = dict()
                var_dict['ItemID'] = item_id
                var_dict['VariantID'] = v_d_v.get('variation_id')
                var_dict['ItemSKU'] = var_d.get('item_sku')
                orders7Days_shupsku = classsku_obj.get_shopsevensale_by_sku(v_d_v.get('variation_sku'))
                if orders7Days_shupsku:
                    try:
                        orders7Days += int(orders7Days_shupsku)
                    except:
                        pass
                var_dict['VariationSKU'] = v_d_v.get('variation_sku')
                sku = classshopsku_obj.getskueach(var_dict['VariationSKU'])
                var_dict['SKU'] = sku
                var_dict['MainSKU'] = classsku_obj.get_bemainsku_by_sku(sku)
                var_dict['Shopstatus'] = classskuobjs.get_goodsstatus_by_sku(sku)
                if var_dict['Shopstatus']:
                    Item_Shopstatus.append(var_dict['Shopstatus'])
                var_dict['Price'] = v_d_v.get('price')
                var_dict['Original_price'] = v_d_v.get('original_price')
                var_dict['Stock'] = v_d_v.get('stock')
                var_dict['Different'] = v_d_v.get('name')
                if v_d_v.get('status') == 'MODEL_NORMAL':
                    var_dict['Status'] = '1'
                elif v_d_v.get('status') == 'MODEL_DELETED':
                    var_dict['Status'] = '0'
                else:
                    var_dict['Status'] = v_d_v.get('status')
                var_dict['CreateTime'] = v_d_v.get('create_time')
                if var_dict['CreateTime']:
                    var_dict['CreateTime'] = (datetime.datetime.utcfromtimestamp(v_d_v.get('create_time'))+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
                var_dict['UpdateTime'] = v_d_v.get('update_time')
                if var_dict['UpdateTime']:
                    var_dict['UpdateTime'] = (datetime.datetime.utcfromtimestamp(v_d_v.get('update_time'))+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
                try:
                    get_num = get_AvailableNum(var_dict['VariantID'], item_id, var_dict['SKU'], var_dict['VariationSKU'])
                    var_dict['AvailableNum'] = get_num[0]
                    var_dict['SellDays'] = get_num[1]
                except Exception as e:
                    var_dict['AvailableNum'] = ''
                    var_dict['SellDays'] = ''
                var_dict_tuple = (
                    var_dict['ItemID'], var_dict['VariantID'], var_dict['SKU'], var_dict['MainSKU'], var_dict['ItemSKU'],
                    var_dict['VariationSKU'], var_dict['Price'], var_dict['Original_price'], var_dict['Stock'], var_dict['Different'],
                    var_dict['Status'], var_dict['CreateTime'], var_dict['UpdateTime'], var_dict['Shopstatus'], var_dict['AvailableNum'],
                    var_dict['SellDays'], var_dict['ItemID'], var_dict['ItemSKU'], var_dict['Price'], var_dict['Original_price'],
                    var_dict['Stock'], var_dict['Different'], var_dict['Status'], var_dict['CreateTime'], var_dict['UpdateTime'],
                    var_dict['Shopstatus'], var_dict['AvailableNum'], var_dict['SellDays']
                )
                item_detail_data['datas'].append(var_dict_tuple)
            if len(item_detail_data['datas']) > 0:
                save_variant_infos(**item_detail_data)
                item_detail_data['datas'] = []
        else:
            delete_ItemID(item_id, shopid)
            continue
        
        item_dict['Orders7Days'] = orders7Days
        if not Item_Shopstatus:
            if int(item_dict['HasVariation']) == 0 or item_dict['HasVariation'] == False:
                if classskuobjs.get_goodsstatus_by_sku(item_dict['SKU']):
                    Item_Shopstatus.append(classskuobjs.get_goodsstatus_by_sku(item_dict['SKU']))
        item_dict['Shopstatus'] = ','.join(Item_Shopstatus)
        item_dict_tuple = (
            item_dict['ItemID'], item_dict['Shopid'], item_dict['ShopName'], item_dict['SKU'], item_dict['MainSKU'],
            item_dict['ItemSKU'], item_dict['Seller'], item_dict['Published'], item_dict['Price'], item_dict['Original_price'],
            item_dict['PackageWidth'], item_dict['PackageLength'], item_dict['PackageHeight'], item_dict['CmtCount'], item_dict['Conditions'],
            item_dict['SizeChart'], item_dict['Currency'], item_dict['Weight'], item_dict['Likes'], item_dict['Image'], item_dict['ExtraImages'],
            item_dict['Views'], item_dict['DaysToShip'], item_dict['HasVariation'], item_dict['RatingStar'], item_dict['Sales'], item_dict['Title'],
            item_dict['CategoryId'], item_dict['DateUploaded'], item_dict['LastUpdated'], item_dict['RefreshTime'], item_dict['Stock'],
            item_dict['Description'], item_dict['Status'], item_dict['Orders7Days'],item_dict['Shopstatus'],
            item_dict['Shopid'], item_dict['ShopName'], item_dict['SKU'], item_dict['MainSKU'], item_dict['ItemSKU'], item_dict['Seller'],
            item_dict['Published'], item_dict['Price'], item_dict['Original_price'], item_dict['PackageWidth'],
            item_dict['PackageLength'], item_dict['PackageHeight'], item_dict['CmtCount'], item_dict['Conditions'],
            item_dict['SizeChart'], item_dict['Currency'], item_dict['Weight'], item_dict['Likes'], item_dict['Image'], item_dict['ExtraImages'],
            item_dict['Views'], item_dict['DaysToShip'], item_dict['HasVariation'], item_dict['RatingStar'], item_dict['Sales'], item_dict['Title'],
            item_dict['CategoryId'], item_dict['DateUploaded'], item_dict['LastUpdated'], item_dict['RefreshTime'], item_dict['Stock'],
            item_dict['Description'], item_dict['Status'], item_dict['Orders7Days'],item_dict['Shopstatus']
        )
        item_data['datas'].append(item_dict_tuple)
        save_item_info(**item_data)
        item_data['datas'] = []
