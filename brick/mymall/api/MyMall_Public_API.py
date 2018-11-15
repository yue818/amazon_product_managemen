# -*- coding: utf-8 -*-

import requests
import json
from mymall_app.table.t_config_online_mymall import t_config_online_mymall

# MYMALLPUBLICAPICONFIG = {
#     'Mall-0001-Fanqube/HF': {
#         # 'host': 'http://115.29.213.208:9192',
#         'host': 'http://115.29.213.208:9193',
#     },
#     'Mall-0002-wangyue/HF': {
#         # 'host': 'http://101.200.73.161:9192',
#         'host': 'http://101.200.73.161:9193',
#     },
#     'Mall-0003-SaiYou/HF': {
#         # 'host': 'http://101.200.86.1:9192',
#         'host': 'http://101.200.86.1:9193',
#     },
#     'Mall-0004-Hequ/HF': {
#         # 'host': 'http://120.55.125.236:9192',
#         'host': 'http://120.55.125.236:9193',
#     },
#     'Mall-0005-Yilalei/HF': {
#         # 'host': 'http://123.57.83.18:9192',
#         'host': 'http://123.57.83.18:9193',
#     },
#     'Mall-0006-Jingj/HF': {
#         # 'host': 'http://139.196.44.136:9192',
#         'host': 'http://139.196.44.136:9193',
#     },
#     'Mall-0007-Dingyou/HF': {
#         # 'host': 'http://101.200.212.146:9192',
#         'host': 'http://101.200.212.146:9193',
#     },
#     'test': {
#         'host': 'http://0.0.0.0:9193'
#     }
# }


def get_shop_ip():
    shop_info = t_config_online_mymall.objects.filter(K='client_id').values('IP', 'ShopName')
    mall_shop_ip = dict()
    for i in shop_info:
        mall_shop_ip[i['ShopName']] = dict()
        mall_shop_ip[i['ShopName']]['host'] = 'http://' + i['IP'] + ':9193'

    return mall_shop_ip


MYMALLPUBLICAPICONFIG = get_shop_ip()


class MyMall_Public_API():

    def __init__(self, access_token, shopname):
        self.headers = dict()
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.headers['Authorization'] = 'Bearer %s' % access_token
        # self.host = MYMALLPUBLICAPICONFIG[shopname]['host']
        self.host = MYMALLPUBLICAPICONFIG[shopname]['host'] + '/fancyqube' + '/mall.my.com/merchant/wish/api/v2'

    def product_get(self, product_id=None, parent_sku=None):
        '''
        return content:
            {
              "code": 0,
              "data": {...},
              "message": ""
            }
        '''
        # method = 'GET'
        # url = self.host + '/mymall/product/'
        url = self.host + '/product/'
        data = dict()
        if product_id:
            data['id'] = product_id
        if parent_sku:
            data['parent_sku'] = parent_sku

        try:
            dict_ret = requests.get(url, params=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

        return dict_ret

    def product_add(self, sku, main_image, name, description, tags, inventory, shipping, price, brand=None,
                    landing_page_url=None, upc=None, extra_images=None, parent_sku=None, msrp=None, color=None,
                    size=None, shipping_time=None):
        '''
        return content:
            {
              "code": 0,
              "data": {...},
              "message": ""
            }
        '''
        # method = 'POST'
        # url = self.host + '/mymall/api/v2/product/add'
        url = self.host + '/product/add'
        data = dict()
        data['sku'] = sku
        data['main_image'] = main_image
        data['name'] = name
        data['description'] = description
        data['tags'] = tags
        data['inventory'] = inventory
        data['shipping'] = shipping
        data['price'] = price
        if brand:
            data['brand'] = brand
        if landing_page_url:
            data['landing_page_url'] = landing_page_url
        if upc:
            data['upc'] = upc
        if extra_images:
            data['extra_images'] = extra_images
        if parent_sku:
            data['parent_sku'] = parent_sku
        if msrp:
            data['msrp'] = msrp
        if color:
            data['color'] = color
        if size:
            data['size'] = size
        if shipping_time:
            data['shipping_time'] = shipping_time

        # data = json.dumps(data)

        try:
            dict_ret = requests.post(url, json=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

        return dict_ret

    def product_update(self, product_id, parent_sku, name=None, description=None, tags=None, brand=None,
                       landing_page_url=None, upc=None, extra_images=None, main_image=None):
        '''
        return content:
            {
              "code": 0,
              "data": {...},
              "message": ""
            }
        '''
        # method = 'POST'
        # url = self.host + '/mymall/api/v2/product/update/'
        url = self.host + '/product/update'
        data = dict()
        data['id'] = product_id
        data['parent_sku'] = parent_sku
        if name:
            data['name'] = name
        if description:
            data['description'] = description
        if tags:
            data['tags'] = tags
        if brand:
            data['brand'] = brand
        if landing_page_url:
            data['landing_page_url'] = landing_page_url
        if upc:
            data['upc'] = upc
        if extra_images:
            data['extra_images'] = extra_images
        if main_image:
            data['main_image'] = main_image

        # data = json.dumps(data)

        try:
            dict_ret = requests.post(url, json=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

        return dict_ret

    def product_enable(self, product_id):
        '''
        return content:
            {
              "code": 0,
              "data": [],
              "message": ""
            }
        '''
        # method = 'POST'
        # url = self.host + '/mymall/api/v2/product/enable/'
        url = self.host + '/product/enable'
        data = dict()
        data['id'] = product_id

        # data = json.dumps(data)

        try:
            dict_ret = requests.post(url, json=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

        return dict_ret

    def product_disable(self, product_id):
        '''
        return content:
            {
              "code": 0,
              "data": [],
              "message": ""
            }
        '''
        # method = 'POST'
        # url = self.host + '/mymall/api/v2/product/disable/'
        url = self.host + '/product/disable'
        data = dict()
        data['id'] = product_id

        # data = json.dumps(data)

        try:
            dict_ret = requests.post(url, json=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

        return dict_ret

    def product_get_download_job_status(self, job_id):
        '''
        return content:
            {
              "code": 0,
              "data": {
                "status": "FAILED",
                "created_date": "2018-03-12 12:27:13"
              },
              "message": ""
            }

            {
                "code":0,
                "data":{
                    "status":"PENDING",
                    "total_count":0,
                    "processed_count":0,
                    "download_link":"",
                    "cancelled_time":"",
                    "end_run_time":"",
                    "start_run_time":"",
                    "created_date":"2018-05-26T12:05:57+03:00"
                },
                "message":""
            }
        '''
        # method = 'POST'
        # url = self.host + '/mymall/api/v2/product/get_download_job_status/'
        url = self.host + '/product/get_download_job_status'
        data = dict()
        data['job_id'] = job_id
        # data = json.dumps(data)

        try:
            dict_ret = requests.post(url, json=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

        return dict_ret

    def product_create_download_job(self):
        '''
        return content:
            {
              "code": 0,
              "data": {
                "job_id": "a4cfe0a3c4db7ff65187be2ec05e7673"
              },
              "message": ""
            }
        '''
        # method = 'POST'
        # url = self.host + '/mymall/api/v2/product/create_download_job'
        url = self.host + '/product/create_download_job'
        # data = dict()

        try:
            dict_ret = requests.post(url, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

        return dict_ret

    def product_remove_extra_images(self, product_id):
        '''
        return content:
            {
              "code": 0,
              "data": [],
              "message": ""
            }
        '''
        # method = 'POST'
        # url = self.host + '/mymall/api/v2/product/remove_extra_images/'
        url = self.host + '/product/remove_extra_images'
        data = dict()
        data['id'] = product_id

        # data = json.dumps(data)

        try:
            dict_ret = requests.post(url, json=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

        return dict_ret

    def product_cancel_download_job(self, job_id):
        '''
        return content:
            {
              "code": 0,
              "data": {
                "message": "Job has already been finished. Use \"POST /get-download-job-status\" for getting download link"
              },
              "message": ""
            }
        '''
        # mrthod = 'POST'
        # url = self.host + '/mymall/api/v2/product/cancel_download_job/'
        url = self.host + '/product/cancel_download_job'
        data = dict()
        data['job_id'] = job_id

        # data = json.dumps(data)

        try:
            dict_ret = requests.post(url, json=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

        return dict_ret

    def variant_get(self, shop_sku):
        '''
        return content:
            ...
        '''
        # method = 'GET'
        # url = self.host + '/mymall/product/variant/'
        url = self.host + '/variant'
        data = dict()
        data['sku'] = shop_sku

        try:
            dict_ret = requests.get(url, params=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

        return dict_ret

    def variant_add(self, parent_shop_sku, shop_sku, inventory, price, shipping, msrp=None, main_image=None, color=None, size=None):
        '''
        return content:
            ...
        '''
        # method = 'POST'
        # url = self.host + '/mymall/api/v2/product/variant/add/'
        url = self.host + '/variant/add'
        data = dict()
        data['parent_sku'] = parent_shop_sku
        data['sku'] = shop_sku
        data['inventory'] = inventory
        data['price'] = price
        data['shipping'] = shipping
        if msrp:
            data['msrp'] = msrp
        if main_image:
            data['main_image'] = main_image
        if color:
            data['color'] = color
        if size:
            data['size'] = size

        # data = json.dumps(data)

        try:
            dict_ret = requests.post(url, json=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

        return dict_ret

    def variant_update(self, shop_sku, msrp=None, inventory=None, price=None, shipping=None,
                       main_image=None, color=None, shipping_time=None, size=None, enabled=None,
                       weight=None):
        '''
        return content:
            ...
        '''
        # method = 'POST'
        # url = self.host + '/mymall/api/v2/product/variant/update/'
        url = self.host + '/variant/update'
        data = dict()
        data['sku'] = shop_sku
        if msrp:
            data['msrp'] = msrp
        if inventory:
            data['inventory'] = inventory
        if price:
            data['price'] = price
        if shipping:
            data['shipping'] = shipping
        if main_image:
            data['main_image'] = main_image
        if color:
            data['color'] = color
        if shipping_time:
            data['shipping_time'] = shipping_time
        if size:
            data['size'] = size
        if enabled:
            data['enabled'] = enabled
        if weight:
            data['weight'] = weight

        # data = json.dumps(data)

        try:
            dict_ret = requests.post(url, json=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

        return dict_ret

    def variant_disable(self, shop_sku):
        '''
        return content:
            ...
        '''
        # method = 'POST'
        # url = self.host + '/mymall/api/v2/product/variant/disable/'
        url = self.host + '/variant/disable'
        data = dict()
        data['sku'] = shop_sku

        # data = json.dumps(data)

        try:
            dict_ret = requests.post(url, json=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

        return dict_ret

    def variant_enable(self, shop_sku):
        '''
        return content:
            ...
        '''
        # method = 'POST'
        # url = self.host + '/mymall/api/v2/product/variant/enable/'
        url = self.host + '/variant/enable'
        data = dict()
        data['sku'] = shop_sku

        # data = json.dumps(data)

        try:
            dict_ret = requests.post(url, json=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

        return dict_ret


class MyMall_Public_API_Token():

    def __init__(self, shopname):
        self.headers = dict()
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.host = MYMALLPUBLICAPICONFIG[shopname]['host'] + '/fancyqube' + '/mall.my.com/oauth/v2/token'

    def token_by_password(self, client_id, client_secret, username, password):
        '''
        return content:
            {
                "access_token": "NGFiNmU5YjU2MDA4ZGMzZTdmOWVkM2ZkMTUxZjFmMGE0M2E2ZDY0YjhlMDhmNjkzMDkyZjRjZjQ1OTRhNTE2NA",
                "expires_in": 3600,
                "token_type": "bearer",
                "scope": null,
                "refresh_token": "OWJkMjBmZjc0M2NmZjc2NmRjNjMzZGZmZTljNGViOWVjZWY4NzQ0YzYyMDc1OWE2MmRlNWIzYWUyMjM5Y2NkZA"
            }
        '''
        # method = 'POST'
        # url = self.host + '/mymall/api/v2/get_token_by_password/'
        url = self.host
        data = dict()
        data['grant_type'] = 'password'
        data['client_id'] = client_id
        data['client_secret'] = client_secret
        data['username'] = username
        data['password'] = password

        # data = json.dumps(data)

        try:
            dict_ret = requests.post(url, json=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

        return dict_ret

    def refresh_token(self, client_id, client_secret, refresh_token):
        '''
        return content:
            {
                "access_token": "MWRjZWMzZDliNmJjNzg2OGYyNWE3OGY4MTlmZDNkMTFiNDcxYmI0MmU0ZTAyYmYwY2Q5ZjYyNTJiZmI2MWRjYg",
                "expires_in": 3600,
                "token_type": "bearer",
                "scope": null,
                "refresh_token": "YjQ4YmY4Njk1ZGEyZDk5MjAxNmVkMDQ1MTE4YmE4OGM4NDQyYTQwNDI5MzM5MjY4Y2M5MGFmNTQ1NTUzMDk2Yg"
            }
        '''
        # method = 'POST'
        # url = self.host + '/mymall/api/v2/refresh_token/'
        url = self.host
        data = dict()
        data['grant_type'] = 'refresh_token'
        data['client_id'] = client_id
        data['client_secret'] = client_secret
        data['refresh_token'] = refresh_token

        # data = json.dumps(data)

        try:
            dict_ret = requests.post(url, json=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

        return dict_ret


class Exception_Error_Obj(object):

    def __init__(self, e):
        self.status_code = 500
        self.content = json.dumps({'code': 1, 'data': {}, 'message': str(e)})
