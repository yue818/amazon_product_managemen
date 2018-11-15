# -*- coding: utf-8 -*-
import requests
import datetime

class cwishapi():

    #上架
    def wish_goods_upload_api(self,param,timeout=30):
        try:
            url = 'https://merchant.wish.com/api/v2/product/add'
            data = param

            r = requests.post(url, data, timeout=timeout)
            _content = eval(r._content)
            if r.status_code == 200 and _content['code'] == 0:
                return {'errorcode': 1, 'errortext': '', 'productid': _content['data']['Product']['id']}
            else:
                return {'errorcode': 0, 'errortext': u'%s:%s:%s' % (r.status_code, _content['code'], _content['message'])}
        except  Exception, e:
            return {'errorcode': -1, 'errortext': u'%s:%s' % (Exception, e)}


    def update_to_disable(self,param,timeout=30):
        url = 'https://merchant.wish.com/api/v2/variant/disable'
        data = {
            'access_token':param['access_token'],
            'format': 'json',
            'sku': param['ShopSKU'],
        }
        r_disable = requests.post(url, data=data,timeout=timeout)
        return r_disable

    def update_to_enable(self,param,timeout=30):
        url = 'https://merchant.wish.com/api/v2/variant/enable'
        data = {
            'access_token':param['access_token'],
            'format': 'json',
            'sku': param['ShopSKU'],
        }
        r_enable = requests.post(url, data=data,timeout=timeout)
        return r_enable

    #变体
    def wish_variant_goods_add_api(self, params, timeout=30):
        try:
            url = 'https://merchant.wish.com/api/v2/variant/add'
            data = params

            r = requests.post(url, data, timeout=timeout)
            _content = eval(r._content)
            if r.status_code == 200 and _content['code'] == 0:
                return {'errorcode': 1, 'errortext': ''}
            else:  # code = 1000 店铺SKU已经存在
                return {'errorcode': 0, 'errortext': u'%s:%s:%s' % (r.status_code, _content['code'], _content['message']), 'apicode': _content['code']}
        except  Exception, e:
            return {'errorcode': -1, 'errortext': u'%s:%s' % (Exception, e)}


    def update_wish_goods_data(self,param,timeout=30):
        url = 'https://merchant.wish.com/api/v2/product'
        data = {
           'access_token': param['access_token'],
           'format': 'json',
           'id': param['ProductID'],
           'parent_sku': param['ParentSKU']
        }

        r = requests.get(url, params=data,timeout=timeout)
        return r

    def enable_by_wish_api(self,param,timeout=30):
        url = 'https://merchant.wish.com/api/v2/product/enable'
        data = {
           'access_token': param['access_token'],
           'format': 'json',
           'id': param['ProductID'],
           'parent_sku': param['ParentSKU']
        }

        r = requests.get(url, params=data,timeout=timeout)
        return r

    def disable_by_wish_api(self,param,timeout=30):
        url = 'https://merchant.wish.com/api/v2/product/disable'
        data = {
           'access_token': param['access_token'],
           'format': 'json',
           'id': param['ProductID'],
           'parent_sku': param['ParentSKU']
        }

        r = requests.get(url, params=data,timeout=timeout)
        return r

    def update_goods_info_by_wish_api(self,param,timeout=30):
        url = 'https://merchant.wish.com/api/v2/product/update'
        r = requests.post(url, data=param,timeout=timeout)
        return r

    def update_shopsku_info_by_wish_api(self,param,timeout=30):
        url = 'https://merchant.wish.com/api/v2/variant/update'
        r = requests.post(url, data=param,timeout=timeout)
        return r

    def add_variant_by_parentsku(self,param):
        url = 'https://merchant.wish.com/api/v2/variant/add'

        r = requests.post(url, data=param)
        return r

    def change_shipping_by_(self,param):
        url = 'https://china-merchant.wish.com/api/v2/product/update-multi-shipping'
        # data = {
        #     access_token: 12312312,
        #     format: json,
        #     id: 123123,
        #     AE: 12,
        #     AL: 123,
        #     AR: 123,
        #     AT: 123,
        #     AU: 123,
        #     BA: 123,
        # }

        r = requests.post(url, data=param)
        return r

    def get_shipping_productid(self,param):
        url = 'https://china-merchant.wish.com/api/v2/product/get-all-shipping'
        # data = {
        #     access_token: 12123412413,
        #     format: json,
        #     id: 1234123413,
        #     parent_sku: 23452345,
        #     country: 3452345,
        # }
        r = requests.get(url, params=param)
        return r

    def upload_image_wish(self, param, timeout=30):
        try:
            url = 'https://merchant.wish.com/api/v2/image'
            data = {
                'access_token': param['access_token'],
                'format': 'json',
                'image': param['image'],
            }
            r = requests.post(url, data=data, timeout=timeout)
            _content = eval(r._content)
            if r.status_code == 200 and _content['code'] == 0:
                return {'errorcode': 1, 'errortext': '', 'image_url': _content['data']['url'].replace('\\','')}
            else:
                return {'errorcode': 0, 'errortext': u'%s' % _content.get('message'), 'apicode': _content['code']}

        except  Exception, e:
            return {'errorcode': -1, 'errortext': u'%s:%s' % (Exception, e)}


    def warehouseid(self, access_token, timeout=30):
        try:
            url = "https://merchant.wish.com/api/v2/warehouse/get-all"
            params = {
                "access_token": access_token,
                "format": "json",
            }

            result = requests.get(url, params=params, timeout=timeout)
            _content = eval(result._content)
            if result.status_code == 200 and _content['code'] == 0:
                warehoused = {}
                for ware in _content['data']:
                    if ware['MerchantWarehouse']['warehouse_type_name'] == 'WISH_EXPRESS':
                        warehoused[ware['MerchantWarehouse']['destination_countries'][0]] = ware['MerchantWarehouse']['warehouse_unit_id']
                return {'errorcode': 1, 'errortext': '', 'data': warehoused}
            else:
                return {'errorcode': 0, 'errortext': u'%s:%s:%s' % (result.status_code, _content['code'], _content['message'])}

        except Exception, e:
            return {'errorcode': -1, 'errortext': u'%s:%s' % (Exception, e)}



    def warehouse_vgoodsinfo(self, access_token, productid, warehouse_name, timeout=30):
        try:
            url = "https://merchant.wish.com/api/v2/product"
            params = {
                "access_token": access_token,
                "format": "json",
                "id": productid,
                "warehouse_name": warehouse_name
            }

            result = requests.get(url, params=params, timeout=timeout)
            _content = eval(result._content)
            if result.status_code == 200 and _content['code'] == 0:
                return {'errorcode': 1, 'errortext': '', 'data': _content['data']['Product']['variants']}
            else:
                return {'errorcode': 0, 'errortext': u'%s:%s:%s' % (result.status_code, _content['code'], _content['message'])}
        except Exception, e:
            return {'errorcode': -1, 'errortext': u'%s:%s' % (Exception, e)}



    def update_vinfo(self, param, timeout=30):
        try:
            url = "https://merchant.wish.com/api/v2/variant/update"
            data  = param

            r = requests.post(url, data, timeout=timeout)
            _content = eval(r._content)
            if r.status_code == 200 and _content['code'] == 0:
                return {'errorcode': 1, 'errortext': ''}
            else:
                return {'errorcode': 0, 'errortext': u'%s:%s:%s' % (r.status_code, _content['code'], _content['message'])}
        except Exception, e:
            return {'errorcode': -1, 'errortext': u'%s:%s' % (Exception, e)}


    def refresh_token(self, param, conn, ShopName,auth_info,timeout=30):
        cursor = conn.cursor()
        conn.autocommit = False
        try:
            url = 'https://merchant.wish.com/api/v2/oauth/refresh_token'
            data = param

            rt = requests.post(url, data, timeout=timeout)
            _content = eval(rt._content.replace(':null,',':0,'))

            if rt.status_code == 200 and _content['code'] == 0:

                access_token = _content['data']['access_token']
                refresh_token = _content['data']['refresh_token']
                expiry_time = datetime.datetime.strptime(_content['data']['expiry_string'], '%Y-%m-%d %H:%M:%S UTC') + datetime.timedelta(days=-1)
                qsql="select K from t_config_online_amazon where `Name` = %s"
                cursor.execute(qsql, (ShopName,))
                Ks=cursor.fetchall()
                exist_k=set()
                for K in Ks:
                    exist_k.add(K[0])

                usql = "update t_config_online_amazon set V = %s where `Name` = %s and K = %s ;"
                isql = "insert into t_config_online_amazon(V,`Name`,K) values(%s,%s,%s)"
                sql_args={
                    'access_token':(access_token,ShopName,'access_token'),
                    'refresh_token':(refresh_token,ShopName,'refresh_token'),
                    'last_refresh_token_time':(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),ShopName,'last_refresh_token_time'),
                    'expiry_time':(expiry_time.strftime('%Y-%m-%d %H:%M:%S'),ShopName, 'expiry_time')
                }
                for k in {'access_token','refresh_token','last_refresh_token_time','expiry_time'}:
                    if k in exist_k:
                        cursor.execute(usql,sql_args[k])
                    else:
                        cursor.execute(isql,sql_args[k])

                auth_info['access_token'] = access_token
                auth_info['refresh_token'] = refresh_token
                auth_info['expiry_time'] = expiry_time

                rReuslt = {'errorcode': 1, 'errortext': '', 'access_token': access_token, 'auth_info': auth_info}
                conn.commit()
            else:
                rReuslt = {'errorcode': 0,'errortext': u'%s:%s:%s' % (rt.status_code, _content['code'], _content['message'])}
        except Exception, e:
            conn.rollback()
            rReuslt = {'errorcode': -1, 'errortext': u'%s:%s' % (Exception, e)}

        cursor.close()
        return rReuslt



    def fine_info(self, param, timeout=30):
        try:
            url = "https://www.merchant.wish.com/api/v2/fine"
            data = {
                "access_token": param['access_token'],
                "format": "json",
                "id": param['fine_id']
            }

            result = requests.get(url, params=data, timeout=timeout)
            _content = eval(result._content)
            if result.status_code == 200 and _content['code'] == 0:
                return {'errorcode': 1, 'errortext': '', 'fine_info': _content['data']['Fine']}
            else:
                return {'errorcode': 0, 'errortext': u'{}:{}:{}'.format(result.status_code, _content['code'], _content['message'])}
        except Exception, e:
            return {'errorcode': -1, 'errortext': u'{}'.format(e)}



    def order_detail_info(self,param, timeout=30):
        try:
            url = "https://www.merchant.wish.com/api/v2/order"
            params = {
                "access_token": param['access_token'],
                "format": "json",
                "id": param['order_id'],
            }

            result = requests.get(url, params=params, timeout=timeout)
            _content = eval(result._content)
            if result.status_code == 200 and _content['code'] == 0:
                return {'errorcode': 1, 'errortext': '', 'Order_Info': _content['data']}
            else:
                return {'errorcode': 0, 'errortext': u'{}:{}:{}'.format(result.status_code, _content['code'], _content['message'])}

        except Exception as e:
            return {'errorcode': -1, 'errortext': u'{}'.format(e)}


    def Get_All_Shipping_Prices_of_a_Product(self, param, timeout=30):
        try:
            url = "https://merchant.wish.com/api/v2/product/get-all-shipping"
            params = {
                "access_token": param['access_token'],
                "format": "json",
                "id": param['product_id'],
            }

            result = requests.get(url, params=params, timeout=timeout)
            _content = eval(result._content)
            if result.status_code == 200 and _content['code'] == 0:
                return {'errorcode': 1, 'errortext': '', 'shiping_infors': _content['data']}
            else:
                return {'errorcode': 0, 'errortext': u'{}:{}:{}'.format(result.status_code, _content['code'], _content['message'])}

        except Exception as e:
            return {'errorcode': -1, 'errortext': u'{}'.format(e)}

    def Get_Shipping_Prices_of_a_Product(self, param, timeout=30):
        try:
            url = "https://merchant.wish.com/api/v2/product/get-shipping"
            params = {
                "access_token": param['access_token'],
                "format": "json",
                "id": param['product_id'],
                "country": param['country'],
            }

            result = requests.get(url, params=params, timeout=timeout)
            _content = eval(result._content)
            if result.status_code == 200 and _content['code'] == 0:
                return {'errorcode': 1, 'errortext': '', 'shiping_infors': _content['data']}
            else:
                return {'errorcode': 0, 'errortext': u'{}:{}:{}'.format(result.status_code, _content['code'], _content['message'])}

        except Exception as e:
            return {'errorcode': -1, 'errortext': u'{}'.format(e)}

    def edit_shipping_price_of_a_product(self, param, timeout=30):
        try:
            url = "https://merchant.wish.com/api/v2/product/update-shipping"
            data = param

            result = requests.post(url, data=data, timeout=timeout)
            _content = eval(result._content)
            if result.status_code == 200 and _content['code'] == 0:
                return {'errorcode': 1, 'errortext': '', 'param': param}
            else:
                errortext = _content['message']
                if '\u' in  _content['message']:
                    try:
                        errortext = errortext.decode("unicode_escape")
                    except:
                        pass
                return {
                    'errorcode': 0,
                    'errortext': u'{}:{}:{}; param: {}'.format(result.status_code, _content['code'], errortext, param)
                }

        except Exception as e:
            return {'errorcode': -1, 'errortext': u'{}; param: {}'.format(e, param)}



