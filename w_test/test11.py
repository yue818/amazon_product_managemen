# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: test11.py
 @time: 2018-05-25 15:56
"""

import pymysql as MySQLdb
import datetime


DATABASES = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hq_db',
        'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
        'PORT': '3306',
        'USER': 'by15161458383',
        'PASSWORD': 'K120Esc1'
            }


def update_is_sure_feed(dealResult, UpdateTime, dealResultInfo, order_id):
    # cnxn = MySQLdb.connect(DATABASES['HOST'], DATABASES['USER'], DATABASES['PASSWORD'], DATABASES['NAME'], charset='utf8')
    # cursor = cnxn.cursor()
    sql = u"update t_order_amazon_india set is_sure_feed='%s',dealResult='%s', dealTime='%s', dealResultInfo='%s',OrderWarningDays=NULL,OrderWarningType=NULL where AmazonOrderId='%s' " % (
        '2', dealResult, UpdateTime, dealResultInfo, order_id)
    # if order_id not in ('406-6687759-8127537','408-8924150-3355554','408-2694514-2209142','405-8686328-8157163','404-3453703-9951563','403-8522419-4123552'):
    #     print  sql,';'
    print order_id, ','
    # cursor.execute(sql)
    # cursor.commit()
    # cursor.close()

Params = '[{"track_date": "2018-02-24T00:39:00Z", "track_company": "ECOM EXPRESS", "track_num": "238557232", "AmazonOrderId": "402-9419304-9860328", "shopName": "AMZ-0201-Cberty-IN/HF"}]'
rtdatas = eval(Params)
for rtdata in rtdatas:
    upTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_is_sure_feed('Complete', upTime, '', rtdata['AmazonOrderId'])