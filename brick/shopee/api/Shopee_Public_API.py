# -*- coding: utf-8 -*-

"""
 @desc:
 @author: 张浩
 @site:
"""

import requests
import json
import hashlib
import hmac
from shopee_app.table.t_config_online_shopee import t_config_online_shopee


def get_shop_ip():
    shop_info = t_config_online_shopee.objects.filter(
        K='partner_id').values('IP', 'ShopName')
    shopee_ip = dict()
    for i in shop_info:
        name = i['ShopName']
        shopee_ip[name] = dict()
        shopee_ip[name]['host'] = 'http://' + i['IP'] + ':9193'
    return shopee_ip

def get_partner_key():
    partner_info = t_config_online_shopee.objects.filter(
        K='partner_key').values('ShopName', 'V')
    partner_key = dict()
    for p in partner_info:
        name = p['ShopName']
        partner_key[name] = dict()
        # partner_key[name]['partner_id'] = p.partner_id
        partner_key[name]['partner_key'] = p['V']
    return partner_key


SHOPEEPUBLICGETIP = get_shop_ip()
SHOPEEPUBLICGETKEY = get_partner_key()


class Shopee_Public_API():

    def __init__(self, shopname):
        self.headers = dict()
        self.headers['Content-Type'] = 'application/json'
        self.headers['Content-Length'] = '89'
        self.host = SHOPEEPUBLICGETIP[shopname]['host'] + '/fancyqube' + '/partner.shopeemobile.com/api/v1'
        self.token_url = "https://partner.shopeemobile.com/api/v1"
        self.shopname = shopname

    def sign(self, partner_key, url, data):
        # 加密获取token
        sort_dict = json.dumps(data)
        parameters_str = "%s|%s" % (url, sort_dict)
        h = hmac.new(partner_key.encode(encoding="utf-8"), parameters_str.encode(encoding="utf-8"), digestmod=hashlib.sha256)
        return h.hexdigest().upper()

    def item_add(self, category_id, name, description, price, stock, logistics, weight, images, partner_id, shopid,
                 timestamp, item_sku=None, variations=None, attributes=None,  package_length=None, package_width=None,
                 package_height=None, days_to_ships=None, wholesales=None, size_chart=None, condition=None):
        url = self.host + '/item/add'
        token_url = self.token_url + '/item/add'
        partner_key = SHOPEEPUBLICGETKEY[shopname]['partner_key']

        data = dict()
        data['category_id'] = category_id
        data['name'] = name
        data['description'] = description
        data['price'] = price
        data['stock'] = stock
        data['images'] = images
        data['logistics'] = logistics
        data['weight'] = weight
        data['partner_id'] = partner_id
        data['shopid'] = shopid
        data['timestamp'] = timestamp
        if item_sku:
            data['item_sku'] = item_sku
        if variations:
            data['variations'] = variations
        if attributes:
            data['attributes'] = attributes
        if package_length:
            data['package_length'] = package_length
        if package_width:
            data['package_width'] = package_width
        if package_height:
            data['package_height'] = package_height
        if days_to_ships:
            data['days_to_ships'] = days_to_ships
        if wholesales:
            data['wholesales'] = wholesales
        if size_chart:
            data['size_chart'] = size_chart
        if condition:
            data['condition'] = condition

        token = self.sign(self, partner_key, token_url, data)
        self.headers['Authorization'] = token
        try:
            dict_ret = requests.post(
                url, json=data, headers=self.headers, timeout=60)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)
        return dict_ret

    def item_addvariations(self, item_id, variations, partner_id, shopid, timestamp):
        '''
        return content:
        {
            "item_id": "",
            "modified_time": "",
            "variations": {}
        }
        '''
        url = self.host + '/view/add_variations'
        data = dict()
        data['item_id'] = item_id
        data['variations'] = variations
        data['partner_id'] = partner_id
        data['shopid'] = shopid
        data['timestamp'] = timestamp

        try:
            dict_ret = requests.post(
                url, json=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)
        return dict_ret

    def item_addItemImg(self, item_id, images, partner_id, shopid, timestamp):
        '''
        return content:
        {
            "item_id": "",
            "fail_image": "",
            "images": ""
        }
        '''
        url = self.host + '/item/img/add'
        data = dict()
        data['item_id'] = item_id
        data['images'] = images
        data['partner_id'] = partner_id
        data['shopid'] = shopid
        data['timestamp'] = timestamp

        try:
            dict_ret = requests.post(
                url, json=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)
        return dict_ret

    def item_delete(self, item_id, partner_id, shopid, timestamp):
        '''
        return content:
        {
            "item_id": "",
            "msg": ""
        }
        '''
        url = self.host + '/item/delete'
        data = dict()
        data['item_id'] = item_id
        data['partner_id'] = partner_id
        data['shopid'] = shopid
        data['timestamp'] = timestamp

        try:
            dict_ret = requests.post(
                url, json=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)
        return dict_ret

    def item_deleteItemImg(self, item_id, partner_id, shopid, timestamp, images=None, positions=None):

        url = self.host + '/item/img/delete'
        data = dict()
        data['item_id'] = item_id
        data['partner_id'] = partner_id
        data['shopid'] = shopid
        data['timestamp'] = timestamp
        if images:
            data['images'] = images
        if positions:
            data['positions'] = positions

        try:
            dict_ret = requests.post(
                url, json=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)
        return dict_ret

    def item_deleteVariation(self, item_id, variation_id, partner_id, shopid, timestamp):
        '''
        return content:
        {
            "item_id": "",
            "variation_id": "",
            "moditi"
        }
        '''
        url = self.host + '/item/delete_variation'
        data = dict()
        data['item_id'] = item_id
        data['variation_id'] = variation_id
        data['partner_id'] = partner_id
        data['shopid'] = shopid
        data['timestamp'] = timestamp

        try:
            dict_ret = requests.post(
                url, json=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)
        return dict_ret

    def item_GetAttributes(self, category_id, partner_id, shopid, timestamp, language=None):
        '''
        return content:
        {
            "attributes": [{
                "attribute_id": "",
                "attribute_name": "",
                "is_mandatory": "",
                "attribute_type": "",
                "input_type": "",
                "options": ""
            }]
        }
        '''
        url = self.host + '/item/attributes/get'
        data = dict()
        data['category_id'] = category_id
        data['partner_id'] = partner_id
        data['shopid'] = shopid
        data['timestamp'] = timestamp
        if language:
            data['language'] = language

        try:
            dict_ret = requests.post(
                url, json=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)
        return dict_ret

    def item_GetCategories(self, partner_id, shopid, timestamp):
        '''
        return content:
        {
            categories:{
                'category_id': "",
                'parent_id': "",
                'category_name': "",
                'has_children': ""
            }
        }
        '''
        url = self.host + '/item/categories/get'
        data = dict()
        data['partner_id'] = partner_id
        data['shopid'] = shopid
        data['timestamp'] = timestamp

        try:
            dict_ret = requests.post(
                url, json=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)
        return dict_ret

    def item_GetCategoriesByCountry(self, country, is_cb, partner_id, timestamp):
        '''
        return content:
        {
            "categories": [
            {
                "parent_id": "",
                "has_children": "",
                "category_id": "",
                "category_name": ""
            }
            ]
        }
        '''
        url = self.host + '/item/categories/get_by_country'
        data = dict()
        data['country'] = country
        data['is_cb'] = is_cb
        data['partner_id'] = partner_id
        data['timestamp'] = timestamp

        try:
            dict_ret = requests.post(
                url, json=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)
        return dict_ret

    def item_GetItemDetail(self, item_id, partner_id, shopid, timestamp):
        '''
        return content:
        {
            'item': [{...}],
            'warning': ''
        }
        '''
        url = self.host + '/item/get'
        token_url = self.token_url + '/item/get'
        partner_key = SHOPEEPUBLICGETKEY[self.shopname]['partner_key']
        
        data = dict()
        data['item_id'] = int(item_id)
        data['partner_id'] = int(partner_id)
        data['shopid'] = int(shopid)
        data['timestamp'] = timestamp

        token = self.sign(partner_key, token_url, data)
        self.headers['Authorization'] = token

        try:
            dict_ret = requests.post(
                url, json=data, headers=self.headers, timeout=100)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)
        return dict_ret

    def item_GetItemsList(self, pagination_offset, pagination_entries_per_page, partner_id, shopid, timestamp,
                          update_time_from=None, update_time_to=None):
        '''
        return content:
        {
            "items":[{...}],
            "more": ""
        }
        '''

        url = self.host + '/items/get'
        token_url = self.token_url + '/items/get'
        partner_key = SHOPEEPUBLICGETKEY[self.shopname]['partner_key']

        data = dict()
        data['pagination_offset'] = pagination_offset
        data['pagination_entries_per_page'] = pagination_entries_per_page
        data['partner_id'] = int(partner_id)
        data['shopid'] = int(shopid)
        data['timestamp'] = timestamp
        if update_time_from:
            data['update_time_from'] = update_time_from
        if update_time_to:
            data['update_time_from'] = update_time_to

        token = self.sign(partner_key, token_url, data)
        self.headers['Authorization'] = token
        
        try:
            dict_ret = requests.post(
                url, json=data, headers=self.headers, timeout=100)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)
        return dict_ret

    def item_InsertItemImg(self, item_id, image_url, image_position, partner_id, shopid, timestamp):
        '''
        return content:
        {
            "item_id": "",
            "modified_time": "",
            "images": ""
        }
        '''

        url = self.host + '/item/img/insert'
        data = dict()
        data['item_id'] = item_id
        data['image_url'] = image_url
        data['image_position'] = image_position
        data['partner_id'] = partner_id
        data['shopid'] = shopid
        data['timestamp'] = timestamp

        try:
            dict_ret = requests.post(
                url, json=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)
        return dict_ret

    def item_UpdateItem(self, item_id, category_id, name, description, logistics, weight, partner_id, shopid,
                        timestamp, item_sku=None, variations=None, attributes=None, days_to_ship=None, wholesales=None,
                        package_length=None, package_width=None, package_height=None, size_chart=None, condition=None):
        '''
        return content:
        {...}
        '''

        url = self.host + '/item/update'
        data = dict()
        data['item_id'] = item_id
        data['category_id'] = category_id
        data['name'] = name
        data['description'] = description
        data['logistics'] = logistics
        data['weight'] = weight
        data['partner_id'] = partner_id
        data['shopid'] = shopid
        data['timestamp'] = timestamp
        if item_sku:
            data['item_sku'] = item_sku
        if variations:
            data['variations'] = variations
        if attributes:
            data['attributes'] = attributes
        if days_to_ship:
            data['days_to_ships'] = days_to_ship
        if wholesales:
            data['wholesales'] = wholesales
        if package_length:
            data['package_length'] = package_length
        if package_width:
            data['package_width'] = package_width
        if package_height:
            data['package_height'] = package_height
        if size_chart:
            data['size_chart'] = size_chart
        if condition:
            data['condition'] = condition

        try:
            dict_ret = requests.post(
                url, json=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)
        return dict_ret

    def item_UpdatePrice(self, item_id, price, partner_id, shopid, timestamp):
        '''
        return content:
        {
            'item': [{
                'item_id': '',
                'modified_time': '',
                'price': ''
            }]
        }
        '''

        url = self.host + '/items/update_price'
        data = dict()
        data['item_id'] = item_id
        data['price'] = price
        data['partner_id'] = partner_id
        data['shopid'] = shopid
        data['timestamp'] = timestamp

        try:
            dict_ret = requests.post(
                url, json=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)
        return dict_ret

    def item_UpdateStock(self, item_id, stock, partner_id, shopid, timestamp):
        '''
        return content:
        {
            'item': [{
                'item_id': "",
                'modified_time': "",
                "stock": ""
            }]
        }
        '''

        url = self.host + '/items/update_stock'
        token_url = self.token_url + '/items/update_stock'
        partner_key = SHOPEEPUBLICGETKEY[self.shopname]['partner_key']

        data = dict()
        data['item_id'] = int(item_id)
        data['stock'] = int(stock)
        data['partner_id'] = int(partner_id)
        data['shopid'] = int(shopid)
        data['timestamp'] = timestamp

        token = self.sign(partner_key, token_url, data)
        self.headers['Authorization'] = token

        try:
            dict_ret = requests.post(
                url, json=data, headers=self.headers, timeout=100)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)
        return dict_ret

    def item_UpdateVariationPrice(self, item_id, price, partner_id, shopid, timestamp, variation_id=None):
        '''
        retrun content:
        {
            "item":[{
                "item_id": "",
                "variation_id": "",
                "modified_time": "",
                "price": ""
            }]
        }
        '''

        url = self.host + '/items/update_variation_price'
        data = dict()
        data['item_id'] = item_id
        data['price'] = price
        data['partner_id'] = partner_id
        data['shopid'] = shopid
        data['timestamp'] = timestamp
        if variation_id:
            data['variation_id'] = variation_id

        try:
            dict_ret = requests.post(
                url, json=data, headers=self.headers, timeout=30)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)
        return dict_ret

    def item_UpdateVariationStock(self, item_id, stock, partner_id, shopid, timestamp, variation_id):
        '''
        retrun content:
        {
            "item": [{
                "item_id": "",
                "variation_id": "",
                "modified_time": "",
                "stock": ""
            }]
        }
        '''

        url = self.host + '/items/update_variation_stock'
        token_url = self.token_url + '/items/update_variation_stock'
        partner_key = SHOPEEPUBLICGETKEY[self.shopname]['partner_key']

        data = dict()
        data['item_id'] = int(item_id)
        data['stock'] = int(stock)
        data['partner_id'] = int(partner_id)
        data['shopid'] = int(shopid)
        data['timestamp'] = timestamp
        data['variation_id'] = int(variation_id)

        token = self.sign(partner_key, token_url, data)
        self.headers['Authorization'] = token

        try:
            dict_ret = requests.post(
                url, json=data, headers=self.headers, timeout=100)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)
        return dict_ret

    def item_UpdateStockBatch(self, partner_id, shopid, timestamp, **items):
        '''
        retrun content:
        {
            "item": [{
                "item_id": "",
                "variation_id": "",
                "modified_time": "",
                "stock": ""
            }]
        }
        '''

        url = self.host + '/items/update/items_stock'
        token_url = self.token_url + '/items/update/items_stock'
        partner_key = SHOPEEPUBLICGETKEY[self.shopname]['partner_key']

        data = dict()
        data['partner_id'] = int(partner_id)
        data['shopid'] = int(shopid)
        data['timestamp'] = timestamp
        data['items'] = items

        token = self.sign(partner_key, token_url, data)
        self.headers['Authorization'] = token

        try:
            dict_ret = requests.post(
                url, json=data, headers=self.headers, timeout=100)
        except Exception as e:
            dict_ret = Exception_Error_Obj(e)
        return dict_ret


# class Shopee_Public_API_Token():

#     def __init__(self, url):
#         self.headers = dict()
#         self.url = "https://partner.uat.shopeemobile.com/api/v1" + url

#     def token_by_partner_id(self, partner_id):
#         token = hashlib.sha256(partner_key + redirect).hexdigest()
#         data = dict()
#         data['id'] = partner_id
#         data['token'] = token
#         data['redirect'] = redirect

#         try:
#             dict_ret = requests.get(url, params=data, timeout=30)
#         except Exception as e:
#             dict_ret = Exception_Error_Obj(e)
#         return dict_ret


class Exception_Error_Obj(object):

    def __init__(self, e):
        self.status_code = 500
        self.content = json.dumps({'code': 1, 'data': {}, 'message': str(e)})
