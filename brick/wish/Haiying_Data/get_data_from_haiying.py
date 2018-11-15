#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


import time
import requests
import hashlib

from brick.wish.Haiying_Data.haiying_cfg import HYCONFIG

class Haiying:
    """
    根据条件单个/批量查询商品信息
    """

    def data(self,Page_Num):
        timestamp = int(round(time.time() * 1000))
        currentPage = Page_Num
        #pidORpname = None
        salesweek1_from =1

        srcString = (HYCONFIG['u_name'] + HYCONFIG['skey']
                     + str(currentPage)                       #签名串的顺序要注意，page是第一个
                     + str(salesweek1_from)                   #增加了一个参数
                     + str(timestamp)).encode('utf-8')   #timestamp放在最后，每次请求独立一个timestamp。多个请求不要共享一个timestamp，以免服务器端过滤重复请求
        sign = hashlib.md5(srcString).hexdigest()

        url = HYCONFIG['urlGetInfoByPID']
        data = {'u_name': HYCONFIG['u_name'], 'time': str(timestamp), 'sign': sign, 'salesweek1_from': salesweek1_from,
                'currentPage': currentPage}

        r = requests.post(url, data=data)
        j = r.json()
        code = j['code']
        result = None
        if code == 200:
            result = j['result']
        print code
        return result

    def data_bypid_g(self,pid):
        timestamp = int(round(time.time() * 1000))
        currentPage = 1

        srcString = (HYCONFIG['u_name'] + HYCONFIG['skey']
                     + str(currentPage)
                     + str(pid)
                     + str(timestamp)).encode('utf-8')   #timestamp放在最后，每次请求独立一个timestamp。多个请求不要共享一个timestamp，以免服务器端过滤重复请求
        sign = hashlib.md5(srcString).hexdigest()

        url = HYCONFIG['urlGetInfoByPID']
        data = {'u_name': HYCONFIG['u_name'], 'time': str(timestamp), 'sign': sign, 'currentPage': currentPage, 'pidORpname': pid}

        r = requests.post(url, data=data)
        j = r.json()
        code = j['code']
        result = None
        if code == 200:
            result = j['result']
        return result

    def data_bypid(self,pid):
        timestamp = int(round(time.time() * 1000))

        srcString = (HYCONFIG['u_name'] + HYCONFIG['skey']
                     + str(timestamp)
                     + str(pid)).encode('utf-8')
        sign = hashlib.md5(srcString).hexdigest()

        url = HYCONFIG['urlGetInfoByPID_pid']
        data = {'u_name': HYCONFIG['u_name'], 'pid': pid, 'time': str(timestamp), 'sign': sign}
        r = requests.post(url, data=data)
        j = r.json()
        code = j['code']
        result = None
        if code == 200:
            result = j['result']
        return result

    def data_viw_bypid(self,pid):
        timestamp = int(round(time.time() * 1000))

        srcString = (HYCONFIG['u_name'] + HYCONFIG['skey']
                     + str(timestamp)
                     + str(pid)).encode('utf-8')
        sign = hashlib.md5(srcString).hexdigest()

        url = HYCONFIG['urlGetInfoByPID_rating']
        data = {'u_name': HYCONFIG['u_name'], 'pids': pid, 'time': str(timestamp), 'sign': sign}
        r = requests.post(url, data=data)
        j = r.json()
        code = j['code']
        result = None
        if code == 200:
            result = j['result']
        return result

    def data_cname_bypid(self):
        timestamp = int(round(time.time() * 1000))

        srcString = (HYCONFIG['u_name'] + HYCONFIG['skey']
                     + str(timestamp)).encode('utf-8')
        sign = hashlib.md5(srcString).hexdigest()

        url = "http://111.231.88.85:38080/hysj_v2/wish_api/cate_infos"
        data = {'u_name': HYCONFIG['u_name'], 'time': str(timestamp), 'sign': sign}
        r = requests.post(url, data=data)
        j = r.json()
        code = j['code']
        result = None
        if code == 200:
            result = j['result']
        return result