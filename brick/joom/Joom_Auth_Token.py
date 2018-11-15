# -*- coding:utf-8 -*-

"""
 @desc:
 @author: 孙健
 @site:
"""


import json
import datetime

from brick.joom.api.Joom_Public_API import Joom_Public_API_Token
from joom_app.table.t_config_online_joom import t_config_online_joom


def refresh_token_fun(shopname, code, client_id, client_secret, refresh_token):
    sRes = {'code': 0, 'message': ''}
    shopname_temp = shopname[:9]
    refresh_token_obj = Joom_Public_API_Token(shopname_temp)
    res = refresh_token_obj.refresh_token(client_id, client_secret, refresh_token)
    if res.status_code == 200:
        content = json.loads(res._content)
        access_token = content['data']['access_token']
        refresh_token = content['data']['refresh_token']
        mymall_config_objs = t_config_online_joom.objects.filter(ShopName__exact=shopname)
        for i in mymall_config_objs:
            if i.K == 'access_token':
                i.V = access_token
                i.save()
            elif i.K == 'refresh_token':
                i.V = refresh_token
                i.save()
            elif i.K == 'last_refresh_token_time':
                i.V = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                i.save()
    elif res.status_code == 400:
        get_new_token = get_auth_token_fun(shopname, client_id, client_secret, code)
        sRes['code'] = get_new_token['code']
        sRes['message'] = get_new_token['message']
    else:
        sRes['code'] = 1
        sRes['message'] = res

    return sRes


def get_auth_token_fun(shopname, client_id, client_secret, code):
    sRes = {'code': 0, 'message': ''}
    shopname_temp = shopname[:9]
    token_api_obj = Joom_Public_API_Token(shopname_temp)
    res = token_api_obj.access_token(client_id, client_secret, code)
    if res.status_code == 200:
        content = json.loads(res._content)
        access_token = content['data']['access_token']
        refresh_token = content['data']['refresh_token']
        mymall_config_objs = t_config_online_joom.objects.filter(ShopName__exact=shopname)
        for i in mymall_config_objs:
            if i.K == 'access_token':
                i.V = access_token
                i.save()
            elif i.K == 'refresh_token':
                i.V = refresh_token
                i.save()
            elif i.K == 'last_refresh_token_time':
                i.V = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                i.save()
    else:
        sRes['code'] = 1
        sRes['message'] = res

    return sRes


def get_config_joom(shopname):
    auth_info = t_config_online_joom.objects.filter(ShopName__exact=shopname).values('K', 'V')
    access_token = ''
    refresh_token = ''
    client_id = ''
    client_secret = ''
    code = ''
    last_refresh_token_time = ''
    if auth_info:
        for i in auth_info:
            if i['K'] == 'access_token':
                access_token = i['V']
            elif i['K'] == 'refresh_token':
                refresh_token = i['V']
            elif i['K'] == 'client_id':
                client_id = i['V']
            elif i['K'] == 'client_secret':
                client_secret = i['V']
            elif i['K'] == 'code':
                code = i['V']
            elif i['K'] == 'last_refresh_token_time':
                last_refresh_token_time = i['V']

    mymall_auth = dict()
    mymall_auth['access_token'] = access_token
    mymall_auth['refresh_token'] = refresh_token
    mymall_auth['client_id'] = client_id
    mymall_auth['client_secret'] = client_secret
    mymall_auth['code'] = code
    mymall_auth['last_refresh_token_time'] = last_refresh_token_time

    return mymall_auth


def check_auth_token(shopname):
    sRes = {'code': 0, 'message': ''}
    auth_info = get_config_joom(shopname)
    now_date = datetime.datetime.now()
    if auth_info['last_refresh_token_time']:
        last_refresh_token_time = auth_info['last_refresh_token_time']
        last_refresh_token_time = datetime.datetime.strptime(last_refresh_token_time, '%Y-%m-%d %H:%M:%S.%f')
        time = now_date - last_refresh_token_time
    else:
        time = datetime.timedelta(seconds=2592000)

    if time.total_seconds() > 2505600:
        refresh_res = refresh_token_fun(shopname, auth_info['code'], auth_info['client_id'],
                                        auth_info['client_secret'], auth_info['refresh_token'])
        sRes = refresh_res

    return sRes
