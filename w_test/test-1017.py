# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: test-1017.py
 @time: 2018/10/17 8:52
"""
import datetime
import pymysql


def get_last_order_time(db_conn, ShopName):
    cursor = db_conn.cursor()
    sql_max_time = "select min(purchase_date), max(purchase_date) from t_amazon_all_orders_data where shop_name = '%s' and order_status = 'Pending' " % (ShopName)
    print 'sql_max_time is: %s' % sql_max_time
    cursor.execute(sql_max_time)
    max_time_obj = cursor.fetchone()
    cursor.close()

    if max_time_obj is None or len(max_time_obj) == 0 or max_time_obj[0] is None:
        print '11'
        cursor = db_conn.cursor()
        sql_max_time_all = "select max(purchase_date) from t_amazon_all_orders_data where shop_name = '%s'" % (ShopName)
        print 'sql_max_time_all is: %s' % sql_max_time_all
        cursor.execute(sql_max_time_all)
        max_time_all_obj = cursor.fetchone()
        cursor.close()
        if max_time_all_obj is None or len(max_time_all_obj) == 0 or max_time_all_obj[0] is None:
            print '22'

            max_update_time = datetime.datetime.strptime('2018-01-01', '%Y-%m-%d')
        else:
            print '33'
            max_update_time = max_time_all_obj[0]
    else:
        print '44'
        max_update_time = max_time_obj[0] + datetime.timedelta(days=-1)
        if max_time_obj[1].strftime('%Y-%m-%d') == '9999-12-31':  # 人工设置需全量刷新的标志日期 9999-12-31
            max_update_time = datetime.datetime.strptime('2018-01-01', '%Y-%m-%d')

    print max_update_time
    last_order_time = list()
    if max_update_time < datetime.datetime.now() + datetime.timedelta(days=-30):
        last_order_time.append(max_update_time.strftime('%Y-%m-%d'))
        for i in range(1, 10):
            time_30_days_later = max_update_time + datetime.timedelta(days=30 * i)
            if time_30_days_later < datetime.datetime.now():
                last_order_time.append(time_30_days_later.strftime('%Y-%m-%d'))
            else:
                last_order_time.append(datetime.datetime.now().strftime('%Y-%m-%d'))
                break
    else:
        time_29_days_before = datetime.datetime.now() + datetime.timedelta(days=-29)
        last_order_time.append(time_29_days_before.strftime('%Y-%m-%d'))
        time_this_day_end = datetime.datetime.now() + datetime.timedelta(days=1)
        last_order_time.append(time_this_day_end.strftime('%Y-%m-%d'))
    print 'last_order_time is :'
    print last_order_time
    return last_order_time


DATABASE = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'hq_db',
    'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
    'PORT': '3306',
    'USER': 'by15161458383',
    'PASSWORD': 'K120Esc1'
}

db_conn = pymysql.connect(DATABASE['HOST'],
                                       DATABASE['USER'],
                                       DATABASE['PASSWORD'],
                                       DATABASE['NAME'],
                                       charset='utf8')

# get_last_order_time(db_conn, 'AMZ-0229-XL-UK/HF')
get_last_order_time(db_conn, 'AMZ-0192-XD-AU/HF')

