#!/usr/bin/python
# -*- coding: utf-8 -*-

import xlrd
import json
# import os
import datetime

from django_redis import get_redis_connection
from django.conf import settings

from brick.public.upload_to_oss import get_obj_from_oss
from brick.db.dbconnect import run, execute_db
from brick.classredis.classsku import classsku
from brick.classredis.classshopsku import classshopsku
from brick.pricelist.calculate_price import calculate_price

from aliexpress_app.table.t_aliexpress_online_info import t_aliexpress_online_info
from aliexpress_app.table.t_aliexpress_online_info_detail import t_aliexpress_online_info_detail
from aliexpress_app.table.t_aliexpress_upload_product_info import t_aliexpress_upload_product_info

ALIEXPRESS_EXCEL_HEADS = [
    u'产品ID',
    u'产品名称',
    u'零售价',
    u'商家编码',
    u'价格信息',
    u'数据来源',
    u'库存',
    u'产品包装后的重量',
    u'商品图片',
]

ALIEXPRESS_EXCEL_HEADS_NEW = [
    u'产品ID',
    u'标题',
    u'售价(US $)',
    u'商家编码',
    u'来源',
    u'库存',
    u'图片路径',
]


def aliexpress_import_products(salling_file='', disable_file='', shopname='', uploadfile_id='', import_user=''):
    sRes = {'code': '0', 'message': ''}
    salling_res = None
    disable_res = None
    if salling_file:
        # salling_res = handle_aliexpress_products(filename=salling_file, flag='True', shopname=shopname)
        salling_res = handle_aliexpress_products_new(filename_params=salling_file, flag='True', shopname=shopname)
    if disable_file:
        # disable_res = handle_aliexpress_products(filename=disable_file, flag='False', shopname=shopname)
        disable_res = handle_aliexpress_products_new(filename_params=disable_file, flag='False', shopname=shopname)

    upload_obj = t_aliexpress_upload_product_info.objects.get(pk=uploadfile_id)
    import_res = ''
    if (salling_res and salling_res['code'] == '0') or (disable_res and disable_res['code'] == '0'):
        if salling_res:
            import_res += 'import salling file result: %s, ' % (salling_res['message'])
        else:
            import_res += 'import salling file result: %s, ' % ('No salling file')
        if disable_res:
            import_res += 'import disble file result: %s' % (disable_res['message'])
        else:
            import_res += 'import disble file result: %s' % ('No disble file')
        update_upload_res(upload_obj, import_user, import_res, True)
    else:
        sRes['code'] = '-1'
        if salling_res:
            import_res += 'import salling file result: %s, ' % (salling_res['message'])
        else:
            import_res += 'import salling file result: %s, ' % ('No salling file')
        if disable_res:
            import_res += 'import disble file result: %s' % (disable_res['message'])
        else:
            import_res += 'import disble file result: %s' % ('No disble file')
        update_upload_res(upload_obj, import_user, import_res, False)

    # 删除导入文件
    # if salling_file and salling_res and salling_res['code'] == '0':
    #     try:
    #         os.remove(salling_file)
    #     except:
    #         pass
    # if disable_file and disable_res and disable_res['code'] == '0':
    #     try:
    #         os.remove(disable_file)
    #     except:
    #         pass

    sRes['message'] = import_res
    return sRes


def handle_aliexpress_products(filename='', flag='True', shopname=''):

    db_res = run({})
    if db_res['errorcode'] == -1:
        print "result['errortext']: %s" % db_res['errortext']
        return
    db_conn = db_res['db_conn']
    redis_conn = get_redis_connection(alias='product')

    classsku_obj = classsku(db_cnxn=db_conn, redis_cnxn=redis_conn)
    classshopsku_obj = classshopsku(db_conn=db_conn, redis_conn=redis_conn)
    # classsku_obj = classsku(db_cnxn=db_conn)
    # classshopsku_obj = classshopsku(db_conn=db_conn)

    # if not filename:
    #     filename = u'/data/djangostack-1.9.7/apps/django/django_projects/Project/media/aliexpress_salling_product_file/2018/04/\u5b59\u5065-16_20_04-products.xls'

    # if not shopname:
    #     shopname = 'Ali-0001-fancyqube/PJ'

    try:
        pro_wb = xlrd.open_workbook(filename)
    except Exception as e:
        return {'code': '-1', 'message': '%s' % str(e)}
    sheet_name = pro_wb.sheet_names()[0]
    sheet_obj = pro_wb.sheet_by_name(sheet_name)
    nrows = sheet_obj.nrows
    heads = sheet_obj.row_values(0)
    head_dict = dict()
    for k, v in enumerate(heads):
        if v in ALIEXPRESS_EXCEL_HEADS:
            head_dict[v] = k

    for row in range(nrows):
        row += 1
        if row == nrows:
            break
        product_id = str(int(sheet_obj.cell_value(row, head_dict[u'产品ID'])))
        if product_id == '0':
            datasource = str(sheet_obj.cell_value(row, head_dict[u'数据来源']))
            product_id = datasource.split('/')[-1].split('.')[0]
        title = str(sheet_obj.cell_value(row, head_dict[u'产品名称']))
        price = str(sheet_obj.cell_value(row, head_dict[u'零售价']))
        # weight = str(sheet_obj.cell_value(row, head_dict[u'产品包装后的重量']))
        try:
            quantity = int(sheet_obj.cell_value(row, head_dict[u'库存']))
        except Exception as e:
            print 'Get Aliexpress product quantity error: %s' % e
            quantity = 0
        pic_url = str(sheet_obj.cell_value(row, head_dict[u'商品图片']))
        image = None
        if pic_url:
            image_url = pic_url.split(',')[0]
            if image_url.startswith('http'):
                image = image_url
            else:
                pass
        try:
            shopskus_info = json.loads(str(sheet_obj.cell_value(row, head_dict[u'价格信息'])))
            shopskus_info = shopskus_info['skuArray']
        except Exception as e:
            print 'Get shopskus price error %s' % e
            continue
        shopskus = list()
        sku_list = list()
        mainsku_list = list()
        weight_list = list()
        for shopsku in shopskus_info:
            shop_sku = shopsku[u'商家编码']
            shop_sku_quantity = shopsku[u'库存']
            shop_sku_price = shopsku[u'价格']
            sku = classshopsku_obj.getSKU(shop_sku)
            mainsku = classsku_obj.get_bemainsku_by_sku(sku)
            weight = classsku_obj.get_weight_by_sku(sku)
            ali_detail_info = dict()
            ali_detail_info['product_id'] = product_id
            ali_detail_info['sku'] = sku
            ali_detail_info['mainsku'] = mainsku
            ali_detail_info['shop_sku'] = shop_sku
            ali_detail_info['shop_sku_price'] = shop_sku_price
            ali_detail_info['shop_sku_quantity'] = shop_sku_quantity
            ali_detail_info['status'] = flag
            if weight:
                ali_detail_info['weight'] = float(weight)
            else:
                ali_detail_info['weight'] = None
            shopskus.append(shop_sku)
            update_aliexpress_info_detail(**ali_detail_info)
            if sku:
                sku_list.append(sku)
            if mainsku and mainsku not in mainsku_list:
                mainsku_list.append(mainsku)
            if weight:
                weight_list.append(float(weight))
            if not image:
                bmpurl = get_image_by_sku(sku, db_conn)
                if bmpurl:
                    image = bmpurl

        mainsku_list_str = None
        sku_list_str = None
        max_weight = None
        if mainsku_list:
            mainsku_list_str = ','.join(mainsku_list)
        if sku_list:
            sku_list_str = ','.join(sku_list)
        if weight_list:
            weight_list.sort()
            max_weight = weight_list[0]

        ali_info = dict()
        ali_info['product_id'] = product_id
        ali_info['title'] = title
        ali_info['price'] = price
        ali_info['shopskus'] = ','.join(shopskus)
        ali_info['quantity'] = quantity
        ali_info['mainsku_list_str'] = mainsku_list_str
        ali_info['sku_list_str'] = sku_list_str
        ali_info['status'] = flag
        ali_info['shopname'] = shopname
        ali_info['image'] = image
        ali_info['weight'] = max_weight
        update_aliexpress_info(**ali_info)
    return {'code': '0', 'message': 'SUCCESS'}


def handle_aliexpress_products_new(filename_params='', flag='True', shopname=''):
    # Excel not from zip

    db_res = run({})
    if db_res['errorcode'] == -1:
        print "result['errortext']: %s" % db_res['errortext']
        return
    db_conn = db_res['db_conn']
    redis_conn = get_redis_connection(alias='product')

    classsku_obj = classsku(db_cnxn=db_conn, redis_cnxn=redis_conn)
    classshopsku_obj = classshopsku(db_conn=db_conn, redis_conn=redis_conn)
    # classsku_obj = classsku(db_cnxn=db_conn)
    # classshopsku_obj = classshopsku(db_conn=db_conn)

    # if not filename:
    #     filename = u'/data/djangostack-1.9.7/apps/django/django_projects/Project/media/aliexpress_salling_product_file/2018/04/\u5b59\u5065-16_20_04-products.xls'

    # if not shopname:
    #     shopname = 'Ali-0001-fancyqube/PJ'

    # try:
    #     # pro_wb = xlrd.open_workbook(filename)
    #     pro_wb = xlrd.open_workbook(filename=None, file_contents=filename.read())
    # except Exception as e:
    #     return {'code': '-1', 'message': '%s' % str(e)}
    if not filename_params:
        return {'code': '-1', 'message': ' No file'}
    oss_file_obj = get_obj_from_oss(settings.BUCKETNAME_XLS)
    oss_res = oss_file_obj.get_obj_from_oss(filename_params)
    file_obj = oss_res['result']
    if oss_res['errorcode'] != 0 or file_obj == '':
        return {'code': '-1', 'message': 'Get oss file Failed'}
    try:
        pro_wb = xlrd.open_workbook(filename=None, file_contents=file_obj.read())
        # pro_wb = filename
        sheet_name = pro_wb.sheet_names()[0]
        sheet_obj = pro_wb.sheet_by_name(sheet_name)
        nrows = sheet_obj.nrows
        heads = sheet_obj.row_values(0)
        head_dict = dict()
        for k, v in enumerate(heads):
            if v in ALIEXPRESS_EXCEL_HEADS_NEW:
                head_dict[v] = k

        for row in range(nrows):
            row += 1
            if row == nrows:
                break
            product_id = str(int(sheet_obj.cell_value(row, head_dict[u'产品ID'])))
            if product_id == '0':
                datasource = str(sheet_obj.cell_value(row, head_dict[u'来源']))
                product_id = datasource.split('/')[-1].split('.')[0]
            title = str(sheet_obj.cell_value(row, head_dict[u'标题']))
            price = str(sheet_obj.cell_value(row, head_dict[u'售价(US $)']))
            # weight = str(sheet_obj.cell_value(row, head_dict[u'产品包装后的重量']))
            try:
                quantity = int(sheet_obj.cell_value(row, head_dict[u'库存']))
            except Exception as e:
                print 'Get Aliexpress product quantity error: %s' % e
                quantity = 0
            pic_url = str(sheet_obj.cell_value(row, head_dict[u'图片路径']))
            image = None
            if pic_url:
                image_url = pic_url.split(',')[0]
                if image_url.startswith('http'):
                    image = image_url
                else:
                    pass
            try:
                shopskus_info = str(sheet_obj.cell_value(row, head_dict[u'商家编码']))
                shopskus_info = shopskus_info.split(';')
            except Exception as e:
                print 'Get shopskus price error %s' % e
                continue
            shopskus = list()
            sku_list = list()
            mainsku_list = list()
            weight_list = list()
            for shopsku in shopskus_info:
                shop_sku = shopsku
                sku = classshopsku_obj.getSKU(shop_sku)
                mainsku = classsku_obj.get_bemainsku_by_sku(sku)
                weight = classsku_obj.get_weight_by_sku(sku)
                ali_detail_info = dict()
                ali_detail_info['product_id'] = product_id
                ali_detail_info['sku'] = sku
                ali_detail_info['mainsku'] = mainsku
                ali_detail_info['shop_sku'] = shop_sku
                ali_detail_info['status'] = flag
                if weight:
                    ali_detail_info['weight'] = float(weight)
                else:
                    ali_detail_info['weight'] = None
                shopskus.append(shop_sku)
                print 'ali_detail_info', ali_detail_info
                update_aliexpress_info_detail(**ali_detail_info)
                if sku:
                    sku_list.append(sku)
                if mainsku and mainsku not in mainsku_list:
                    mainsku_list.append(mainsku)
                if weight:
                    weight_list.append(float(weight))
                if not image:
                    bmpurl = get_image_by_sku(sku, db_conn)
                    if bmpurl:
                        image = bmpurl
                print 'image', image

            mainsku_list_str = None
            sku_list_str = None
            max_weight = None
            if mainsku_list:
                mainsku_list_str = ','.join(mainsku_list)
            if sku_list:
                sku_list_str = ','.join(sku_list)
            if weight_list:
                weight_list.sort()
                max_weight = weight_list[0]

            profitrate = get_aliexpress_profitrate(price, sku)

            ali_info = dict()
            ali_info['product_id'] = product_id
            ali_info['title'] = title
            ali_info['price'] = price
            ali_info['shopskus'] = ','.join(shopskus)
            ali_info['quantity'] = quantity
            ali_info['mainsku_list_str'] = mainsku_list_str
            ali_info['sku_list_str'] = sku_list_str
            if flag == 'True':
                ali_info['status'] = '1'
            else:
                ali_info['status'] = '0'
            ali_info['shopname'] = shopname
            ali_info['image'] = image
            ali_info['weight'] = max_weight
            ali_info['profitRate'] = profitrate
            update_aliexpress_info(**ali_info)
    except Exception as e:
        return {'code': '-1', 'message': '%s' % str(e)}
    return {'code': '0', 'message': 'SUCCESS'}


def update_aliexpress_info_detail(**kw):
    try:
        aliexpress_info_obj = t_aliexpress_online_info_detail.objects.get(ProductID=kw['product_id'], ShopSKU=kw['shop_sku'])
        aliexpress_info_obj.SKU = kw['sku']
        aliexpress_info_obj.MainSKU = kw['mainsku']
        aliexpress_info_obj.Status = kw['status']
        aliexpress_info_obj.Weight = kw['weight']
        aliexpress_info_obj.save()
    except t_aliexpress_online_info_detail.DoesNotExist:
        aliexpress_info_obj = t_aliexpress_online_info_detail(
            ProductID=kw['product_id'],
            SKU=kw['sku'],
            MainSKU=kw['mainsku'],
            ShopSKU=kw['shop_sku'],
            Status=kw['status'],
            Weight=kw['weight']
        )
        aliexpress_info_obj.save()


def update_aliexpress_info(**kw):
    try:
        aliexpress_obj = t_aliexpress_online_info.objects.get(ProductID=kw['product_id'])
        aliexpress_obj.SKU = kw['sku_list_str']
        aliexpress_obj.MainSKU = kw['mainsku_list_str']
        aliexpress_obj.Title = kw['title']
        aliexpress_obj.Price = kw['price']
        aliexpress_obj.ShopSKU = kw['shopskus']
        aliexpress_obj.Quantity = kw['quantity']
        aliexpress_obj.Status = kw['status']
        aliexpress_obj.Image = kw['image']
        aliexpress_obj.ShopName = kw['shopname']
        aliexpress_obj.Weight = kw['weight']
        aliexpress_obj.ProfitRate = kw['profitRate']
        aliexpress_obj.save()
    except t_aliexpress_online_info.DoesNotExist:
        aliexpress_obj = t_aliexpress_online_info(
            ProductID=kw['product_id'],
            SKU=kw['sku_list_str'],
            MainSKU=kw['mainsku_list_str'],
            Title=kw['title'],
            Price=kw['price'],
            ShopSKU=kw['shopskus'],
            Quantity=kw['quantity'],
            Status=kw['status'],
            Image=kw['image'],
            ShopName=kw['shopname'],
            Weight=kw['weight'],
            ProfitRate=kw['profitRate']
        )
        aliexpress_obj.save()


def get_image_by_sku(sku, db_conn):
    sql = "SELECT Bmpurl FROM py_db.b_goods WHERE SKU='%s';" % sku
    res = execute_db(sql, db_conn, 'select')
    if res:
        image = res[0]['Bmpurl']
    else:
        image = None
    return image


def get_aliexpress_profitrate(price, sku):
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
    ali_objs = t_aliexpress_online_info.objects.filter(ProfitRate__isnull=True, Status='1').values('id', 'Price', 'SKU')[0:1000]
    for obj in ali_objs:
        price = obj['Price']
        if not price:
            continue
        if price.find('-') != -1:
            price.replace('-', '~')
        if not obj['SKU']:
            continue
        sku = obj['SKU'].split(',')[0]
        profitrate = get_aliexpress_profitrate(price, sku)
        ali_pro_obj = t_aliexpress_online_info.objects.get(pk=obj['id'])
        ali_pro_obj.ProfitRate = profitrate
        ali_pro_obj.save()
    end_time = datetime.datetime.now()
    print 'end_time: ', end_time
    time_range = end_time - start_time
    print 'time_range: ', time_range
