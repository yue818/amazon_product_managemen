# -*- coding:utf-8 -*-

"""
 @desc:
 @author: 孙健
 @site:
"""


import json
import datetime

from brick.mymall.api.MyMall_Public_API import MyMall_Public_API_Token
from mymall_app.table.t_config_online_mymall import t_config_online_mymall


def refresh_token_fun(shopname, username, password, client_id, client_secret, refresh_token):
    sRes = {'code': 0, 'message': ''}
    refresh_token_obj = MyMall_Public_API_Token(shopname)
    res = refresh_token_obj.refresh_token(client_id, client_secret, refresh_token)
    if res.status_code == 200:
        content = json.loads(res.content)
        access_token = content['access_token']
        refresh_token = content['refresh_token']
        mymall_config_objs = t_config_online_mymall.objects.filter(ShopName__exact=shopname)
        for i in mymall_config_objs:
            if i.K == 'access_token':
                i.V = access_token
                i.save()
            elif i.K == 'refresh_token':
                i.V = refresh_token
                i.save()
            elif i.K == 'last_refresh_token_time':
                i.V = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                i.save()
    elif res.status_code == 400:
        get_new_token = get_auth_token_fun(shopname, client_id, client_secret, username, password)
        sRes['code'] = get_new_token['code']
        sRes['message'] = get_new_token['message']
    else:
        sRes['code'] = 1
        sRes['message'] = res

    return sRes


def get_auth_token_fun(shopname, client_id, client_secret, username, password):
    sRes = {'code': 0, 'message': ''}
    token_api_obj = MyMall_Public_API_Token(shopname)
    res = token_api_obj.token_by_password(client_id, client_secret, username, password)
    if res.status_code == 200:
        content = json.loads(res.content)
        access_token = content['access_token']
        refresh_token = content['refresh_token']
        mymall_config_objs = t_config_online_mymall.objects.filter(ShopName__exact=shopname)
        for i in mymall_config_objs:
            if i.K == 'access_token':
                i.V = access_token
                i.save()
            elif i.K == 'refresh_token':
                i.V = refresh_token
                i.save()
            elif i.K == 'last_refresh_token_time':
                i.V = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                i.save()
    else:
        sRes['code'] = 1
        sRes['message'] = res

    return sRes


def get_config_mymall(shopname):
    auth_info = t_config_online_mymall.objects.filter(ShopName__exact=shopname).values('K', 'V')
    access_token = ''
    refresh_token = ''
    client_id = ''
    client_secret = ''
    username = ''
    password = ''
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
            elif i['K'] == 'username':
                username = i['V']
            elif i['K'] == 'password':
                password = i['V']
            elif i['K'] == 'last_refresh_token_time':
                last_refresh_token_time = i['V']

    mymall_auth = dict()
    mymall_auth['access_token'] = access_token
    mymall_auth['refresh_token'] = refresh_token
    mymall_auth['client_id'] = client_id
    mymall_auth['client_secret'] = client_secret
    mymall_auth['username'] = username
    mymall_auth['password'] = password
    mymall_auth['last_refresh_token_time'] = last_refresh_token_time

    return mymall_auth


def check_auth_token(shopname):
    sRes = {'code': 0, 'message': ''}
    auth_info = get_config_mymall(shopname)
    now_date = datetime.datetime.now()
    if auth_info['last_refresh_token_time']:
        last_refresh_token_time = auth_info['last_refresh_token_time']
        last_refresh_token_time = datetime.datetime.strptime(last_refresh_token_time, '%Y-%m-%d %H:%M:%S')
        time = now_date - last_refresh_token_time
    else:
        time = datetime.timedelta(seconds=3600)

    if time.total_seconds() > 2400:
        refresh_res = refresh_token_fun(shopname, auth_info['username'], auth_info['password'], auth_info['client_id'],
                                        auth_info['client_secret'], auth_info['refresh_token'])
        sRes = refresh_res

    return sRes
