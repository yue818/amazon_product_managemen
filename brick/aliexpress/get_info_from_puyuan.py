# -*- coding: utf-8 -*-
import MySQLdb
def get_connections():
    from django.db import connection
    # return MySQLdb.connect('192.168.105.111', 'root', 'root123', 'hq')
    return  connection

def get_ShopSKU_by_id(id):
    conn = get_connections()
    cur = conn.cursor()
    cur.execute('select ShopSKU from t_report_sales_weekly where ProductID = %s',(id,))
    skurows = cur.fetchall()
    cur.close()
    conn.close()
    if len(skurows)>=1:
        return skurows[0][0]
    return 0

def get_MainSKU_by_id(id):
    conn = get_connections()
    cur = conn.cursor()
    cur.execute('select MainSKU from t_report_sales_weekly where ProductID = %s',(id,))
    skurows = cur.fetchall()
    cur.close()
    conn.close()
    if len(skurows)>=1:
        return skurows[0][0]
    return 0

def get_SKU_by_id(id):
    conn = get_connections()
    cur = conn.cursor()
    cur.execute('select SKU from t_report_sales_weekly where ProductID = %s',(id,))
    skurows = cur.fetchall()
    cur.close()
    conn.close()
    if len(skurows)>=1:
        return skurows[0][0]
    return 0

def get_salesCount_by_mainsku(sku):
    try:
        sum = 0
        conn = get_connections()
        cur = conn.cursor()
        cur.execute('select SalesVolume from t_report_sales_weekly where MainSKU = %s', (sku,))
        SalesVolumes = cur.fetchall()
        for SalesVolume in SalesVolumes:
            sum+=SalesVolume[0]
        cur.close()
        conn.close()
        return sum
    except:
        return 0

def get_weekCount_by_mainsku(sku):
    try:
        sum = 0
        conn = get_connections()
        cur = conn.cursor()
        cur.execute('select WeekNO from t_report_sales_weekly where MainSKU = %s ORDER BY WeekNO Desc', (sku,))
        WeekNOs = cur.fetchall()
        if len(WeekNOs)>=1:
            lastWeekNOs = WeekNOs[0][0]
        else:
            cur.execute('select WeekNO from t_report_sales_weekly ORDER BY WeekNO Desc')
            WeekNOs = cur.fetchall()
            lastWeekNOs = WeekNOs[0][0]
        cur.execute('select SalesVolume from t_report_sales_weekly where MainSKU = %s and WeekNO = %s', (sku,lastWeekNOs))
        SalesVolumes = cur.fetchall()
        for SalesVolume in SalesVolumes:
            sum += SalesVolume[0]
        cur.close()
        conn.close()
        return sum
    except:
        return 0

def get_price_by_shopsku(shopsku):
    from django.db import connection
    from django_redis import get_redis_connection
    from brick.pydata.py_redis.py_SynRedis_pub import connRedis
    from ..classredis.classshopsku import classshopsku
    # redis_conn = get_redis_connection(alias='product')
    redis_conn = connRedis
    classsku_obj = classshopsku(connection, redis_conn)
    return classsku_obj.getPrice(shopsku)

def get_price_by_sku(sku):
    from django.db import connection
    #from django_redis import get_redis_connection
    # redis_conn = get_redis_connection(alias='product')
    from ..classredis.classsku import classsku
    from brick.pydata.py_redis.py_SynRedis_pub import connRedis
    redis_conn = connRedis
    classsku_obj = classsku(connection, redis_conn)
    return classsku_obj.get_price_by_sku(sku)

def get_price_from_redis_by_sku(sku):
    from brick.pydata.py_redis.py_SynRedis_pub import connRedis
    # from django_redis import get_redis_connection
    # redis_conn = get_redis_connection(alias='product')
    return connRedis.hget(sku, 'Price')
    # return redis_conn.gethash(sku, 'Price')

def get_price_by_productid_from_puyuan(id):
    import pymssql
    conn = pymssql.connect(host='122.226.216.10:18793', user='fancyqube', password='K120Esc1', database='ShopElf')
    cur = conn.cursor()
    cur.execute('SELECT productMinPrice,productMaxPrice,productPrice FROM L_AliStoreGoods WHERE productId = %d', (id,))
    try:
        prices = cur.fetchall()
        cur.close()
        conn.close()
        return prices[0][0], prices[0][1], prices[0][2]
    except:
        return 0,0,0

def get_sqleifo_from_db(id):
    mainsku = get_MainSKU_by_id(id)
    shopsku = get_ShopSKU_by_id(id)
    SKU = get_ShopSKU_by_id(id)
    salesCount = get_salesCount_by_mainsku(mainsku)
    weekCount = get_weekCount_by_mainsku(mainsku)
    # miniprice, maxprice, price = get_price_by_productid_from_puyuan(id)
    price = get_price_by_sku(SKU)
    # price = get_price_from_redis_by_sku(SKU)
    if mainsku==0:
        return 0,0,0,0,price    #str(miniprice)+'-'+str(maxprice)
    return mainsku ,shopsku ,salesCount ,weekCount ,price   #str(miniprice)+'-'+str(maxprice)

if __name__ == '__main__':
    print(get_sqleifo_from_db('32843312399'))