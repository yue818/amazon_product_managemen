#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from django.db import connection
from brick.classredis.classsku import classsku
from ebayapp.table.t_online_info_ebay_listing import t_online_info_ebay_listing
from skuapp.table.t_online_info_ebay_subsku import t_online_info_ebay_subsku
from skuapp.table.t_config_store_ebay import t_config_store_ebay

classsku_obj = classsku()


def get_ebay_shopname():
    shopname_list = t_config_store_ebay.objects.all().values('storeName', 'ShopName')
    shopname_dict = dict()
    for i in shopname_list:
        shopname_dict[i['storeName']] = i['ShopName']

    return shopname_dict


def ebayapp_update_seven_orders():
    start = datetime.datetime.now()
    print 'start', start

    cursor = connection.cursor()
    clear_sql = "UPDATE t_online_info_ebay SET Orders7Days=NULL"
    cursor.execute(clear_sql)
    cursor.execute("commit;")

    # shopname_dict = get_ebay_shopname()

    pro_shop_sku = t_online_info_ebay_listing.objects.filter(dostatus='doSuccess').values('itemid', 'SKU', 'ShopName')
    counts_num = len(pro_shop_sku) / 10000 + 1
    for count_num in range(counts_num):
        # if count_num == 1:
        #     break
        start_num = count_num * 10000
        end_num = (count_num + 1) * 10000
        for ss in pro_shop_sku[start_num:end_num]:
            itemid = ss['itemid']
            t_online_info_ebay_subsku_objs = t_online_info_ebay_subsku.objects.filter(itemid=itemid).values('subSKU')
            sevenorders = 0
            # shopname = shopname_dict[ss['ShopName']]
            shopname = ss['ShopName']
            if len(t_online_info_ebay_subsku_objs) > 0:
                for ebay_subsku in t_online_info_ebay_subsku_objs:
                    shopsku = shopname + '@#@' + ebay_subsku['subSKU']
                    num = classsku_obj.get_shopsevensale_by_sku(shopsku)
                    update_time = classsku_obj.get_SevenSales_UpdateTime_by_shopsku(shopsku)
                    if update_time:
                        update_time = update_time[:10]
                        today = datetime.date.today().strftime('%Y-%m-%d')
                        if today != update_time:
                            continue
                    else:
                        continue
                    if not num:
                        num = 0
                    sevenorders += int(num)
            else:
                shopsku = shopname + '@#@' + ss['SKU']
                num = classsku_obj.get_shopsevensale_by_sku(shopsku)
                update_time = classsku_obj.get_SevenSales_UpdateTime_by_shopsku(shopsku)
                if update_time:
                    update_time = update_time[:10]
                    today = datetime.date.today().strftime('%Y-%m-%d')
                    if today != update_time:
                        continue
                else:
                    continue
                if not num:
                    num = 0
                sevenorders = num

            print 'itemid: %s, sevenorders: %s' % (itemid, sevenorders)
            sql_orders = "UPDATE t_online_info_ebay SET Orders7Days=%s WHERE itemid=%s;"
            res = dict()
            res['code'] = 0
            try:
                cursor.execute(sql_orders, (sevenorders, itemid,))
            except Exception as e:
                res['code'] = -1
                print 'error', e
            if res['code'] == 0:
                pass
            else:
                print res
                print 'itemid', itemid
        cursor.execute("commit;")
        print 'handle num range: %s ~ %s' % (start_num, end_num)
    cursor.close()

    end = datetime.datetime.now()
    print 'end', end
    how_long = end - start
    print 'how_long', how_long
