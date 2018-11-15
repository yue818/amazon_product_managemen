# -*- coding:utf-8 -*-

"""
 @desc:
 @author: wuchongxiang
 @site:
 @software: PyCharm
 @file: 20181026.py
 @time: 2018/10/26 14:02
"""
import pymysql
import datetime

# DATABASE = {
#     'ENGINE': 'django.db.backends.mysql',
#     'NAME': 'hq_db',
#     'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
#     'PORT': '3306',
#     'USER': 'by15161458383',
#     'PASSWORD': 'K120Esc1'
# }

# try:
#     db_conn = pymysql.connect(DATABASE['HOST'],
#                               DATABASE['USER'],
#                               DATABASE['PASSWORD'],
#                               DATABASE['NAME'],
#                               charset='utf8')
#
#     param_list = list()
#     with open('D:\\1.txt', 'r') as f:
#         for line in f.readlines():
#             line_list = line.strip('\n').split('||')
#             param_list.append(line_list)
#
#     # print param_list
#
#     cursor = db_conn.cursor()
#
#     sql = "insert into temp_20181026 (shop_name, seller_sku, posted_date, amazon_order_id, finance_type) values ( %s, %s, %s, %s, %s)"
#     print datetime.datetime.now()
#     cursor.executemany(sql, param_list)
#     print datetime.datetime.now()
#     db_conn.commit()
# except Exception as ex:
#     print ex
#     db_conn.close()

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


def insert_finance_record_file(file_name):
    finance_param_list = list()
    with open(file_name, 'r') as f_r:
        for line in f_r.readlines():
            line_list = line.strip('\n').split('||')
            finance_param_list.append(line_list)

    sql_insert = '''insert into t_amazon_finance_record
                   (posted_date, amazon_order_id, marketplace_name, seller_sku, quantity_shipped, order_adjustment_item_id, fee_type, fee_currency, fee_amount,order_item_id, finance_type, shop_name, refresh_time)
                   values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                   '''
    cursor_many = db_conn.cursor()
    cursor_many.executemany(sql_insert, finance_param_list)
    db_conn.commit()
    cursor_many.close()


insert_finance_record_file('C:\\fba_server\\finance_record_20180206T231424_20180308_20181026170307.log')