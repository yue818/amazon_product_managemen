#!/usr/bin/python
# coding: utf-8

# import os
# import random
# import datetime
# import threading
# from urllib import unquote
import sys
import time
import json
import requests
# import simplejson
import logging
import logging.handlers
import BaseHTTPServer
import SimpleHTTPServer


log_formatter = logging.Formatter('%(asctime)s [%(filename)s %(funcName)s:%(lineno)d] %(thread)d %(levelname)s %(message)s')
logFile = 'mall_api_server.log'
my_handler = logging.handlers.RotatingFileHandler(
    logFile,
    mode='a',
    maxBytes=100 * 1024 * 1024,
    backupCount=4,
    encoding=None,
    delay=0)

my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.DEBUG)

logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

logger.addHandler(my_handler)
logger.addHandler(ch)


class MyMallAPI():

    def __init__(self, access_token):
        self.headers = dict()
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.headers['Authorization'] = 'Bearer %s' % access_token

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
        url = 'https://mall.my.com/merchant/wish/api/v2/product/'
        data = dict()
        if product_id:
            data['id'] = product_id
        if parent_sku:
            data['parent_sku'] = parent_sku.replace('%23', '#').replace('%24', '$').replace('%21', '!')

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
        url = 'https://mall.my.com/merchant/wish/api/v2/product/add'
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

        try:
            dict_ret = requests.post(url, data=data, headers=self.headers, timeout=30)
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
        url = 'https://mall.my.com/merchant/wish/api/v2/product/update'
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

        try:
            dict_ret = requests.post(url, data=data, headers=self.headers, timeout=30)
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
        url = 'https://mall.my.com/merchant/wish/api/v2/product/enable'
        data = dict()
        data['id'] = product_id

        try:
            dict_ret = requests.post(url, data=data, headers=self.headers, timeout=30)
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
        url = 'https://mall.my.com/merchant/wish/api/v2/product/disable'
        data = dict()
        data['id'] = product_id

        try:
            dict_ret = requests.post(url, data=data, headers=self.headers, timeout=30)
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
        url = 'https://mall.my.com/merchant/wish/api/v2/product/get-download-job-status'
        data = dict()
        data['job_id'] = job_id

        try:
            dict_ret = requests.post(url, data=data, headers=self.headers, timeout=30)
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
        url = 'https://mall.my.com/merchant/wish/api/v2/product/create-download-job'
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
        url = 'https://mall.my.com/merchant/wish/api/v2/product/remove-extra-images'
        data = dict()
        data['id'] = product_id

        try:
            dict_ret = requests.post(url, data=data, headers=self.headers, timeout=30)
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
        url = 'https://mall.my.com/merchant/wish/api/v2/order/cancel-download-job'
        data = dict()
        data['job_id'] = job_id

        try:
            dict_ret = requests.post(url, data=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

        return dict_ret

    def variant_get(self, shop_sku):
        '''
        return content:
            ...
        '''
        # method = 'GET'
        url = 'https://mall.my.com/merchant/wish/api/v2/variant'
        data = dict()
        data['sku'] = shop_sku.replace('%23', '#').replace('%24', '$').replace('%21', '!')

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
        url = 'https://mall.my.com/merchant/wish/api/v2/variant/add'
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

        try:
            dict_ret = requests.post(url, data=data, headers=self.headers, timeout=30)
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
        url = 'https://mall.my.com/merchant/wish/api/v2/variant/update'
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

        try:
            dict_ret = requests.post(url, data=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

        return dict_ret

    def variant_disable(self, shop_sku):
        '''
        return content:
            ...
        '''
        # method = 'POST'
        url = 'https://mall.my.com/merchant/wish/api/v2/variant/disable'
        data = dict()
        data['sku'] = shop_sku

        try:
            dict_ret = requests.post(url, data=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

        return dict_ret

    def variant_enable(self, shop_sku):
        '''
        return content:
            ...
        '''
        # method = 'POST'
        url = 'https://mall.my.com/merchant/wish/api/v2/variant/enable'
        data = dict()
        data['sku'] = shop_sku

        try:
            dict_ret = requests.post(url, data=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

        return dict_ret


class MyMallAPIToken():

    def __init__(self):
        self.headers = dict()
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.url = 'https://mall.my.com/oauth/v2/token'

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
        data = dict()
        data['grant_type'] = 'password'
        data['client_id'] = client_id
        data['client_secret'] = client_secret
        data['username'] = username
        data['password'] = password

        try:
            dict_ret = requests.post(self.url, data=data, headers=self.headers, timeout=30)
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
        data = dict()
        data['grant_type'] = 'refresh_token'
        data['client_id'] = client_id
        data['client_secret'] = client_secret
        data['refresh_token'] = refresh_token

        try:
            dict_ret = requests.post(self.url, data=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

        return dict_ret


class Exception_Error_Obj(object):

    def __init__(self, e):
        self.status_code = 500
        self._content = json.dumps({'code': 1, 'data': {}, 'message': str(e)})


class SETHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        logger.debug("GET")
        path = self.path
        logger.debug('path: %s' % path)
        message = path.split('?')
        logger.debug('message list info: %s' % message)
        Authorization = self.headers.getheader('Authorization')
        if Authorization:
            access_token = Authorization.split('Bearer ')[-1]
            if len(message) > 1:
                url = message[0]
                params = message[1]
                params = self.handle_data_to_json(params)
            else:
                url = message[0]
                params = ''
            logger.debug('url: %s' % url)
            logger.debug('params: %s' % params)

            code = 204
            content = params

            mymall_api_obj = MyMallAPI(access_token)
            if url == '/mymall/product/':
                product_id = params.get('id')
                parent_sku = params.get('parent_sku')
                gd_job_resp = mymall_api_obj.product_get(product_id=product_id, parent_sku=parent_sku)
                content = gd_job_resp.content
                code = gd_job_resp.status_code
            elif url == '/mymall/product/variant/':
                shop_sku = params.get('sku')
                gd_job_resp = mymall_api_obj.variant_get(shop_sku)
                content = gd_job_resp.content
                code = gd_job_resp.status_code
            else:
                pass
        else:
            code = 500
            content = {'message': 'Authorization not found'}

        logger.debug('content: %s' % content)
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        logger.debug("POST")
        logger.debug(self.headers)
        path = self.path
        logger.debug('path: %s' % path)
        length = int(self.headers.getheader('content-length'))
        Authorization = self.headers.getheader('Authorization')
        if Authorization:
            access_token = Authorization.split('Bearer ')[-1]
        else:
            access_token = ''

        qs = self.rfile.read(length)
        logger.debug('qs: %s' % qs)
        logger.debug('dir(self.rfile): %s' % dir(self.rfile))
        try:
            request_data = json.loads(qs)
            # request_data = unquote(qs)
        except Exception as e:
            logger.debug(e)
            request_data = ''

        logger.debug("request_data: %s" % request_data)
        code = 204
        content = ''
        # data = self.handle_data_to_json(request_data)
        data = request_data

        mymall_api_obj = MyMallAPI(access_token)
        mymall_token_api_obj = MyMallAPIToken()

        code, content = self.relay_request_url(path, data, mymall_api_obj, mymall_token_api_obj)
        logger.debug('content: %s' % content)

        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(content)

    def handle_data_to_json(self, data):
        data_dict = dict()
        if not data:
            return data_dict
        datas = data.split('&')
        for i in datas:
            data_info = i.split('=')
            data_dict[data_info[0]] = data_info[1].replace('+', ' ').replace('%23', '#').replace('%24', '$').replace('%21', '!') \
                .replace('%25', '%').replace('%26', '&').replace('%20', ' ').replace('%21', '!').replace('%28', '(').replace('%29', ')') \
                .replace('%3A', ':').replace('%40', '@').replace('%5F', '_').replace('%7B', '{').replace('%7D', '}')
        return data_dict

    def relay_request_url(self, url, data, mymall_api_obj, mymall_token_api_obj):
        code = 204
        content = ''

        if url == '/mymall/api/v2/product/add/':
            res = self.request_product_add(mymall_api_obj, data)
            code = res['code']
            content = res['content']
        elif url == '/mymall/api/v2/product/update/':
            res = self.request_product_update(mymall_api_obj, data)
            code = res['code']
            content = res['content']
        elif url == '/mymall/api/v2/product/enable/':
            res = self.request_product_enable(mymall_api_obj, data)
            code = res['code']
            content = res['content']
        elif url == '/mymall/api/v2/product/disable/':
            res = self.request_product_disable(mymall_api_obj, data)
            code = res['code']
            content = res['content']
        elif url == '/mymall/api/v2/product/get_download_job_status/':
            res = self.request_product_get_download_job_status(mymall_api_obj, data)
            code = res['code']
            content = res['content']
        elif url == '/mymall/api/v2/product/create_download_job/':
            res = self.request_product_create_download_job(mymall_api_obj, data)
            code = res['code']
            content = res['content']
        elif url == '/mymall/api/v2/product/remove_extra_images/':
            res = self.request_product_remove_extra_images(mymall_api_obj, data)
            code = res['code']
            content = res['content']
        elif url == '/mymall/api/v2/product/cancel_download_job/':
            res = self.request_product_cancel_download_job(mymall_api_obj, data)
            code = res['code']
            content = res['content']
        elif url == '/mymall/api/v2/product/variant/add/':
            res = self.request_product_variant_add(mymall_api_obj, data)
            code = res['code']
            content = res['content']
        elif url == '/mymall/api/v2/product/variant/update/':
            res = self.request_product_variant_update(mymall_api_obj, data)
            code = res['code']
            content = res['content']
        elif url == '/mymall/api/v2/product/variant/enable/':
            res = self.request_product_variant_enable(mymall_api_obj, data)
            code = res['code']
            content = res['content']
        elif url == '/mymall/api/v2/product/variant/disable/':
            res = self.request_product_variant_disable(mymall_api_obj, data)
            code = res['code']
            content = res['content']
        elif url == '/mymall/api/v2/refresh_token/':
            res = self.request_refresh_token(mymall_token_api_obj, data)
            code = res['code']
            content = res['content']
        elif url == '/mymall/api/v2/get_token_by_password/':
            res = self.request_get_token_by_password(mymall_token_api_obj, data)
            code = res['code']
            content = res['content']
        else:
            pass

        return code, content

    def request_product_add(self, mymall_api_obj, data):
        sku = data.get('sku')
        main_image = data.get('main_image')
        name = data.get('name')
        description = data.get('description')
        tags = data.get('tags')
        inventory = data.get('inventory')
        shipping = data.get('shipping')
        price = data.get('price')
        brand = data.get('brand', None)
        landing_page_url = data.get('landing_page_url', None)
        upc = data.get('upc', None)
        extra_images = data.get('extra_images', None)
        parent_sku = data.get('parent_sku', None)
        msrp = data.get('msrp', None)
        color = data.get('color', None)
        size = data.get('size', None)
        shipping_time = data.get('shipping_time', None)

        responses = mymall_api_obj.product_add(sku, main_image, name, description, tags, inventory, shipping, price,
                                               brand=brand, landing_page_url=landing_page_url, upc=upc, extra_images=extra_images,
                                               parent_sku=parent_sku, msrp=msrp, color=color, size=size, shipping_time=shipping_time)

        sRes = {'code': responses.status_code, 'content': responses.content}
        return sRes

    def request_product_update(self, mymall_api_obj, data):
        product_id = data.get('id')
        parent_sku = data.get('parent_sku')
        name = data.get('name', None)
        description = data.get('description', None)
        tags = data.get('tags', None)
        brand = data.get('brand', None)
        landing_page_url = data.get('landing_page_url', None)
        upc = data.get('upc', None)
        extra_images = data.get('extra_images', None)
        main_image = data.get('main_image', None)

        responses = mymall_api_obj.product_update(product_id, parent_sku, name=name, description=description, tags=tags, brand=brand,
                                                  landing_page_url=landing_page_url, upc=upc, extra_images=extra_images, main_image=main_image)

        sRes = {'code': responses.status_code, 'content': responses.content}
        return sRes

    def request_product_enable(self, mymall_api_obj, data):
        product_id = data.get('id')

        responses = mymall_api_obj.product_enable(product_id)

        sRes = {'code': responses.status_code, 'content': responses.content}
        return sRes

    def request_product_disable(self, mymall_api_obj, data):
        product_id = data.get('id')

        responses = mymall_api_obj.product_disable(product_id)

        sRes = {'code': responses.status_code, 'content': responses.content}
        return sRes

    def request_product_get_download_job_status(self, mymall_api_obj, data):
        job_id = data.get('job_id')

        responses = mymall_api_obj.product_get_download_job_status(job_id)

        sRes = {'code': responses.status_code, 'content': responses.content}
        return sRes

    def request_product_create_download_job(self, mymall_api_obj, data):
        responses = mymall_api_obj.product_create_download_job()

        sRes = {'code': responses.status_code, 'content': responses.content}
        return sRes

    def request_product_remove_extra_images(self, mymall_api_obj, data):
        product_id = data.get('id')

        responses = mymall_api_obj.product_remove_extra_images(product_id)

        sRes = {'code': responses.status_code, 'content': responses.content}
        return sRes

    def request_product_cancel_download_job(self, mymall_api_obj, data):
        job_id = data.get('job_id')

        responses = mymall_api_obj.product_cancel_download_job(job_id)

        sRes = {'code': responses.status_code, 'content': responses.content}
        return sRes

    def request_product_variant_add(self, mymall_api_obj, data):
        parent_shop_sku = data.get('parent_sku')
        shop_sku = data.get('sku')
        inventory = data.get('inventory')
        price = data.get('price')
        shipping = data.get('shipping')
        msrp = data.get('msrp')
        main_image = data.get('main_image')
        color = data.get('color')
        size = data.get('size')

        responses = mymall_api_obj.variant_add(parent_shop_sku, shop_sku, inventory, price, shipping, msrp=msrp, main_image=main_image, color=color, size=size)

        sRes = {'code': responses.status_code, 'content': responses.content}
        return sRes

    def request_product_variant_update(self, mymall_api_obj, data):
        shop_sku = data.get('sku')
        msrp = data.get('msrp')
        inventory = data.get('inventory')
        price = data.get('price')
        shipping = data.get('shipping')
        main_image = data.get('main_image')
        color = data.get('color')
        shipping_time = data.get('shipping_time')
        size = data.get('size')
        enabled = data.get('enabled')
        weight = data.get('weight')

        responses = mymall_api_obj.variant_update(shop_sku, msrp=msrp, inventory=inventory, price=price, shipping=shipping,
                                                  main_image=main_image, color=color, shipping_time=shipping_time,
                                                  size=size, enabled=enabled, weight=weight)

        sRes = {'code': responses.status_code, 'content': responses.content}
        return sRes

    def request_product_variant_enable(self, mymall_api_obj, data):
        shop_sku = data.get('sku')

        responses = mymall_api_obj.variant_enable(shop_sku)

        sRes = {'code': responses.status_code, 'content': responses.content}
        return sRes

    def request_product_variant_disable(self, mymall_api_obj, data):
        shop_sku = data.get('sku')

        responses = mymall_api_obj.variant_disable(shop_sku)

        sRes = {'code': responses.status_code, 'content': responses.content}
        return sRes

    def request_refresh_token(self, mymall_token_api_obj, data):
        client_id = data.get('client_id')
        client_secret = data.get('client_secret')
        refresh_token = data.get('refresh_token')

        responses = mymall_token_api_obj.refresh_token(client_id, client_secret, refresh_token)

        sRes = {'code': responses.status_code, 'content': responses.content}
        return sRes

    def request_get_token_by_password(self, mymall_token_api_obj, data):
        client_id = data.get('client_id')
        client_secret = data.get('client_secret')
        username = data.get('username')
        password = data.get('password')

        responses = mymall_token_api_obj.token_by_password(client_id, client_secret, username, password)

        sRes = {'code': responses.status_code, 'content': responses.content}
        return sRes


class Server():

    def __init__(self):
        pass

    def listen_client(self):
        ServerClass = BaseHTTPServer.HTTPServer
        Protocol = "HTTP/1.0"

        if sys.argv[1:]:
            port = int(sys.argv[1])
        else:
            port = 9192
        server_address = ('0.0.0.0', port)

        SETHandler.protocol_version = Protocol
        httpd = ServerClass(server_address, SETHandler)

        sa = httpd.socket.getsockname()
        logger.debug("Serving HTTP on %s port %s ..." % (sa[0], sa[1]))
        # print "Serving HTTP on %s port %s ..." % (sa[0], sa[1])
        httpd.serve_forever()


def retry():
    try:
        c = Server()
        c.listen_client()
        time.sleep(0.5)
    except Exception as e:
        logger.error(e)
        time.sleep(0.5)
        retry()


if __name__ == '__main__':
    retry()
