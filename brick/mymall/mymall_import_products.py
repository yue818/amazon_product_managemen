# -*- coding: utf-8 -*-

"""
 @desc:
 @author: 孙健
 @site:
 @Warning:
    1. first line echo "sep=;"
    2. Replace csv '\";' to '";'' & reqplace '\"' to ''
    3. Then save sa xlsx file
"""


# import os
# import json
import xlrd
import datetime

from django_redis import get_redis_connection
from django.conf import settings
from django.db import connection

from brick.public.upload_to_oss import get_obj_from_oss
from brick.classredis.classsku import classsku
from brick.classredis.classshopsku import classshopsku
from brick.pricelist.calculate_price import calculate_price

from mymall_app.table.t_mymall_online_info import t_mymall_online_info
from mymall_app.table.t_mymall_upload_product_info import t_mymall_upload_product_info

MYMALL_EXCEL_HEADS = [
    'SKU',
    'enable',
    'stock',
    'name',
    'price',
    'old_price',
    'color',
    'size',
    'brand',
    'tags',
    'UPC',
    'description',
    'main_image_url',
    'image_url_1',
    'image_url_2',
    'image_url_3',
    'image_url_4',
    'image_url_5',
    'image_url_6',
    'image_url_7',
    'image_url_8',
    'image_url_9',
    'image_url_10',
    'shipping_time',
    'shipping_price',
    'landing_page_url',
    'product_id',
    'product_variation_id',
]


def mymall_import_products(salling_file='', shopname='', uploadfile_id='', import_user=''):
    sRes = {'code': '0', 'message': ''}
    salling_res = None
    if salling_file:
        salling_res = handle_mymall_products(filename_params=salling_file, flag='True', shopname=shopname)

    upload_obj = t_mymall_upload_product_info.objects.get(pk=uploadfile_id)
    import_res = ''
    if salling_res and salling_res['code'] == '0':
        if salling_res:
            import_res += 'import salling file result: %s, ' % (salling_res['message'])
        else:
            import_res += 'import salling file result: %s, ' % ('No salling file')
        update_upload_res(upload_obj, import_user, import_res, True)
    else:
        sRes['code'] = '-1'
        if salling_res:
            import_res += 'import salling file result: %s, ' % (salling_res['message'])
        else:
            import_res += 'import salling file result: %s, ' % ('No salling file')
        update_upload_res(upload_obj, import_user, import_res, False)

    sRes['message'] = import_res
    return sRes


def handle_mymall_products(filename_params='', flag='True', shopname=''):

    start_read_file_time = datetime.datetime.now()
    print '============= start_read_file_time: %s' % start_read_file_time
    db_conn = connection
    redis_conn = get_redis_connection(alias='product')

    classsku_obj = classsku(db_cnxn=db_conn, redis_cnxn=redis_conn)
    classshopsku_obj = classshopsku(db_conn=db_conn, redis_conn=redis_conn)

    if not filename_params:
        return {'code': '-1', 'message': ' No file'}
    oss_file_obj = get_obj_from_oss(settings.BUCKETNAME_XLS)
    oss_res = oss_file_obj.get_obj_from_oss(filename_params)
    file_obj = oss_res['result']
    if oss_res['errorcode'] != 0 or file_obj == '':
        return {'code': '-1', 'message': 'Get oss file Failed'}

    # filename = settings.MEDIA_ROOT + 'mymall_salling_product_file/2018/06/mall_mycom_products_1.xlsx'

    # if True:
    try:
        pro_wb = xlrd.open_workbook(filename=None, file_contents=file_obj.read())
        # pro_wb = xlrd.open_workbook(filename=filename)

        end_read_file_time = datetime.datetime.now()
        print '============= end_read_file_time: %s' % end_read_file_time
        print '============= handle_read_file_time: %s' % (end_read_file_time - start_read_file_time).total_seconds()

        start_insert_data_time = datetime.datetime.now()
        print '============= start_insert_data_time: %s' % start_insert_data_time

        sheet_name = pro_wb.sheet_names()[0]
        sheet_obj = pro_wb.sheet_by_name(sheet_name)
        nrows = sheet_obj.nrows
        heads = sheet_obj.row_values(0)
        head_dict = dict()
        for k, v in enumerate(heads):
            if v in MYMALL_EXCEL_HEADS:
                head_dict[v] = k

        sku_list = list()
        main_sku_list = list()
        shop_sku_list = list()
        extra_image_list = list()
        status_list = list()
        cursor = db_conn.cursor()
        mm_infos_dict = dict()
        mm_infos_detail_dict = dict()
        mm_infos_dict['cursor'] = cursor
        mm_infos_dict['datas'] = list()
        mm_infos_detail_dict['cursor'] = cursor
        mm_infos_detail_dict['datas'] = list()

        num = 1
        while True:
            if num + 1 >= nrows:
                break

            # if num > 10000:
            #     break

            for row in range(num, nrows):

                shop_sku = str(sheet_obj.cell_value(row, head_dict['SKU']))
                sku = classshopsku_obj.getSKU(shop_sku)
                mainsku = classsku_obj.get_bemainsku_by_sku(sku)
                weight = classsku_obj.get_weight_by_sku(sku)
                enable = str(sheet_obj.cell_value(row, head_dict['enable']))

                if enable == '1':
                    status = enable
                else:
                    status = '0'

                try:
                    quantity = int(sheet_obj.cell_value(row, head_dict['stock']))
                except Exception as e:
                    print '[x] row: %s, Get MyMall product quantity error: %s' % (row, e)
                    quantity = 0
                title = str(sheet_obj.cell_value(row, head_dict['name']))
                price = str(sheet_obj.cell_value(row, head_dict['price']))
                msrp = str(sheet_obj.cell_value(row, head_dict['old_price']))
                color = str(sheet_obj.cell_value(row, head_dict['color']))
                size = str(sheet_obj.cell_value(row, head_dict['size']))
                tags = str(sheet_obj.cell_value(row, head_dict['tags']))
                brand = str(sheet_obj.cell_value(row, head_dict['brand']))
                UPC = str(sheet_obj.cell_value(row, head_dict['UPC']))
                description = str(sheet_obj.cell_value(row, head_dict['description']))
                main_image_url = str(sheet_obj.cell_value(row, head_dict['main_image_url']))
                extra_images_dict = dict()
                extra_images_dict['image_url_1'] = str(sheet_obj.cell_value(row, head_dict['image_url_1']))
                extra_images_dict['image_url_2'] = str(sheet_obj.cell_value(row, head_dict['image_url_2']))
                extra_images_dict['image_url_3'] = str(sheet_obj.cell_value(row, head_dict['image_url_3']))
                extra_images_dict['image_url_4'] = str(sheet_obj.cell_value(row, head_dict['image_url_4']))
                extra_images_dict['image_url_5'] = str(sheet_obj.cell_value(row, head_dict['image_url_5']))
                extra_images_dict['image_url_6'] = str(sheet_obj.cell_value(row, head_dict['image_url_6']))
                extra_images_dict['image_url_7'] = str(sheet_obj.cell_value(row, head_dict['image_url_7']))
                extra_images_dict['image_url_8'] = str(sheet_obj.cell_value(row, head_dict['image_url_8']))
                extra_images_dict['image_url_9'] = str(sheet_obj.cell_value(row, head_dict['image_url_9']))
                extra_images_dict['image_url_10'] = str(sheet_obj.cell_value(row, head_dict['image_url_10']))
                shipping_time = str(sheet_obj.cell_value(row, head_dict['shipping_time']))
                shipping_price = str(sheet_obj.cell_value(row, head_dict['shipping_price']))
                landing_page_url = str(sheet_obj.cell_value(row, head_dict['landing_page_url']))
                product_id = str(sheet_obj.cell_value(row, head_dict['product_id']))
                product_variation_id = str(sheet_obj.cell_value(row, head_dict['product_variation_id']))

                # print '11111111111111111111 shop_sku: %s' % shop_sku
                # print '11111111111111111111 enable: %s' % enable
                # print '11111111111111111111 title: %s' % title
                # print '11111111111111111111 price: %s' % price
                # print '11111111111111111111 msrp: %s' % msrp
                # print '11111111111111111111 color: %s' % color
                # print '11111111111111111111 size: %s' % size
                # print '11111111111111111111 tags: %s' % tags
                # print '11111111111111111111 brand: %s' % brand
                # print '11111111111111111111 UPC: %s' % UPC
                # print '11111111111111111111 description: %s' % description
                # print '11111111111111111111 main_image_url: %s' % main_image_url
                # print '11111111111111111111 extra_images_dict: %s' % extra_images_dict
                # print '11111111111111111111 shipping_time: %s' % shipping_time
                # print '11111111111111111111 shipping_price: %s' % shipping_price
                # print '11111111111111111111 landing_page_url: %s' % landing_page_url
                # print '11111111111111111111 product_id: %s' % product_id
                # print '11111111111111111111 product_variation_id: %s' % product_variation_id

                if not price and not msrp:
                    continue
                elif price or msrp:
                    try:
                        float(price)
                    except Exception as e:
                        print e
                        continue

                    try:
                        float(msrp)
                    except Exception as e:
                        print e
                        continue
                else:
                    pass

                try:
                    next_product_id = str(sheet_obj.cell_value(row + 1, head_dict['product_id']))
                except Exception as e:
                    next_product_id = ''

                mymall_product_detail_info = dict()
                mymall_product_detail_info['ProductID'] = product_id
                mymall_product_detail_info['VariantID'] = product_variation_id
                mymall_product_detail_info['SKU'] = sku
                mymall_product_detail_info['MainSKU'] = mainsku
                mymall_product_detail_info['ShopSKU'] = shop_sku
                mymall_product_detail_info['Price'] = price
                mymall_product_detail_info['Quantity'] = quantity
                mymall_product_detail_info['Status'] = status
                mymall_product_detail_info['Shipping'] = shipping_price
                mymall_product_detail_info['ShippingTime'] = shipping_time
                mymall_product_detail_info['Color'] = color
                mymall_product_detail_info['Size'] = size
                mymall_product_detail_info['Msrp'] = msrp
                mymall_product_detail_info['Weight'] = weight
                mymall_product_detail_info['cursor'] = cursor

                mymall_product_detail_info_tuple = (
                    mymall_product_detail_info['ProductID'], mymall_product_detail_info['VariantID'], mymall_product_detail_info['SKU'], mymall_product_detail_info['MainSKU'], mymall_product_detail_info['ShopSKU'], mymall_product_detail_info['Price'], mymall_product_detail_info['Quantity'], mymall_product_detail_info['Status'],
                    mymall_product_detail_info['Shipping'], mymall_product_detail_info['ShippingTime'], mymall_product_detail_info['Color'], mymall_product_detail_info['Size'], mymall_product_detail_info['Msrp'], mymall_product_detail_info['Weight'],
                    mymall_product_detail_info['Price'], mymall_product_detail_info['Quantity'], mymall_product_detail_info['Status'], mymall_product_detail_info['Shipping'], mymall_product_detail_info['ShippingTime'], mymall_product_detail_info['Color'], mymall_product_detail_info['Size'], mymall_product_detail_info['Msrp'], mymall_product_detail_info['Weight'],
                )
                mm_infos_detail_dict['datas'].append(mymall_product_detail_info_tuple)

                if product_id != next_product_id:

                    for i in range(1, 11):
                        image_num = 'image_url_' + str(i)
                        if extra_images_dict[image_num]:
                            extra_image_list.append(extra_images_dict[image_num])
                    if sku:
                        sku_list.append(sku)
                    if mainsku and mainsku not in main_sku_list:
                        main_sku_list.append(mainsku)
                    if shop_sku:
                        shop_sku_list.append(shop_sku)
                    if status:
                        status_list.append(status)

                    if '1' in status_list:
                        pro_status = '1'
                    else:
                        pro_status = '0'

                    extra_images = ','.join(extra_image_list)
                    skus = ','.join(sku_list)
                    mainskus = ','.join(main_sku_list)
                    shop_skus = ','.join(shop_sku_list)

                    if len(mainskus) >= 255:
                        mainskus = mainskus[:250]

                    mymall_product_info = dict()
                    mymall_product_info['ProductID'] = product_id
                    mymall_product_info['ShopName'] = shopname
                    mymall_product_info['Title'] = title
                    mymall_product_info['SKU'] = skus
                    mymall_product_info['MainSKU'] = mainskus
                    mymall_product_info['ShopSKU'] = shop_skus
                    mymall_product_info['RefreshTime'] = datetime.datetime.now()
                    mymall_product_info['Tags'] = tags
                    mymall_product_info['Brand'] = brand
                    mymall_product_info['Description'] = description
                    mymall_product_info['LandingPageUrl'] = landing_page_url
                    mymall_product_info['Upc'] = UPC
                    mymall_product_info['Image'] = main_image_url
                    mymall_product_info['ExtraImages'] = extra_images
                    mymall_product_info['Status'] = pro_status
                    mymall_product_info['cursor'] = cursor

                    mymall_product_info_tuple = (
                        mymall_product_info['ProductID'], mymall_product_info['ShopName'], mymall_product_info['Title'], mymall_product_info['SKU'], mymall_product_info['MainSKU'], mymall_product_info['ShopSKU'], mymall_product_info['RefreshTime'],
                        mymall_product_info['Tags'], mymall_product_info['Brand'], mymall_product_info['Description'], mymall_product_info['LandingPageUrl'], mymall_product_info['Upc'], mymall_product_info['Image'], mymall_product_info['ExtraImages'], mymall_product_info['Status'],
                        mymall_product_info['Title'], mymall_product_info['RefreshTime'], mymall_product_info['Tags'], mymall_product_info['Brand'], mymall_product_info['Description'],
                        mymall_product_info['LandingPageUrl'], mymall_product_info['Upc'], mymall_product_info['Image'], mymall_product_info['ExtraImages'], mymall_product_info['Status'],
                    )
                    mm_infos_dict['datas'].append(mymall_product_info_tuple)

                    # update_mymall_info(**mymall_product_info)

                    sku_list = []
                    main_sku_list = []
                    shop_sku_list = []
                    extra_image_list = []
                    status_list = []
                    if row + 1 == nrows:
                        num = row + 1
                        break
                    if (row - num) > 2000:
                        num = row + 1
                        break
                else:
                    if sku:
                        sku_list.append(sku)
                    if mainsku and mainsku not in main_sku_list:
                        main_sku_list.append(mainsku)
                    if shop_sku:
                        shop_sku_list.append(shop_sku)
                    if status:
                        status_list.append(status)

            update_mymall_info(**mm_infos_dict)
            update_mymall_info_detail(**mm_infos_detail_dict)

            mm_infos_dict['datas'] = []
            mm_infos_detail_dict['datas'] = []

        cursor.execute('commit;')
        cursor.close()

    except Exception as e:
        return {'code': '-1', 'message': '%s' % str(e)}

    end_insert_data_time = datetime.datetime.now()
    print '============= end_insert_data_time: %s' % end_insert_data_time
    print '============= handle_insert_data_time: %s' % (end_insert_data_time - start_insert_data_time).total_seconds()

    return {'code': '0', 'message': 'SUCCESS'}


def update_mymall_info_detail(**kw):
    cursor = kw['cursor']

    sql = 'INSERT INTO t_mymall_online_info_detail (ProductID, VariantID, SKU, MainSKU, ShopSKU, ' \
          'Price, Quantity, Status, Shipping, ShippingTime, Color, Size, Msrp, Weight) ' \
          'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ' \
          'ON DUPLICATE KEY UPDATE ' \
          'Price=%s, Quantity=%s, Status=%s, Shipping=%s, ShippingTime=%s, Color=%s, Size=%s, Msrp=%s, Weight=%s;'

    # sql = 'INSERT INTO t_mymall_online_info_detail_test (ProductID, VariantID, SKU, MainSKU, ShopSKU, ' \
    #       'Price, Quantity, Status, Shipping, ShippingTime, Color, Size, Msrp, Weight) ' \
    #       'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    cursor.executemany(sql, kw['datas'])


def update_mymall_info(**kw):
    cursor = kw['cursor']

    sql = "INSERT INTO t_mymall_online_info (ProductID, ShopName, Title, SKU, MainSKU, ShopSKU, " \
          "RefreshTime, Tags, Brand, Description, LandingPageUrl, Upc, Image, ExtraImages, Status) " \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) " \
          "ON DUPLICATE KEY UPDATE Title=%s, RefreshTime=%s, Tags=%s, Brand=%s, Description=%s, LandingPageUrl=%s, " \
          "Upc=%s, Image=%s, ExtraImages=%s, Status=%s;"

    # sql = "INSERT INTO t_mymall_online_info_test (ProductID, ShopName, Title, SKU, MainSKU, ShopSKU, " \
    #       "RefreshTime, Tags, Brand, Description, LandingPageUrl, Upc, Image, ExtraImages, Status) " \
    #       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    cursor.executemany(sql, kw['datas'])


def get_mymall_profitrate(price, sku):
    sellingPrice = price.split('~')
    calculate_price_obj = calculate_price(sku)

    try:
        profitrate_min = calculate_price_obj.calculate_profitRate(sellingPrice[0], platformCountryCode='ALIEXPRESS-RUS', DestinationCountryCode='RUS')
    except:
        profitrate_min = ''
    if profitrate_min:
        min_profitrate = '%.2f' % float(profitrate_min['profitRate'])
    else:
        min_profitrate = ''

    try:
        profitrate_max = calculate_price_obj.calculate_profitRate(sellingPrice[0], platformCountryCode='ALIEXPRESS-RUS', DestinationCountryCode='RUS')
    except:
        profitrate_max = ''
    if profitrate_max:
        max_profitrate = '%.2f' % float(profitrate_max['profitRate'])
    else:
        max_profitrate = ''

    profitrate = min_profitrate + '% ~' + max_profitrate + '%'
    return profitrate


def update_upload_res(upload_obj, import_user, import_res, import_flag):
    upload_obj.ImportFlag = import_flag
    upload_obj.ImportUser = import_user
    upload_obj.ImportDatetime = datetime.datetime.now()
    upload_obj.ImportRes = import_res
    upload_obj.save()


def update_old_product_profit():
    start_time = datetime.datetime.now()
    print 'start_time: ', start_time
    ali_objs = t_mymall_online_info.objects.filter(ProfitRate__isnull=True, Status='1').values('id', 'Price', 'SKU')[0:1000]
    for obj in ali_objs:
        price = obj['Price']
        if not price:
            continue
        if price.find('-') != -1:
            price.replace('-', '~')
        if not obj['SKU']:
            continue
        sku = obj['SKU'].split(',')[0]
        profitrate = get_mymall_profitrate(price, sku)
        ali_pro_obj = t_mymall_online_info.objects.get(pk=obj['id'])
        ali_pro_obj.ProfitRate = profitrate
        ali_pro_obj.save()
    end_time = datetime.datetime.now()
    print 'end_time: ', end_time
    time_range = end_time - start_time
    print 'time_range: ', time_range
