# encoding: utf-8
'''
@author: zhangyu
@contact: 292724306@qq.com
@software: pycharm
@file: wish_ticket_syn.py
@time: 2018-06-11 13:46
'''
import requests
import json
import MySQLdb
from datetime import datetime
from django.db import connection
from django.db import transaction
import logging
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


class wish_ticket_syn():

    def __init__(self):
        self.my_conn = connection
        self.my_cursor = self.my_conn.cursor()
        self.db_conn = connection
        self.cursor = self.db_conn.cursor()

    def getData(self, access_token):
        url = "https://merchant.wish.com/api/v2/ticket/get-action-required"
        params = {
            "access_token": access_token,
            "format": "json",
            "limit": "500",
        }
        try:
            r = requests.get(url, params=params, timeout=30)
            _content = eval(r._content)
            if r.status_code == 200 and _content['code'] == 0:
                return {'errorcode': 1, 'data': _content['data']}
            else:
                return {'errorcode': 0,'errortext': u'%s:%s:%s' % (r.status_code, _content['code'], _content['message'])}
        except Exception as e:
            return {'errorcode': -1, 'errortext': u'%s' % e}


    def get_access_token(self, shopName):
        sql = "select K, V from t_config_online_amazon where Name = '{}'".format(shopName)
        self.my_cursor.execute(sql)
        rts = self.my_cursor.fetchall()
        access_token = ''
        for rt in rts:
            if rt[0] == 'access_token':
                access_token = rt[1]
        return access_token

    def insertDB(self, shopName):
        try:
            auth_info = verb_token(shopName, self.db_conn)
            access_token = auth_info.get('access_token')
            if access_token:
                info = self.getData(access_token)
                if info['errorcode'] == 1:
                    list_ticket = []
                    if info['data']:  # data 不为空
                        objs_tmp = t_store_configuration_file.objects.filter(ShopName_temp=shopName).values('Operators')
                        Operators = objs_tmp[0]['Operators'] if objs_tmp else ''

                        try:
                            for data in info['data']:
                                logger.error('data--------------------------------------%s' % data)
                                dict_ticket = {'shopName': shopName, 'updateTime': datetime.now(),
                                               'Operators': Operators,
                                               'default_refund_reason': '', 'label': '', 'sublabel': '',
                                               'open_date': '',
                                               'state': '', 'UserInfo_locale': '', 'UserInfo_joined_date': '',
                                               'UserInfo_id': '',
                                               'UserInfo_name': '', 'last_update_date': '', 'state_id': '',
                                               'merchant_id': '',
                                               'photo_proof': '', 'ticket_id': '', 'ticket_transaction_id': '',
                                               'subject': ''}

                                data['Ticket'].pop('replies')
                                data['Ticket'].pop('items')
                                ticket_dict = data['Ticket']
                                for k, v in ticket_dict.items():
                                    if k == 'UserInfo':
                                        for x, y in ticket_dict['UserInfo'].items():
                                            if x == 'id':
                                                x = 'UserInfo_id'
                                            elif x == 'locale':
                                                x = 'UserInfo_locale'
                                            elif x == 'joined_date':
                                                x = 'UserInfo_joined_date'
                                            elif x == 'name':
                                                x = 'UserInfo_name'
                                            if '\u' in y:
                                                try:
                                                    y = y.decode("unicode_escape")
                                                except:
                                                    pass
                                            dict_ticket[x] = y
                                    else:
                                        if k == 'id':
                                            k = 'ticket_id'
                                        elif k == 'transaction_id':
                                            k = 'ticket_transaction_id'
                                        if '\u' in v:
                                            try:
                                                v = v.decode("unicode_escape")
                                            except:
                                                pass
                                        dict_ticket[k] = v

                                list_ticket.append(dict_ticket)
                        except Exception, e1:
                            logger.error('--------------------------------------%s' % e1)
                            # 数据同步错误
                            return 3

                    try:
                        transaction.set_autocommit(False)

                        truncateSQL = "delete from wish_ticket where shopName='{}'".format(shopName)

                        insertSQL = "INSERT INTO wish_ticket(shopName,label,sublabel,open_date,state," \
                                    "UserInfo_locale,UserInfo_joined_date,UserInfo_id,UserInfo_name,last_update_date," \
                                    "state_id,default_refund_reason,merchant_id,photo_proof,ticket_id," \
                                    "ticket_transaction_id,subject,updateTime, Operators) VALUE (%(shopName)s," \
                                    "%(label)s,%(sublabel)s,%(open_date)s,%(state)s,%(UserInfo_locale)s," \
                                    "%(UserInfo_joined_date)s,%(UserInfo_id)s,%(UserInfo_name)s,%(last_update_date)s," \
                                    "%(state_id)s,%(default_refund_reason)s,%(merchant_id)s,%(photo_proof)s," \
                                    "%(ticket_id)s,%(ticket_transaction_id)s,%(subject)s,%(updateTime)s,%(Operators)s)"

                        self.cursor.execute(truncateSQL)
                        self.cursor.executemany(insertSQL, list_ticket)
                        transaction.commit()

                        return 0
                    except Exception, e1:
                        logger.error('--------------------------------------%s' % e1)
                        transaction.rollback()
                        # 数据同步错误
                        return 3

                else:
                    logger.error("error token:{}".format(shopName))
                    # 错误的token
                    return 2
            else:
                # 没有token
                return 1
        except Exception, e:
            return 0

    def closeDB(self):
        if self.cursor:
            self.cursor.close()
        if self.db_conn:
            self.db_conn.close()
        if self.my_cursor:
            self.my_cursor.close()
        if self.my_conn:
            self.my_conn.close()
