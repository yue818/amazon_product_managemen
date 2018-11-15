#!/usr/bin/python
# -*- coding: utf-8 -*-

from brick.classredis.classlisting import classlisting
from brick.wish.Haiying_Data.haiying_cfg import HYCONFIG
from haiying_data_in_db import haiying_data_in_db
from get_data_from_haiying import Haiying
import time
from app_djcelery.celery import app
from django.db import  connection
from django_redis import get_redis_connection
import datetime
#
# print redis_conn
# exit()
# import redis
# #这里替换为连接的实例host和port
# host = 'r-uf6206e9df36e854.redis.rds.aliyuncs.com'
# port = 6379
# #这里替换为实例password
# pwd = 'K120Esc1'
# redis_conn = redis.StrictRedis(host=host, port=port, password=pwd)
#
# from brick.db import dbconnect
# params ={}
# result = dbconnect.run(params)
# connection=result['db_conn']

@app.task
def get_data_from_haiying_task(pagnum):
    redis_conn = get_redis_connection(alias='product')
    classlisting_obj = classlisting(connection,redis_conn)
    hy_data_in_db_obj = haiying_data_in_db()
    hy = Haiying()
    try:
        cursor = connection.cursor()
        rt = None
        rt = hy.data(pagnum)
        if rt is None:
            cursor.close()
            return False;# 容错机制：海鹰返回错误时，本页数据忽略
        for obj in rt:
            if obj:
                if classlisting_obj.getvaluefromredis(obj['pid']) is not None:
                    continue
                else:
                    hy_data_in_db_obj.t_config_wishapi_product_analyse_info(obj, cursor)
                    classlisting_obj.setvaluefromredis(obj['pid'],HYCONFIG['hyflag'])
        print ('haiying data pagnum:%s success' % (pagnum))
        cursor.close()
    except Exception, ex:
        print '-------------%s:%s' % (Exception, ex)
        cursor.close()

@app.task
def get_data_from_haiying_original_trans(pagnum):
    hy_data_in_db_obj = haiying_data_in_db()
    hy = Haiying()
    try:
        rt = None
        for i in range(0, pagnum):
            try:
                cursor = connection.cursor()
                rt = hy.data(i)
                if rt is None:
                    cursor.close()
                    #return False;# 容错机制：海鹰返回错误时，本页数据忽略
                for obj in rt:
                    if obj:
                        hy_data_in_db_obj.t_config_wishapi_product_analyse_all_info(obj, cursor)
                cursor.close()
                print ('haiying data pagnum:%s success' % (i))
            except Exception, ex:
                print '-------------%s:%s' % (Exception, ex)
                cursor.close()
    except Exception, ex:
        print '-------------%s:%s' % (Exception, ex)
        cursor.close()
    time.sleep(20)
    try:
        cursor = connection.cursor()
        cursor1 = connection.cursor()
        hy_data_in_db_obj.t_config_wishapi_product_analyse_all_info_view_his_data(cursor,cursor1)
        cursor.close()
        cursor1.close()
    except Exception, ex:
        print '-------------%s:%s' % (Exception, ex)
        cursor.close()
        cursor1.close()
#get_data_from_haiying_task(connection,redis_conn,3)