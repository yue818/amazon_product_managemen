#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from brick.db.dbconnect import run
from brick.db.dbconnect import execute_db
from brick.classredis.classsku import classsku
from joom_app.table.t_online_info_joom import t_online_info_joom
classsku1_obj = classsku()


def joom_update_seven_orders():
    start = datetime.datetime.now()
    print 'start', start
    db_res = run({})
    if db_res['errorcode'] == -1:
        print "result['errortext']: %s" % db_res['errortext']
        return

    pro_shop_sku = t_online_info_joom.objects.filter(Status='1', ReviewState='0').values('ProductID', 'ShopSKU', 'ShopName')
    cursor = db_res['db_conn'].cursor()

    # CLear SevenOrders
    clear_sql = "UPDATE t_online_info_joom SET Orders7Days=NULL"
    cursor.execute(clear_sql)
    cursor.execute("commit;")
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
                num = classsku1_obj.get_shopsevensale_by_sku(shopsku)
                update_time = classsku1_obj.get_SevenSales_UpdateTime_by_shopsku(shopsku)
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
            sql_orders = "UPDATE t_online_info_joom SET Orders7Days=%s WHERE ProductID='%s';" % (sevenorders, product_id)
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


def update_joom_product_sku_and_mainsku():
    from brick.classredis.classsku import classsku
    from brick.classredis.classshopsku import classshopsku
    from django_redis import get_redis_connection

    start = datetime.datetime.now()
    print 'start', start

    db_res = run({})
    if db_res['errorcode'] == -1:
        print "result['errortext']: %s" % db_res['errortext']
        return
    db_conn = db_res['db_conn']
    redis_conn = get_redis_connection(alias='product')

    classsku_obj = classsku(db_cnxn=db_conn, redis_cnxn=redis_conn)
    classshopsku_obj = classshopsku(db_conn=db_conn, redis_conn=redis_conn)

    # joom_pros = t_online_info_joom.objects.filter(Status='True', ReviewState='approved').values('ProductID', 'ShopSKU', 'ShopName')
    joom_pros = t_online_info_joom.objects.filter(Status='1', ReviewState='0').values('ProductID', 'ShopSKU', 'ShopName')

    curs = db_conn.cursor()

    no_mainsku_pro_list = list()

    for pro in joom_pros:
        # print pro
        shopsku_list = pro['ShopSKU'].split(',')
        product_id = pro['ProductID']
        shopname = pro['ShopName']
        sku_list = list()
        mainsku_list = list()

        for shopsku in shopsku_list:
            sku = classshopsku_obj.getSKU(shopsku)
            # print sku
            mainsku = classsku_obj.get_bemainsku_by_sku(sku)
            # print mainsku
            if sku:
                sku_list.append(sku)
            if mainsku and mainsku not in mainsku_list:
                mainsku_list.append(mainsku)
            sql_detail = "UPDATE t_online_info_joom_detail SET SKU=%s, MainSKU=%s WHERE ProductID=%s AND ShopSKU=%s;"
            curs.execute(sql_detail, (sku, mainsku, product_id, shopsku))

        skus = None
        if sku_list:
            skus = ','.join(sku_list)
        mainskus = None
        if mainsku_list:
            mainskus = ','.join(mainsku_list)

        if not sku_list or not mainsku_list:
            # print 'product_id', product_id
            # print 'shopsku_list', shopsku_list
            a_on_info = dict()
            a_on_info['shopname'] = shopname
            a_on_info['product_id'] = product_id
            a_on_info['shopsku_list'] = shopsku_list
            no_mainsku_pro_list.append(a_on_info)
        sql_joom = "UPDATE t_online_info_joom SET SKU=%s, MainSKU=%s WHERE ProductID=%s;"
        curs.execute(sql_joom, (skus, mainskus, product_id))
    # print 'no_mainsku_pro_list num', len(no_mainsku_pro_list)
    print 'no_mainsku_pro_list', no_mainsku_pro_list
    curs.execute('commit;')
    curs.close()

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

    re_set_status_sql = "UPDATE t_online_info_joom SET CanPriceParity=NULL;"

    set_status_sql = "UPDATE t_online_info_joom SET CanPriceParity=1 WHERE id IN (SELECT q.id FROM ( " \
                     "SELECT MAX(a.id) AS id FROM t_online_info_joom a, (SELECT MAX(b.Orders7Days) AS maxorder7days, " \
                     "b.MainSKU FROM t_online_info_joom AS b WHERE b.MainSKU IS NOT NULL AND b.MainSKU<>'' AND " \
                     "b.`Status`='1' AND b.ReviewState='0' AND b.cutprice_flag<>1 GROUP BY b.MainSKU) c WHERE " \
                     "a.MainSKU=c.MainSKU AND a.Orders7Days=c.maxorder7days GROUP BY a.MainSKU) q);"

    # re_set_status_sql = "UPDATE t_online_info_joom_test_sj SET CanPriceParity=NULL;"

    # set_status_sql = "UPDATE t_online_info_joom_test_sj SET CanPriceParity=1 WHERE id IN (SELECT q.id FROM ( " \
    #                  "SELECT MAX(a.id) AS id FROM t_online_info_joom_test_sj a, (SELECT MAX(b.Orders7Days) AS maxorder7days, " \
    #                  "b.MainSKU FROM t_online_info_joom_test_sj AS b WHERE b.MainSKU IS NOT NULL AND b.MainSKU<>'' AND " \
    #                  "b.`Status`='1' AND b.ReviewState='0' AND b.cutprice_flag<>1 GROUP BY b.MainSKU) c WHERE " \
    #                  "a.MainSKU=c.MainSKU AND a.Orders7Days=c.maxorder7days GROUP BY a.MainSKU) q);"

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
