#-*-coding:utf-8-*-
u"""
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: token_verification.py
 @time: 2018/6/19 17:02
"""
import os,sys
sys.path.append('/data/djangostack-1.9.7/apps/django/django_projects/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Project.settings')
# from django.db import connection
from brick.table.t_config_online_amazon import t_config_online_amazon

from brick.wish.api.wishapi import cwishapi
from datetime import datetime
import traceback

def get_accesstoken(auth_info,ShopName,conn):
    cwishapi_obj = cwishapi()

    data = {
        'client_id': auth_info['client_id'],
        'client_secret': auth_info['client_secret'],
        'refresh_token': auth_info['refresh_token'],
        'grant_type': 'refresh_token',
    }

    aResult = cwishapi_obj.refresh_token(data, conn, ShopName,auth_info,timeout=30)
    assert aResult['errorcode'] == 1, aResult['errortext']

    return aResult


def verb_token(shopname,conn):
    try:
        online_config_objs = t_config_online_amazon(conn)
        auth_info = online_config_objs.getauthByShopName(shopname)
        if not auth_info:
            raise Exception(u'ERROR: Please configure token information for the store.')

        if not auth_info.get('expiry_time') or not auth_info.get('access_token'):   #  如果 没有 到期时间的
            aResult=get_accesstoken(auth_info,shopname,conn)
            return aResult

        else: # 如果有到期时间的
            expiry_time=datetime.strptime(auth_info['expiry_time'], "%Y-%m-%d %H:%M:%S")
            utc_today=datetime.utcnow()
            if utc_today>=expiry_time:
                aResult=get_accesstoken(auth_info,shopname,conn)
                return aResult
            else:
                return {'errorcode':1,'errortext':'expiry time is ok', 'access_token': auth_info['access_token'],'auth_info': auth_info}

    except Exception as ex:
        return {'errorcode': -1, 'errortext': '%s' % ex}
        # return {'errorcode': -1, 'errortext': '%s' % traceback.format_exc()}






























