#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import json, time
import pika
import sys, StringIO, csv
import requests, urllib2
import logging
import logging.handlers
import MySQLdb
import datetime
import traceback
import copy


# logging.basicConfig(level=logging.DEBUG,format='%(asctime)s [%(filename)s %(funcName)s:%(lineno)d] %(thread)d %(levelname)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S',filename='joom_get_product.log',filemode='a')
# logging.handlers.RotatingFileHandler('joom_get_product.log', maxBytes=100 * 1024 * 1024, backupCount=10)

log_formatter = logging.Formatter('%(asctime)s [%(filename)s %(funcName)s:%(lineno)d] %(thread)d %(levelname)s %(message)s')
logFile = 'Joom_Get_Now_Shop_Products.log'
my_handler = logging.handlers.RotatingFileHandler(
    logFile,
    mode='a',
    maxBytes=100*1024*1024,
    backupCount=4,
    encoding=None,
    delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.DEBUG)
logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)
logger.addHandler(my_handler)


# Real environment sql connection info
DATABASES = {
    'NAME': 'hq_db',
    'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
    'PORT': '3306',
    'USER': 'by15161458383',
    'PASSWORD': 'K120Esc1'
}


class Server():

    def __init__(self):
        self.realIP = self.get_out_ip(self.get_real_url())

    def listen_client(self):
        print " [x] Start to get shop products"
        db_conn = MySQLdb.connect(DATABASES['HOST'], DATABASES['USER'], DATABASES['PASSWORD'], DATABASES['NAME'], charset="utf8")
        shopname_list = self.get_shop_names(db_conn)
        shopnames_auth_info = list()
        for i in shopname_list:
            auth_info = self.getauthByShopName(i, db_conn)
            shopnames_auth_info.append(auth_info)
        for i in shopnames_auth_info:
            res = self.get_shop_products(i, db_conn)
            print '%s ================= %s' % (i['ShopName'], len(res))
            logger.debug('%s ================= %s' % (i['ShopName'], len(res)))
        db_conn.close()
        print " [x] End to get shop products"

    def get_shop_products(self, auth_info, db_conn):
        pageurl = ''
        datalist = []
        while True:
            if pageurl == '':
                url_List_all_Products = "https://api-merchant.joom.com/api/v2/product/multi-get"
                data = {
                    'access_token':auth_info['access_token'] ,
                    'limit': '250',
                }
                dict_ret = requests.get(url_List_all_Products, params=data, timeout = 30)
                _content = eval((dict_ret._content.replace('null', 'None')))
                if  _content['code']== 1015 or _content['code']== 1016:# or _content['code']== 4000   or _content['code']== 1017  or _content['code']== 1018  or _content['code']== 9000   :
                    break
                if dict_ret.status_code==200 and  _content['code']==0 :
                    datalist = datalist + _content['data']

                    if _content.has_key('paging') and _content['paging'].has_key('next'):
                        # logger.debug("_content['paging']['next']: %s" % _content['paging']['next'])
                        pageurl = _content['paging']['next'].replace('\\u0026','&')
                        # logger.debug("pageurl: %s" % pageurl)
                    else:
                        db_conn.commit()
                        break
                else:
                    break
            else:
                # logger.debug('pageurl %s' % pageurl)
                paging_bytes = None
                try:
                    paging_req = urllib2.Request(pageurl)
                    paging_bytes = urllib2.urlopen(paging_req, timeout=60).read()
                    paging_bytes = paging_bytes.replace('null', 'None')
                    # logger.debug('paging_bytes: %s' % paging_bytes)
                except Exception,ex:
                    datalist = []
                    errorinfo = '%s  f_GetShopSKUInfo except Exception= %s ex=%s  __LINE__=%s'%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),Exception,ex,sys._getframe().f_lineno)
                    break

                if paging_bytes is not None:
                    paging_bytes_dict = eval(paging_bytes)
                    datalist = datalist + paging_bytes_dict['data']

                    if paging_bytes_dict.has_key('paging') and paging_bytes_dict['paging'].has_key('next'):
                        if len(paging_bytes_dict['paging']['next']) <= 10 :
                            break
                        else:
                            # logger.debug("paging_bytes_dict['paging']['next']: %s" % paging_bytes_dict['paging']['next'])
                            pageurl = paging_bytes_dict['paging']['next'].replace('\\u0026','&')
                    else:
                        break
                else:
                    break
        # logger.debug('datalist: %s' % datalist)
        return datalist

    def get_shop_names(self, db_conn):
        shopnames_sql = "SELECT DISTINCT ShopName FROM t_config_online_joom WHERE IP='%s'" % self.realIP
        shopnames = self.execute_db(shopnames_sql, db_conn)
        shopname_list = list()
        for i in shopnames:
            shopname_list.append(i['ShopName'])
        return shopname_list

    def getauthByShopName(self, ShopName, db_conn):
        cursor =db_conn.cursor();
        sql = "SELECT IP,ShopName,K,V FROM t_config_online_joom WHERE ShopName= %s "
        # logger.debug('getauthByShopName: %s' % sql)
        cursor.execute(sql,(ShopName.strip(),))
        t_config_online_joom_objs=cursor.fetchall()
        cursor.close()
        auth_info = {}
        auth_info['ShopName'] = ShopName
        for t_config_online_joom_obj in t_config_online_joom_objs:
            auth_info['ShopIP'] = t_config_online_joom_obj[0]
            k = t_config_online_joom_obj[2]
            v = t_config_online_joom_obj[3]
            auth_info[k]=v
        return auth_info

    def get_out_ip(self, url):
        r = requests.get(url)
        txt = r.text
        ip = txt[txt.find("[") + 1: txt.find("]")]
        print('ip:' + ip)
        return ip

    def get_real_url(self, url=r'http://www.ip138.com/'):
        r = requests.get(url)
        txt = r.text
        soup = BeautifulSoup(txt,"html.parser").iframe
        return soup["src"]

    def execute_db(self, sql, db_conn):
        cursor = db_conn.cursor()
        cursor.execute(sql)
        columns = cursor.description
        result = []
        for value in cursor.fetchall():
            tmp = {}
            for (index,column) in enumerate(value):
                tmp[columns[index][0]] = column
            result.append(tmp)

        cursor.close()
        return result

c = Server()
c.listen_client()