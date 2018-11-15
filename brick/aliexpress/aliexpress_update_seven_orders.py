#!/usr/bin/python
# -*- coding: utf-8 -*-

from brick.db.dbconnect import run
from brick.db.dbconnect import execute_db
# from brick.pydata.py_redis.py_SynRedis_tables import connRedis
from aliexpress_app.table.t_aliexpress_online_info import t_aliexpress_online_info
import datetime
from brick.classredis.classsku import classsku
classsku_obj = classsku()


def aliexpress_update_seven_orders():
    start = datetime.datetime.now()
    print 'start', start
    db_res = run({})
    if db_res['errorcode'] == -1:
        print "result['errortext']: %s" % db_res['errortext']
        return

    pro_shop_sku = t_aliexpress_online_info.objects.filter(Status='1').values('ProductID', 'ShopSKU', 'ShopName')
    cursor = db_res['db_conn'].cursor()
    counts_num = len(pro_shop_sku) / 10000 + 1
    for count_num in range(counts_num):
        # if count_num == 1:
        #     break
        start_num = count_num * 10000
        end_num = (count_num + 1) * 10000
        for ss in pro_shop_sku[start_num:end_num]:
            shopskus = ss['ShopSKU'].split(',')
            product_id = ss['ProductID']
            sevenorders = 0
            shopname = ss['ShopName']
            for i in shopskus:
                shopsku = shopname + '@#@' + i
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

            print 'product_id: %s, sevenorders: %s' % (product_id, sevenorders)
            sql_orders = "UPDATE t_aliexpress_online_info SET Orders7Days=%s WHERE ProductID='%s';" % (sevenorders, product_id)
            res = dict()
            res['code'] = 0
            try:
                cursor.execute(sql_orders)
            except Exception as e:
                res['code'] = -1
                print 'error', e
            if res['code'] == 0:
                pass
            else:
                print res
                print 'product_id', product_id
        cursor.execute("commit;")
        print 'handle num range: %s ~ %s' % (start_num, end_num)
    cursor.close()

    end = datetime.datetime.now()
    print 'end', end
    how_long = end - start
    print 'how_long', how_long


def aliexpress_update_seven_orders_by_shopname(shopname):
    start = datetime.datetime.now()
    print 'start', start
    db_res = run({})
    if db_res['errorcode'] == -1:
        print "result['errortext']: %s" % db_res['errortext']
        return

    pro_shop_sku = t_aliexpress_online_info.objects.filter(Status='1', ShopName=shopname).values('ProductID', 'ShopSKU', 'ShopName')
    cursor = db_res['db_conn'].cursor()
    for ss in pro_shop_sku:
        shopskus = ss['ShopSKU'].split(',')
        product_id = ss['ProductID']
        sevenorders = 0
        shopname = ss['ShopName']
        for i in shopskus:
            shopsku = shopname + '@#@' + i
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

        print 'product_id: %s, sevenorders: %s' % (product_id, sevenorders)
        sql_orders = "UPDATE t_aliexpress_online_info SET Orders7Days=%s WHERE ProductID='%s';" % (sevenorders, product_id)
        res = dict()
        res['code'] = 0
        try:
            cursor.execute(sql_orders)
        except Exception as e:
            res['code'] = -1
            print 'error', e
        if res['code'] == 0:
            pass
        else:
            print res
            print 'product_id', product_id
    cursor.execute("commit;")
    cursor.close()

    end = datetime.datetime.now()
    print 'end', end
    how_long = end - start
    print 'how_long', how_long


def update_can_price_parity_status():
    sRes = {'code': 0, 'message': ''}
    db_res = run({})
    if db_res['errorcode'] == -1:
        print "result['errortext']: %s" % db_res['errortext']
        sRes['code'] = db_res['errorcode']
        sRes['message'] = db_res['errortext']
        return sRes

    re_set_status_sql = "UPDATE t_aliexpress_online_info SET CanPriceParity=NULL;"
    # re_set_status_sql = "UPDATE t_aliexpress_online_info_test0512 SET CanPriceParity=NULL;"

    set_status_sql = "UPDATE t_aliexpress_online_info SET CanPriceParity=1 WHERE id IN (SELECT q.id FROM ( " \
                     "SELECT MAX(id) AS id FROM t_aliexpress_online_info WHERE CONCAT(Orders7Days,MainSKU) IN " \
                     "(SELECT CONCAT(MAX(Orders7Days),MainSKU) FROM t_aliexpress_online_info WHERE Status='1' " \
                     "GROUP BY MainSKU ) GROUP BY MainSKU) q);"
    # set_status_sql = "UPDATE t_aliexpress_online_info_test0512 SET CanPriceParity=1 WHERE id IN (SELECT q.id FROM ( " \
    #                  "SELECT MAX(id) AS id FROM t_aliexpress_online_info_test0512 WHERE CONCAT(Orders7Days,MainSKU) IN " \
    #                  "(SELECT CONCAT(MAX(Orders7Days),MainSKU) FROM t_aliexpress_online_info_test0512 WHERE Status='1' " \
    #                  "GROUP BY MainSKU ) GROUP BY MainSKU) q);"

    try:
        reset_infos = execute_db(re_set_status_sql, db_res['db_conn'], 'update')
        set_infos = execute_db(set_status_sql, db_res['db_conn'], 'update')
        if reset_infos['code'] != 0:
            sRes['code'] = reset_infos['code']
            sRes['message'] += 'reset CanPriceParity all null error: ' + reset_infos['message']
        if set_infos['code'] != 0:
            sRes['code'] = set_infos['code']
            sRes['message'] += 'set CanPriceParity 1 error: ' + set_infos['message']
    except Exception as e:
        sRes['code'] = -1
        sRes['message'] = str(e)

    return sRes
