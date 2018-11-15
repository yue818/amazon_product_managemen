#!/usr/bin/python
# -*- coding: utf-8 -*-

from brick.db.dbconnect import run
from brick.joom.Joom_Change_Product_Price_Client import Joom_Change_Product_Price_Client
from brick.table.t_joom_cutprice_log import t_joom_cutprice_log
from brick.table.t_online_info_joom import t_online_info_joom


def Joom_Recover_Monitor():
    print ' [x] Start to search cutprice products'
    db_res = run({})
    if db_res['errorcode'] == -1:
        print "result['errortext']: %s" % db_res['errortext']
        return
    joom_cutprice_log = t_joom_cutprice_log(db_conn=db_res['db_conn'])
    products = joom_cutprice_log.get_cutpricing_products()
    # print 'type(products)', type(products)
    # print 't_joom_cutprice_log: %s' % str(products)
    if not products:
        print '==========No Cut Price Product'
        return
    products_dict = dict()
    for i in products:
        products_dict[i['ProductID']] = i
    product_ids = products_dict.keys()
    if len(product_ids) > 1:
        product_id = '\'' + '\',\''.join(product_ids) + '\''
    elif len(product_ids) == 1:
        product_id = '\'' + product_ids[0] + '\''
    else:
        print '----------No Cut Price Product'
        return

    online_info_joom = t_online_info_joom(db_conn=db_res['db_conn'])
    joom_products_info = online_info_joom.get_joom_products_by_productids(product_ids=product_id)
    # print 't_online_info_joom: %s' % str(joom_products_info)
    for i in joom_products_info:
        products_dict[i['ProductID']]['nowOfSales'] = i['OfSales']

    for i in products_dict.keys():
        Threshold = int(products_dict[i]['Threshold'])
        oldsales = int(products_dict[i]['OfSales'])
        nowsales = int(products_dict[i]['nowOfSales'])
        if (nowsales - oldsales) >= Threshold:
            productid = i
            shopname = products_dict[i]['ShopName']
            # print 'productid', productid
            # print 'shopname', shopname
            status = 0
            sRes = online_info_joom.set_joom_products_cut_price_status(productid, status)
            print sRes
            send_res = Joom_Change_Product_Price_Client(shop_name=shopname, product_id=productid, cutprice_flag=1)
            print send_res
        else:
            continue

    print ' [x] End to search cutprice products'
