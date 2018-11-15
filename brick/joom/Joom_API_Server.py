#!/usr/bin/python
# coding: utf-8

# import os
# import random
# import datetime
# import threading
# import simplejson
# from urllib import unquote
import sys
import time
import json
import requests
import logging
import logging.handlers
import BaseHTTPServer
import SimpleHTTPServer
from bs4 import BeautifulSoup


log_formatter = logging.Formatter('%(asctime)s [%(filename)s %(funcName)s:%(lineno)d] %(thread)d %(levelname)s %(message)s')
logFile = 'Joom_API_Server.log'
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

JOOMIPURL = {
    '47.100.224.71': '/joom/1/api/v2/',
    '119.23.144.25': '/joom/2/api/v2/',
    '114.115.161.21': '/joom/3/api/v2/',
    '121.43.198.134': '/joom/4/api/v2/',
    '120.26.7.212': '/joom/5/api/v2/',
    '115.29.213.208': '/joom/6/api/v2/',
    '120.76.171.177': '/joom/7/api/v2/',
    '120.76.118.141': '/joom/8/api/v2/',
    '121.41.52.241': '/joom/9/api/v2/',
}


class Joom_API():

    def __init__(self, access_token):
        self.headers = dict()
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.headers['Authorization'] = 'Bearer %s' % access_token
        self.access_token = access_token
        self.head_url = 'https://api-merchant.joom.com/api/v2'

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
        url = self.head_url + '/product'
        data = dict()
        data['access_token'] = self.access_token
        data['id'] = product_id

        try:
            dict_ret = requests.get(url, params=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

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
        url = self.head_url + '/product/add'
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
        url = self.head_url + '/product/update'
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
        url = self.head_url + '/product/enable'
        data = dict()
        data['access_token'] = self.access_token
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
        url = self.head_url + '/product/disable'
        data = dict()
        data['access_token'] = self.access_token
        data['id'] = product_id

        try:
            dict_ret = requests.post(url, data=data, headers=self.headers, timeout=30)
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
        url = self.head_url + '/product/remove-extra-images'
        data = dict()
        data['access_token'] = self.access_token
        data['id'] = product_id

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
        url = self.head_url + '/variant'
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
        url = self.head_url + '/variant/add'
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
        url = self.head_url + '/variant/update'
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
        url = self.head_url + '/variant/disable'
        data = dict()
        data['access_token'] = self.access_token
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
        url = self.head_url + '/variant/enable'
        data = dict()
        data['access_token'] = self.access_token
        data['sku'] = shop_sku

        try:
            dict_ret = requests.post(url, data=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

        return dict_ret

    def auth_test(self, ):
        url = self.head_url + '/auth_test'
        self.headers['access_token'] = self.access_token

        try:
            dict_ret = requests.get(url, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)

        return dict_ret


class Joom_API_Token():

    def __init__(self):
        self.headers = dict()
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.head_url = 'https://api-merchant.joom.com/api/v2'

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
        url = self.head_url + '/access_token'
        data = dict()
        self.headers['client_id'] = client_id
        self.headers['client_secret'] = client_secret
        self.headers['code'] = code
        self.headers['grant_type'] = grant_type
        self.headers['redirect_uri'] = redirect_uri

        try:
            dict_ret = requests.post(url, data=data, headers=self.headers, timeout=30)
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
        # New joom api not work
        # url = self.head_url + '/refresh_token'

        url = self.head_url + '/oauth/refresh_token'
        data = dict()
        self.headers['grant_type'] = 'refresh_token'
        self.headers['client_id'] = client_id
        self.headers['client_secret'] = client_secret
        self.headers['refresh_token'] = refresh_token

        data['grant_type'] = 'refresh_token'
        data['client_id'] = client_id
        data['client_secret'] = client_secret
        data['refresh_token'] = refresh_token

        try:
            # New joom api not work
            # dict_ret = requests.post(url, data=data, headers=self.headers, timeout=30)
            dict_ret = requests.post(url, params=data, timeout=30)
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

            joom_api_obj = Joom_API(access_token)
            if url == url_start + 'product/':
                product_id = params.get('id')
                gd_job_resp = joom_api_obj.product_get(product_id)
                content = gd_job_resp.content
                code = gd_job_resp.status_code
            elif url == url_start + 'variant/':
                shop_sku = params.get('sku')
                gd_job_resp = joom_api_obj.variant_get(shop_sku)
                content = gd_job_resp.content
                code = gd_job_resp.status_code
            else:
                pass
        elif path == '/':
            code = 204
            content = {}
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

        joom_api_obj = Joom_API(access_token)
        joom_token_api_obj = Joom_API_Token()

        code, content = self.relay_request_url(path, data, joom_api_obj, joom_token_api_obj)
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
            data_dict[data_info[0]] = data_info[1].replace('+', ' ')
        return data_dict

    def relay_request_url(self, url, data, joom_api_obj, joom_token_api_obj):
        code = 204
        content = ''

        if url == url_start + 'product/add/':
            res = self.request_product_add(joom_api_obj, data)
            code = res['code']
            content = res['content']
        elif url == url_start + 'product/update/':
            res = self.request_product_update(joom_api_obj, data)
            code = res['code']
            content = res['content']
        elif url == url_start + 'product/enable/':
            res = self.request_product_enable(joom_api_obj, data)
            code = res['code']
            content = res['content']
        elif url == url_start + 'product/disable/':
            res = self.request_product_disable(joom_api_obj, data)
            code = res['code']
            content = res['content']
        elif url == url_start + 'product/remove_extra_images/':
            res = self.request_product_remove_extra_images(joom_api_obj, data)
            code = res['code']
            content = res['content']
        elif url == url_start + 'variant/add/':
            res = self.request_product_variant_add(joom_api_obj, data)
            code = res['code']
            content = res['content']
        elif url == url_start + 'variant/update/':
            res = self.request_product_variant_update(joom_api_obj, data)
            code = res['code']
            content = res['content']
        elif url == url_start + 'variant/enable/':
            res = self.request_product_variant_enable(joom_api_obj, data)
            code = res['code']
            content = res['content']
        elif url == url_start + 'variant/disable/':
            res = self.request_product_variant_disable(joom_api_obj, data)
            code = res['code']
            content = res['content']
        elif url == url_start + 'auth_test/':
            res = self.request_auth_test(joom_api_obj, data)
            code = res['code']
            content = res['content']
        elif url == url_start + 'access_token/':
            res = self.request_access_token(joom_token_api_obj, data)
            code = res['code']
            content = res['content']
        elif url == url_start + 'refresh_token/':
            res = self.request_refresh_token(joom_token_api_obj, data)
            code = res['code']
            content = res['content']
        else:
            pass

        return code, content

    def request_product_add(self, joom_api_obj, data):
        parent_sku = data.get('parent_sku')
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
        msrp = data.get('msrp', None)
        color = data.get('color', None)
        size = data.get('size', None)
        shipping_time = data.get('shipping_time', None)

        responses = joom_api_obj.product_add(parent_sku, main_image, name, description, tags, inventory, shipping, price,
                                             brand=brand, landing_page_url=landing_page_url, upc=upc, extra_images=extra_images,
                                             msrp=msrp, color=color, size=size, shipping_time=shipping_time)

        sRes = {'code': responses.status_code, 'content': responses.content}
        return sRes

    def request_product_update(self, joom_api_obj, data):
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

        responses = joom_api_obj.product_update(product_id, parent_sku, name=name, description=description, tags=tags, brand=brand,
                                                landing_page_url=landing_page_url, upc=upc, extra_images=extra_images, main_image=main_image)

        sRes = {'code': responses.status_code, 'content': responses.content}
        return sRes

    def request_product_enable(self, joom_api_obj, data):
        product_id = data.get('id')

        responses = joom_api_obj.product_enable(product_id)

        sRes = {'code': responses.status_code, 'content': responses.content}
        return sRes

    def request_product_disable(self, joom_api_obj, data):
        product_id = data.get('id')

        responses = joom_api_obj.product_disable(product_id)

        sRes = {'code': responses.status_code, 'content': responses.content}
        return sRes

    def request_product_remove_extra_images(self, joom_api_obj, data):
        product_id = data.get('id')

        responses = joom_api_obj.product_remove_extra_images(product_id)

        sRes = {'code': responses.status_code, 'content': responses.content}
        return sRes

    def request_product_variant_add(self, joom_api_obj, data):
        parent_shop_sku = data.get('parent_sku')
        shop_sku = data.get('sku')
        inventory = data.get('inventory')
        price = data.get('price')
        shipping = data.get('shipping')
        msrp = data.get('msrp')
        main_image = data.get('main_image')
        color = data.get('color')
        size = data.get('size')

        responses = joom_api_obj.variant_add(parent_shop_sku, shop_sku, inventory, price, shipping, msrp=msrp, main_image=main_image, color=color, size=size)

        sRes = {'code': responses.status_code, 'content': responses.content}
        return sRes

    def request_product_variant_update(self, joom_api_obj, data):
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

        responses = joom_api_obj.variant_update(shop_sku, msrp=msrp, inventory=inventory, price=price, shipping=shipping,
                                                main_image=main_image, color=color, shipping_time=shipping_time,
                                                size=size, enabled=enabled, weight=weight)

        sRes = {'code': responses.status_code, 'content': responses.content}
        return sRes

    def request_product_variant_enable(self, joom_api_obj, data):
        shop_sku = data.get('sku')

        responses = joom_api_obj.variant_enable(shop_sku)

        sRes = {'code': responses.status_code, 'content': responses.content}
        return sRes

    def request_product_variant_disable(self, joom_api_obj, data):
        shop_sku = data.get('sku')

        responses = joom_api_obj.variant_disable(shop_sku)

        sRes = {'code': responses.status_code, 'content': responses.content}
        return sRes

    def request_auth_test(self, joom_api_obj, data):
        responses = joom_api_obj.auth_test()

        sRes = {'code': responses.status_code, 'content': responses.content}
        return sRes

    def request_access_token(self, joom_token_api_obj, data):
        client_id = data.get('client_id')
        client_secret = data.get('client_secret')
        code = data.get('code')

        responses = joom_token_api_obj.access_token(client_id, client_secret, code)

        sRes = {'code': responses.status_code, 'content': responses.content}
        return sRes

    def request_refresh_token(self, joom_token_api_obj, data):
        client_id = data.get('client_id')
        client_secret = data.get('client_secret')
        refresh_token = data.get('refresh_token')

        responses = joom_token_api_obj.refresh_token(client_id, client_secret, refresh_token)

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
            port = 9181
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


def get_reverse_proxy_joom_url():
    realip = get_out_ip(get_real_url())
    head_url = JOOMIPURL.get(realip, '')
    return head_url


def get_out_ip(url):
    r = requests.get(url, timeout=30)
    txt = r.text
    ip = txt[txt.find("[") + 1: txt.find("]")]
    print('ip:' + ip)
    return ip


def get_real_url(url=r'http://www.ip138.com/'):
    r = requests.get(url, timeout=30)
    txt = r.text
    soup = BeautifulSoup(txt, "html.parser").iframe
    return soup["src"]

if __name__ == '__main__':
    global url_start
    url_start = get_reverse_proxy_joom_url()
    retry()
