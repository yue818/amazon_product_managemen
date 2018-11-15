#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-04-28 8:45
# @Author  : chenchen
# @Site    : 
# @File    : test2.py
# @Software: PyCharm


# -*- coding:utf-8 -*-

import MySQLdb.cursors
import sys
import bs4
from bs4 import BeautifulSoup
import os, errno, base64, datetime, time, hashlib, hmac, binascii, traceback
import urllib2, urllib, httplib
import datetime
from brick.pricelist.calculate_price import calculate_price

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)
# cursorclass=MySQLdb.cursors.SSCursor
from django.db import connection as conn
cur = conn.cursor()
sql = 'SELECT SKU,sellprice_us FROM a_test2'

print ('连接阿里云数据成功！')
cur.execute(sql)
rows = cur.fetchall()
for row in rows:
    calculate_price_obj = calculate_price(str(row[0]))
    try:
        Profit_info = calculate_price_obj.calculate_profitRate(str(row[1]), platformCountryCode='AMAZON-IN-FBA',
                                                                   DestinationCountryCode='IN')
        profitRate = str(Profit_info['profitRate'])
        price_extra_fba = str(Profit_info['price_extra_fba'])
        price_extra_js = str(Profit_info['price_extra_js'])
        price_extra_bcd = str(Profit_info['price_extra_bcd'])
        price_extra_gst = str(Profit_info['price_extra_gst'])
        price_extra_yj = str(Profit_info['price_extra_yj'])
        price_extra_qg = str(Profit_info['price_extra_qg'])
        price_extra_all = str(Profit_info['price_extra_all'])
        Money = str(Profit_info['Money'])
        price_yf = str(Profit_info['price_yf'])
        sum_money = str(Profit_info['sum_money'])
    except:
        profitRate = ''

    sql2 = "update a_test2 set Profit = '%s',fba='%s',js='%s',bcd='%s',gst='%s',yj='%s',qg='%s',money='%s',yf='%s',`all`='%s' where SKU = '%s'" % (profitRate,price_extra_fba,price_extra_js,price_extra_bcd,price_extra_gst,price_extra_yj,price_extra_qg,Money,price_yf,sum_money,str(row[0]))
    print sql2
    cur.execute(sql2)
    cur.execute("commit;")

cur.close()
conn.close()
