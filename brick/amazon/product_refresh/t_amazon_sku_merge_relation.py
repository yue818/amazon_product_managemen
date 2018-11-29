# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_sku_merge_relation.py
 @time: 2018/11/22 10:38
"""  
import pymysql


DATABASES = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hq_db',
        'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
        'PORT': '3306',
        'USER': 'by15161458383',
        'PASSWORD': 'K120Esc1'
            }

db_conn = pymysql.connect(DATABASES['HOST'],
                          DATABASES['USER'],
                          DATABASES['PASSWORD'],
                          DATABASES['NAME'],
                          charset='utf8')
try:
    sql = "select id, details from t_product_information_modify where `select`=7 and Mstatus='WCXG' and details is not null"
    with db_conn.cursor() as cursor:
        cursor.execute(sql)
        print cursor.rowcount
        if cursor.rowcount > 0:
            records = cursor.fetchall()
        else:
            records = None

    sku_modify_list = list()
    if records:
        sku_modify_list.extend([(record[0], sku_pair['delete_sku'], sku_pair['retain_sku']) for record in records for sku_pair in eval(record[1])])
    print sku_modify_list

    sql_delete = 'truncate table t_amazon_sku_merge'
    sql_insert = '''insert into t_amazon_sku_merge(merge_id, old_sku, new_sku) values (%s, %s, %s)'''
    with db_conn.cursor() as cursor:
        cursor.execute(sql_delete)
        cursor.executemany(sql_insert, sku_modify_list)
        db_conn.commit()
    db_conn.close()
except Exception as ex:
    print ex
    db_conn.close()



