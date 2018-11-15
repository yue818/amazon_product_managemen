# -*- coding:utf-8 -*-

"""
 @desc:
 @author: 孙健
 @site:
"""

import json
import datetime

from mymall_app.table.t_mymall_template_publish import t_mymall_template_publish
from mymall_app.table.t_mymall_online_info import t_mymall_online_info
from mymall_app.table.t_mymall_online_info_detail import t_mymall_online_info_detail
from skuapp.table.t_store_configuration_file import t_store_configuration_file

from brick.mymall.api.MyMall_Public_API import MyMall_Public_API
from brick.mymall.MyMall_Auth_Token import refresh_token_fun
from brick.mymall.MyMall_Auth_Token import get_config_mymall
from brick.mymall.MyMall_Auth_Token import check_auth_token


def My_Mall_Publish_Product(pro_id, publish_user):
    sRes = {'code': 1, 'message': ''}
    try:
        pro_obj = t_mymall_template_publish.objects.get(pk=pro_id)
    except t_mymall_template_publish.DoesNotExist:
        sRes['code'] = -1
        sRes['message'] = 'This Product of id: %s, does not exist' % pro_id
        return sRes

    shopname = pro_obj.ShopName

    auth_info = get_config_mymall(shopname)
    check_res = check_auth_token(shopname)
    if check_res['code'] == 0:
        auth_info = get_config_mymall(shopname)
    else:
        sRes['code'] = 1
        sRes['message'] = check_res['message']
        return sRes

    access_token = auth_info.get('access_token')
    refresh_token = auth_info.get('refresh_token')
    client_id = auth_info.get('client_id')
    client_secret = auth_info.get('client_secret')
    username = auth_info.get('username')
    password = auth_info.get('password')

    # if True:
    try:
        public_api_obj = MyMall_Public_API(access_token, shopname)

        product_data = dict()
        # Main_Pro_Info = json.loads(pro_obj.MainInfo)
        Variants_info = json.loads(pro_obj.Variants)

        sku_dict = dict()

        product_data['sku'] = Variants_info[0].get('ShopSKU')
        product_data['main_image'] = pro_obj.MainImage
        product_data['name'] = pro_obj.Title
        product_data['description'] = pro_obj.Description
        product_data['tags'] = pro_obj.Tags
        product_data['inventory'] = Variants_info[0].get('Kc')
        product_data['shipping'] = Variants_info[0].get('Shipping')
        product_data['price'] = Variants_info[0].get('Price')
        product_data['extra_images'] = pro_obj.ExtraImages
        product_data['parent_sku'] = Variants_info[0].get('ShopSKU')
        product_data['msrp'] = Variants_info[0].get('Msrp')
        product_data['color'] = Variants_info[0].get('Color')
        product_data['size'] = Variants_info[0].get('Size')
        product_data['shipping_time'] = Variants_info[0].get('Shippingtime')
        sku_dict[Variants_info[0].get('ShopSKU')] = Variants_info[0].get('SKU')

        product_publish_res = pub_mymall_pro(public_api_obj, **product_data)
        if product_publish_res.status_code == 401:
            refresh_token_res = refresh_token_fun(shopname, username, password, client_id, client_secret, refresh_token)
            if refresh_token_res['code'] == 0:
                sRes['code'] = 1
                sRes['message'] = 'The access token provided has expired, But has been refreshed success, Please try again'
                # return sRes
            else:
                sRes['code'] = 2
                sRes['message'] = 'The access token provided has expired, But has been refreshed failed, Please connect with IT'
                # return sRes
        elif product_publish_res.status_code == 200:
            content = json.loads(product_publish_res.content)
            if content['code'] == 0:
                product_id = content['data']['Product']['id']
                sRes['code'] = 0
                sRes['ProductID'] = product_id
                handle_var_res = handle_pub_rvariants_info(Variants_info, sku_dict, product_data, public_api_obj, shopname, auth_info)
                if handle_var_res['code'] != 0:
                    sRes.update(handle_var_res)
                get_product_info_and_update_db(public_api_obj, product_id, shopname, pro_obj, sku_dict, publish_user)
            else:
                sRes['code'] = 3
                sRes['message'] = content
        else:
            sRes['code'] = 4
            sRes['message'] = product_publish_res.content
            content = json.loads(product_publish_res.content)
            if content['code'] == 1004:
                variant_info_res = get_mymall_pro_variant(public_api_obj, **product_data)
                var_content = json.loads(variant_info_res.content)
                sRes['ProductID'] = var_content.get('data').get('Variant').get('product_id')
                product_id = var_content.get('data').get('Variant').get('product_id')

                handle_var_res = handle_pub_rvariants_info(Variants_info, sku_dict, product_data, public_api_obj, shopname, auth_info)
                if handle_var_res['code'] != 0:
                    sRes.update(handle_var_res)
                get_product_info_and_update_db(public_api_obj, product_id, shopname, pro_obj, sku_dict, publish_user)
    except Exception as e:
        sRes['code'] = 5
        sRes['message'] = str(e)

    return sRes


def get_product_info_and_update_db(public_api_obj, product_id, shopname, pro_obj, sku_dict, publish_user):
    product_info_response = get_product_info_by_id(public_api_obj, product_id=product_id)
    if product_info_response.status_code == 200:
        pro_info_content = json.loads(product_info_response.content)
        if pro_info_content['code'] == 0:
            product_info = pro_info_content['data']
            insert_info_mymall_online_info(product_info.get('Product'), shopname, pro_obj.Tags, sku_dict, pro_obj.MainSKU, pro_obj.ExtraImages, publish_user)
        else:
            pass


def handle_pub_rvariants_info(Variants_info, sku_dict, product_data, public_api_obj, shopname, auth_info):
    sRes = {'code': 0, 'message': ''}
    variant_res_list = list()
    for i in range(1, len(Variants_info)):
        sku_dict[Variants_info[i].get('ShopSKU')] = Variants_info[i].get('SKU')
        variant_dict = dict()
        variant_dict['parent_shop_sku'] = product_data['parent_sku']
        variant_dict['shop_sku'] = Variants_info[i].get('ShopSKU')
        variant_dict['inventory'] = Variants_info[i].get('Kc')
        variant_dict['price'] = Variants_info[i].get('Price')
        variant_dict['shipping'] = Variants_info[i].get('Shipping')
        variant_dict['msrp'] = Variants_info[i].get('Msrp')
        variant_dict['main_image'] = Variants_info[i].get('vPic')
        variant_dict['color'] = Variants_info[i].get('Color')
        variant_dict['size'] = Variants_info[i].get('Size')
        variant_publish_res = pub_mymall_pro_variant(public_api_obj, **variant_dict)
        if variant_publish_res.status_code == 401:
            refresh_token_res = refresh_token_fun(shopname, auth_info.get('username'), auth_info.get('password'), auth_info.get('client_id'), auth_info.get('client_secret'), auth_info.get('refresh_token'))
            if refresh_token_res['code'] == 0:
                sRes['code'] = 1
                sRes['message'] = 'Variant publish error The access token provided has expired, But has been refreshed success, ' \
                    'Please unpublish This Product, Then change ShopSKU, Try again to publish.'
            else:
                sRes['code'] = 2
                sRes['message'] = 'Variant publish error The access token provided has expired, But has been refreshed failed, Please connect with IT'
            break
        elif variant_publish_res.status_code != 200:
            variant_res_list.append(variant_publish_res.content)
        # elif variant_publish_res.status_code == 200:
        #     res_content = json.loads(variant_publish_res.content)
        #     if res_content['code'] == 0:
        #         update_var_res = update_mymall_pro_variant(public_api_obj, **variant_dict)
        #         if update_var_res.status_code != 200:
        #             variant_res_list.append(update_var_res.content)

        if variant_res_list:
            sRes['code'] = 5
            sRes['message'] = 'Variant publish error, Please check error message, Then try again, error: %s' % str(variant_res_list)

    return sRes


def get_product_info_by_id(public_api_obj, product_id=None, parent_sku=None):
    res = public_api_obj.product_get(product_id=product_id, parent_sku=parent_sku)
    return res


def insert_info_mymall_online_info(product_info, shopname, tags, product_sku, main_sku, extra_images, publish_user):
    if product_info:
        shopskus = list()
        for i in product_info['variants']:
            shopskus.append(i['Variant']['sku'])
            if i['Variant']['enabled'] == 'True':
                variant_status = '1'
            else:
                variant_status = '0'

            try:
                t_mymall_detail_obj = t_mymall_online_info_detail.objects.get(ProductID=product_info['id'], ShopSKU=i['Variant']['sku'])
                t_mymall_detail_obj.Price = i['Variant']['price']
                t_mymall_detail_obj.Quantity = i['Variant']['inventory']
                t_mymall_detail_obj.Status = variant_status
                t_mymall_detail_obj.Shipping = i['Variant']['shipping']
                t_mymall_detail_obj.ShippingTime = i['Variant']['shipping_time']
                t_mymall_detail_obj.Color = i['Variant']['color']
                t_mymall_detail_obj.Size = i['Variant']['size']
                t_mymall_detail_obj.Msrp = i['Variant']['msrp']
                t_mymall_detail_obj.MainImage = i['Variant']['main_image']
                t_mymall_detail_obj.UpdatedTime = handle_time(i['Variant']['updated_at'])
                t_mymall_detail_obj.save()
            except t_mymall_online_info_detail.DoesNotExist:
                t_mymall_detail_obj = t_mymall_online_info_detail(
                    ProductID=product_info['id'],
                    VariantID=i['Variant']['id'],
                    SKU=product_sku.get(i['Variant']['sku']),
                    MainSKU=main_sku,
                    ShopSKU=i['Variant']['sku'],
                    Price=i['Variant']['price'],
                    Quantity=i['Variant']['inventory'],
                    Status=variant_status,
                    Shipping=i['Variant']['shipping'],
                    ShippingTime=i['Variant']['shipping_time'],
                    Color=i['Variant']['color'],
                    Size=i['Variant']['size'],
                    Msrp=i['Variant']['msrp'],
                    MainImage=i['Variant']['main_image'],
                    UpdatedTime=handle_time(i['Variant']['updated_at']),
                )
                t_mymall_detail_obj.save()

        shopsku_str = ','.join(shopskus)

        if product_info['is_promoted'] == 'True':
            is_promoted = '1'
        else:
            is_promoted = '0'

        if product_info['enabled'] == 'True':
            pro_status = '1'
        else:
            pro_status = '0'

        skus = ','.join(product_sku.values())

        Seller = get_store_config_info(shopname).get('Seller')

        try:
            t_mymall_obj = t_mymall_online_info.objects.get(ProductID=product_info['id'])
            t_mymall_obj.Title = product_info['name']
            t_mymall_obj.SKU = skus
            t_mymall_obj.MainSKU = main_sku
            t_mymall_obj.ShopSKU = shopsku_str
            t_mymall_obj.RefreshTime = datetime.datetime.now()
            t_mymall_obj.DateUploaded = handle_time(product_info['date_uploaded'])
            t_mymall_obj.LastUpdated = handle_time(product_info['last_updated'])
            t_mymall_obj.Tags = tags
            t_mymall_obj.Brand = product_info['brand']
            t_mymall_obj.Description = product_info['description']
            t_mymall_obj.LandingPageUrl = product_info['landing_page_url']
            t_mymall_obj.Upc = product_info['upc']
            t_mymall_obj.Image = product_info['main_image']
            t_mymall_obj.ExtraImages = extra_images
            t_mymall_obj.OriginalImageUrl = product_info['original_image_url']
            t_mymall_obj.IsPromoted = is_promoted
            t_mymall_obj.Status = pro_status
            t_mymall_obj.Published = publish_user
            t_mymall_obj.Seller = Seller
            t_mymall_obj.save()
        except t_mymall_online_info.DoesNotExist:
            t_mymall_obj = t_mymall_online_info(
                ProductID=product_info['id'],
                ShopName=shopname,
                Title=product_info['name'],
                SKU=skus,
                MainSKU=main_sku,
                ShopSKU=shopsku_str,
                RefreshTime=datetime.datetime.now(),
                DateUploaded=handle_time(product_info['date_uploaded']),
                LastUpdated=handle_time(product_info['last_updated']),
                Tags=tags,
                Brand=product_info['brand'],
                Description=product_info['description'],
                LandingPageUrl=product_info['landing_page_url'],
                Upc=product_info['upc'],
                Image=product_info['main_image'],
                ExtraImages=extra_images,
                OriginalImageUrl=product_info['original_image_url'],
                IsPromoted=is_promoted,
                Status=pro_status,
                Published=publish_user,
                Seller=Seller,
            )
            t_mymall_obj.save()


def handle_time(time):
    time = time.split('+')
    date_time = None
    if len(time) > 1:
        try:
            this_time = time[0]
            this_time_diff = int(time[1].split(':')[0]) + 2
            date_time = datetime.datetime.strptime(this_time, '%Y-%m-%dT%H:%M:%S') + datetime.timedelta(hours=this_time_diff)
        except Exception as e:
            print e
            date_time = datetime.datetime.now()
    else:
        date_time = datetime.datetime.now()

    return date_time


def pub_mymall_pro(public_api_obj, **product_data):
    res = public_api_obj.product_add(product_data['sku'], product_data['main_image'], product_data['name'], product_data['description'],
                                     product_data['tags'], product_data['inventory'], product_data['shipping'], product_data['price'],
                                     extra_images=product_data['extra_images'], parent_sku=product_data['parent_sku'], msrp=product_data['msrp'],
                                     color=product_data['color'], size=product_data['size'], shipping_time=product_data['shipping_time'])
    return res


def pub_mymall_pro_variant(public_api_obj, **variant_dict):
    res = public_api_obj.variant_add(variant_dict['parent_shop_sku'], variant_dict['shop_sku'], variant_dict['inventory'], variant_dict['price'],
                                     variant_dict['shipping'], msrp=variant_dict['msrp'], main_image=variant_dict['main_image'], color=variant_dict['color'],
                                     size=variant_dict['size'])

    return res


def get_mymall_pro_variant(public_api_obj, **product_data):
    res = public_api_obj.variant_get(product_data['sku'])
    return res


def update_mymall_pro_variant(public_api_obj, **variant_dict):
    res = public_api_obj.variant_update(variant_dict['shop_sku'], size=variant_dict['size'])

    return res


def get_store_config_info(shopname):
    store_info = dict()
    try:
        store_obj = t_store_configuration_file.objects.get(ShopName__exact=shopname)
        store_info['Seller'] = store_obj.Seller
        store_info['Operators'] = store_obj.Operators
        store_info['Published'] = store_obj.Published
    except t_store_configuration_file.DoesNotExist:
        pass

    return store_info
