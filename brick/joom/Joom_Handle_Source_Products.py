#!/usr/bin/python
# -*- coding: utf-8 -*-

from brick.db.dbconnect import run
from brick.table.t_joom_source_products import t_joom_source_products
from brick.table.t_online_info_joom_detail import t_online_info_joom_detail
from django_redis import get_redis_connection
import datetime


def Joom_Handle_Source_Products():
    start_time = datetime.datetime.now()
    db_res = run({})
    if db_res['errorcode'] == -1:
        print "result['errortext']: %s" % db_res['errortext']
        return

    t_joom_source_products_obj = t_joom_source_products(db_res['db_conn'])
    while True:
        res = t_joom_source_products_obj.get_all_source_products()
        if not res:
            break
        else:
            for i in res:
                source_id = i['id']
                ShopName = i['ShopName']
                products_info = eval(i['ProductsInfo'])
                t_online_info_joom_detail_obj = t_online_info_joom_detail(ShopName, db_res['db_conn'], redis_conn=get_redis_connection(alias='product'))
                refreshdict = t_online_info_joom_detail_obj.insertJoomV2([products_info])
                print 'refreshdict: %s' % refreshdict
                t_joom_source_products_obj.set_hanle_over(source_id)
                # break
            break
            t_joom_source_products_obj.delete_info()
            continue
    end_time = datetime.datetime.now()
    handle_time = end_time - start_time
    print 'handle_time: %s' % handle_time.total_seconds()
