# encoding: utf-8
'''
@author: zhangyu
@contact: 292724306@qq.com
@software: pycharm
@file: wish_infractions_syn.py
@time: 2018-06-13 14:46
'''
import requests
import json
import MySQLdb
from django.db import connection
import logging
from datetime import datetime
from skuapp.table.t_store_configuration_file import t_store_configuration_file
from brick.wish.wish_api_before.token_verification import verb_token
logger = logging.getLogger('sourceDns.webdns.views')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hq_db',
        # 'HOST': 'hequskuapp.mysql.rds.aliyuncs.com',
        'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
        'PORT': '3306',
        'USER': 'by15161458383',
        'PASSWORD': 'K120Esc1'
    },
    'syn': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'py_db',
        # 'HOST': 'hequskuapp.mysql.rds.aliyuncs.com',
        'HOST': 'rm-uf6kd5a4wee2n2ze6rw.mysql.rds.aliyuncs.com',
        'PORT': '3306',
        'USER': 'by15161458383',
        'PASSWORD': 'K120Esc1'
    },
    'pic': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pic_db',
        # 'HOST': 'hequskuapp.mysql.rds.aliyuncs.com',
        'HOST': 'rm-uf6kd5a4wee2n2ze6rw.mysql.rds.aliyuncs.com',
        'PORT': '3306',
        'USER': 'by15161458383',
        'PASSWORD': 'K120Esc1'
    }

}

connection_lll = connection


class wish_infractions_syn():

    def __init__(self):
        self.my_conn = connection_lll
        self.my_cursor = self.my_conn.cursor()
        self.db_conn = connection
        self.cursor = self.db_conn.cursor()

    def get_infractions_count(self, access_token):
        url = "https://merchant.wish.com/api/v2/count/infractions"
        params = {
            "access_token": access_token,
            "format": "json",
        }
        try:
            r = requests.get(url, params=params, timeout=30)
            info = json.loads(r.text)
            return info
        except:
            return {}

    def get_access_token(self, shopName):
        # shopName = 'Wish-0236'
        sql = "select K, V from t_config_online_amazon where Name = '{}'".format(shopName)
        self.my_cursor.execute(sql)
        rts = self.my_cursor.fetchall()
        access_token = ''
        for rt in rts:
            if rt[0] == 'access_token':
                access_token = rt[1]
        return access_token

    def insertDB(self, shopName):
        code = 0
        infractions_count = 0
        try:
            auth_info = verb_token(shopName, self.db_conn)
            access_token = auth_info.get('access_token')
            if access_token:
                objs_tmp = t_store_configuration_file.objects.filter(ShopName_temp=shopName).values('Operators')
                Operators = objs_tmp[0]['Operators'] if objs_tmp else ''
                dict_infractions_count = self.get_infractions_count(access_token)
                if 'code' in dict_infractions_count and dict_infractions_count[
                    'code'] == 0 and 'data' in dict_infractions_count and 'CountInfractionsResponse' in \
                        dict_infractions_count['data'] and 'count' in dict_infractions_count['data'][
                        'CountInfractionsResponse']:
                    infractions_count = int(dict_infractions_count['data']['CountInfractionsResponse']['count'])
                    dict_infractions = {'shopName': shopName, 'updateTime': datetime.now(),
                                        'infractions_count': infractions_count, 'Operators': Operators}
                    try:
                        truncateSQL = "delete from wish_infractions where shopName='{}'".format(
                            shopName)
                        self.cursor.execute(truncateSQL)
                        insertSQL = "INSERT INTO wish_infractions(shopName, infractions_count,Operators, updateTime) VALUE (%(shopName)s, %(infractions_count)s, %(Operators)s, %(updateTime)s)"
                        self.cursor.execute(insertSQL, dict_infractions)
                    except MySQLdb.Error, e:
                        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                        self.db_conn.rollback()
                        # 数据同步错误
                        code = 3
                    else:
                        self.db_conn.commit()
                        code = 0
                else:
                    # 错误的token
                    code = 2
            else:
                # 没有token
                code = 1
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            code = 3
        finally:
            return code

    def closeDB(self):
        if self.cursor:
            self.cursor.close()
        if self.db_conn:
            self.db_conn.close()
        if self.my_cursor:
            self.my_cursor.close()
        if self.my_conn:
            self.my_conn.close()
