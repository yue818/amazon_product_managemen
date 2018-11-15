#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from brick.db.dbconnect import run
# from brick.db.dbconnect import execute_db
from brick.classredis.classsku import classsku
from skuapp.table.t_online_info_amazon_listing import t_online_info_amazon_listing
# from brick.pydata.py_redis.py_SynRedis_tables import connRedis
classsku1_obj = classsku()


def amazon_update_seven_orders():
    start = datetime.datetime.now()
    print 'start', start
    db_res = run({})
    if db_res['errorcode'] == -1:
        print "result['errortext']: %s" % db_res['errortext']
        return

    pro_shop_sku = t_online_info_amazon_listing.objects.filter(Status='Active').values('product_id', 'seller_sku')
    cursor = db_res['db_conn'].cursor()

    # CLear SevenOrders
    clear_sql = "UPDATE t_online_info_amazon_listing SET order7days=NULL"
    cursor.execute(clear_sql)
    cursor.execute("commit;")

    for ss in pro_shop_sku:
        shopskus = list()
        shopsku = ss['seller_sku']
        if shopsku.find('*'):
            shopsku = shopsku.split('*')[0]
            shopskus.append(shopsku)
        elif shopsku.find('+'):
            shopsku = shopsku.split('+')
            shopskus += shopsku
        else:
            shopskus.append(shopsku)
        product_id = ss['product_id']
        for i in shopskus:
            sevenorders = 0
            num = classsku1_obj.get_shopsevensale_by_sku(shopsku)
            update_time = classsku1_obj.get_updatetime_by_sku(shopsku)
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
        sql_orders = "UPDATE t_online_info_amazon_listing SET order7days=%s WHERE product_id='%s';" % (sevenorders, product_id)
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
