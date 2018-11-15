# -*- coding: utf-8 -*-

import requests
import json

# 通用代理转发请求

ONLINEJOOMPUBLICAPICONFIG = {
    'JOOM-0001': {
        'url_start': 'http://47.100.224.71:9193',
    },
    'JOOM-0002': {
        'url_start': 'http://119.23.144.25:9193',
    },
    'JOOM-0003': {
        'url_start': 'http://114.115.161.21:9193',
    },
    'JOOM-0004': {
        'url_start': 'http://121.43.198.134:9193',
    },
    'JOOM-0005': {
        'url_start': 'http://120.26.7.212:9193',
    },
    'JOOM-0006': {
        'url_start': 'http://115.29.213.208:9193',
    },
    'JOOM-0007': {
        'url_start': 'http://120.76.171.177:9193',
    },
    'JOOM-0008': {
        'url_start': 'http://120.76.118.141:9193',
    },
    'JOOM-0009': {
        'url_start': 'http://121.41.52.241:9193',
    },
}

# 直接代理转发请求

JOOMPUBLICAPIHOSTCONFIG = {
    'JOOM-0001': {
        'url_start': 'http://47.100.224.71:9181/joom/1/api/v2',
    },
    'JOOM-0002': {
        'url_start': 'http://119.23.144.25:9181/joom/2/api/v2',
    },
    'JOOM-0003': {
        'url_start': 'http://114.115.161.21:9181/joom/3/api/v2',
    },
    'JOOM-0004': {
        'url_start': 'http://121.43.198.134:9181/joom/4/api/v2',
    },
    'JOOM-0005': {
        'url_start': 'http://120.26.7.212:9181/joom/5/api/v2',
    },
    'JOOM-0006': {
        'url_start': 'http://115.29.213.208:9181/joom/6/api/v2',
    },
    'JOOM-0007': {
        'url_start': 'http://120.76.171.177:9181/joom/7/api/v2',
    },
    'JOOM-0008': {
        'url_start': 'http://120.76.118.141:9181/joom/8/api/v2',
    },
    'JOOM-0009': {
        'url_start': 'http://121.41.52.241:9181/joom/9/api/v2',
    },
}

# Nginx反向代理转发请求

NGINX_IP = 'http://192.168.107.11'

JOOMPUBLICAPIURLCONFIG = {
    'JOOM-0001': {
        'url_start': '%s/joom/1/api/v2' % NGINX_IP,
    },
    'JOOM-0002': {
        'url_start': '%s/joom/2/api/v2' % NGINX_IP,
    },
    'JOOM-0003': {
        'url_start': '%s/joom/3/api/v2' % NGINX_IP,
    },
    'JOOM-0004': {
        'url_start': '%s/joom/4/api/v2' % NGINX_IP,
    },
    'JOOM-0005': {
        'url_start': '%s/joom/5/api/v2' % NGINX_IP,
    },
    'JOOM-0006': {
        'url_start': '%s/joom/6/api/v2' % NGINX_IP,
    },
    'JOOM-0007': {
        'url_start': '%s/joom/7/api/v2' % NGINX_IP,
    },
    'JOOM-0008': {
        'url_start': '%s/joom/8/api/v2' % NGINX_IP,
    },
    'JOOM-0009': {
        'url_start': '%s/joom/9/api/v2' % NGINX_IP,
    },
}


class Joom_Public_API():

    def __init__(self, access_token, shopname_temp):
        self.headers = dict()
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.headers['Authorization'] = 'Bearer %s' % access_token
        # self.url_start = JOOMPUBLICAPIHOSTCONFIG[shopname_temp]['url_start']
        self.url_start = ONLINEJOOMPUBLICAPICONFIG[shopname_temp]['url_start'] + '/fancyqube' + '/api-merchant.joom.com/api/v2'
        self.access_token = access_token

    def product_get(self, product_id):
        '''
        return content:
            {
              "code": 0,
              "data": {...},
              "message": ""
            }
        '''
        # method = 'GET'
        # url = self.url_start + '/product/'
        url = self.url_start + '/product'
        data = dict()
        data['access_token'] = self.access_token
        data['id'] = product_id

        dict_ret = requests.get(url, params=data, headers=self.headers, timeout=30)
        # try:
        #     dict_ret = requests.get(url, params=data, headers=self.headers, timeout=30)
        # except Exception as e:
        #     dict_ret = Exception_Error_Obj(e)

        return dict_ret

    def product_add(self, parent_sku, main_image, name, description, tags, inventory, shipping, price, brand=None,
                    landing_page_url=None, upc=None, extra_images=None, msrp=None, color=None, size=None, shipping_time=None):
        '''
        return content:
            {
              "code": 0,
              "data": {...},
              "message": ""
            }
        '''
        # method = 'POST'
        # url = self.url_start + '/product/add/'
        url = self.url_start + '/product/add'
        data = dict()
        data['access_token'] = self.access_token
        data['parent_sku'] = parent_sku
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
        # url = self.url_start + '/product/update/'
        url = self.url_start + '/product/update'
        data = dict()
        data['access_token'] = self.access_token
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
        # url = self.url_start + '/product/enable/'
        url = self.url_start + '/product/enable'
        data = dict()
        data['access_token'] = self.access_token
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
        # url = self.url_start + '/product/disable/'
        url = self.url_start + '/product/disable'
        data = dict()
        data['access_token'] = self.access_token
        data['id'] = product_id

        # data = json.dumps(data)

        try:
            dict_ret = requests.post(url, json=data, headers=self.headers, timeout=30)
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
        # url = self.url_start + '/product/remove_extra_images/'
        url = self.url_start + '/product/remove_extra_images'
        data = dict()
        data['access_token'] = self.access_token
        data['id'] = product_id

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
        # url = self.url_start + '/variant/'
        url = self.url_start + '/variant'
        data = dict()
        data['access_token'] = self.access_token
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
        # url = self.url_start + '/variant/add/'
        url = self.url_start + '/variant/add'
        data = dict()
        data['access_token'] = self.access_token
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
        # url = self.url_start + '/variant/update/'
        url = self.url_start + '/variant/update'
        data = dict()
        data['access_token'] = self.access_token
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
        # url = self.url_start + '/variant/disable/'
        url = self.url_start + '/variant/disable'
        data = dict()
        data['access_token'] = self.access_token
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
        # url = self.url_start + '/variant/enable/'
        url = self.url_start + '/variant/enable'
        data = dict()
        data['access_token'] = self.access_token
        data['sku'] = shop_sku

        # data = json.dumps(data)

        try:
            dict_ret = requests.post(url, json=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

        return dict_ret

    def auth_test(self, ):
        # url = self.url_start + '/auth_test/'
        url = self.url_start + '/auth_test'
        # data = dict()
        # data['access_token'] = self.access_token
        self.headers['access_token'] = self.access_token

        # data = json.dumps(data)

        try:
            # dict_ret = requests.post(url, json=data, headers=self.headers, timeout=30)
            dict_ret = requests.post(url, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

        return dict_ret

    def order_shipping_lable(self, order_id):
        url = self.url_start + '/order/shipping-label'
        # self.headers['access_token'] = self.access_token

        data = dict()
        data['access_token'] = self.access_token
        data['id'] = order_id

        try:
            dict_ret = requests.get(url, params=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

        return dict_ret


class Joom_Public_API_Token():

    def __init__(self, shopname_temp):
        self.headers = dict()
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        # self.url_start = JOOMPUBLICAPIHOSTCONFIG[shopname_temp]['url_start']
        self.url_start = ONLINEJOOMPUBLICAPICONFIG[shopname_temp]['url_start'] + '/fancyqube' + '/api-merchant.joom.com/api/v2'

    def access_token(self, client_id, client_secret, code, grant_type='authorization_code', redirect_uri='https://merchant.joom.it'):
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
        url = self.url_start + '/access_token'
        data = dict()

        # data['grant_type'] = grant_type
        # data['client_id'] = client_id
        # data['client_secret'] = client_secret
        # data['code'] = code
        # data['redirect_uri'] = redirect_uri

        self.headers['grant_type'] = grant_type
        self.headers['client_id'] = client_id
        self.headers['client_secret'] = client_secret
        self.headers['code'] = code
        self.headers['redirect_uri'] = redirect_uri

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
        # url = self.url_start + '/refresh_token/'
        url = self.url_start + '/oauth/refresh_token'
        data = dict()
        data['grant_type'] = 'refresh_token'
        data['client_id'] = client_id
        data['client_secret'] = client_secret
        data['refresh_token'] = refresh_token

        # data = json.dumps(data)

        try:
            # dict_ret = requests.post(url, data=data, headers=self.headers, timeout=30)
            dict_ret = requests.post(url, params=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

        return dict_ret


class Exception_Error_Obj(object):

    def __init__(self, e):
        self.status_code = 500
        self.content = json.dumps({'code': 1, 'data': {}, 'message': str(e)})
