#!/usr/bin/python
# coding: utf-8

import json
import time
import os
import sys
import pika
import traceback
import requests
import MySQLdb
import datetime

from ebayTypes import EBayUnissuedItem  # , Pagination, EBayOrder, EBayItemInfo, EBaySummary, Money, Picture
from ebay_api import EBayStoreAPI  # , EBayAPI
from ebay_publish_logger import logger

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


RABBITMQ = {
    # 'hostname': '106.14.125.45',
    'hostname': '127.0.0.1',
    'port': 5672,
    'username': 'admin',
    'password': 'admin',
}

DATABASES = {
    'NAME': 'hq_db',
    'HOST': 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com',
    'USER': 'by15161458383',
    'PASSWORD': 'K120Esc1',
    'PORT': '3306',
}

LOCALPATH = '/opt/hq-project/ebay/pic/'

appinfos_1 = {
    'appid': 'woodspid-MyStoreM-PRD-3c6c7072b-93250daa',
    'devid': '2431472d-fcbf-4688-af0e-29c65fdf6737',
    'certid': 'PRD-c6c7072be76d-25b6-4e63-bb08-706d',
    'runame': 'woodspider_liuj-woodspid-MyStor-lemookxm'
}

sandbox_stoken = 'AgAAAA**AQAAAA**aAAAAA**5pUnWg**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wFk4GkD5OKqAWdj6x9nY+seQ**C0sEAA**AAMAAA**XkN+3LTbwCXkwRMx+7qXq3WY31Y6kDppqQzrSjcMJ44izbkeoXpmP7tQoXZKRNBjGp0g76qVN3vmvbUbJH7XeZ1+jCBfdOoDGS7pJX/AG97uxSZC1Nenlwe+zln96bnPcrgSt3OctvntIM6FXRJFwtX2xRkVdzqMgiYD2GthVQbHNWkvVn5ph1PmrGIlp0r2PmlByNuZrfT2f5HS9xD1oIaAP4FRI7HvPQwPnskBgWVU2vJFGMt9licHqDox4QoLq1EE8oYw7AxtXBDFkkXOab6362tB+DPhwl7YpRJytrfwTyX7/s7Q9hOzh4URoJ1TwtF9dmYZaRcIZ1iMO9Bwq/V2zH4y6tmW96P50ez/+99L2fL5dTfvtETmx4/qTNc2CZzt8x9y1B3rEqIfpYL+DcPO1/p4XS5N5vyOlXN4UJ9vOatMH62ODEsN8O83kwrT7t7B6l3hKlE6JW0uaK5YZW/AB6BJcd/I1ZjOkMWRWh3Hv1xIePivgeoVO00MfffAQb8OZxTMdEXHEO6aa4Uy/t3rd4r11aciJr4kIhP8LhFZnBTT5RBJxTZ0aQ+IaEHHiVVdfBB60rsO1PKFca/dQftTspyDMMbsA10fKtI0f8GX/l20v5GzDyKuPXHDz1OTkOb6x7ALe4XRZTXyfhSw89eD4CkiFhZ8/H4FA5mEr8/8r8x6ebpKhg/iGJWhjfvkLS87mST3QNxt6sNCXw7PZyJEjCELJDTCDxKAqphGyz5V4dDUxNqdMcrS0URx4VYN'


class Server():

    def __init__(self):
        credentials = pika.PlainCredentials(RABBITMQ['username'], RABBITMQ['password'])
        self.parameters = pika.ConnectionParameters(RABBITMQ['hostname'],
                                                    RABBITMQ['port'],
                                                    '/',
                                                    credentials,
                                                    blocked_connection_timeout=36000,
                                                    socket_timeout=36000,
                                                    heartbeat=36000)
        self.connection = pika.BlockingConnection(self.parameters)

    def listen_client(self):
        channel = self.connection.channel()
        queue = 'ebay_publish_product'
        channel.queue_declare(queue=queue)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(self.callback, queue=queue, no_ack=True)
        channel.start_consuming()

    def callback(self, ch, method, properties, body):
        logger.debug("[x] Received %r" % (body,))
        '''
            body = [
                {
                    'uploadtaskid': '$id',
                    'shopname': '$shopname',
                    'title': '',
                    'product_sku': '$product_sku',
                    'shopsku': '$shopsku',
                    'time': '120',
                    'Site' : '$Site'
                },
            ]
        '''
        datas = json.loads(body)
        main_images = dict()
        var_images = dict()
        count_tag = 0

        try:
            db_conn = MySQLdb.connect(DATABASES['HOST'], DATABASES['USER'], DATABASES['PASSWORD'], DATABASES['NAME'], charset="utf8")
        except Exception as e:
            error = 'Connect mysql db error %s' % e
            logger.error(error)
            return None

        for data in datas:
            # product_sku = data.get('product_sku')
            # shopsku = data.get('shopsku')
            shopname = data.get('shopname')
            uploadtaskid = data.get('uploadtaskid')
            result_id = data.get('result_id')
            wait_time = int(data.get('time'))
            title = data.get('title')
            Site = data.get('Site')

            if not count_tag == 0:
                time.sleep(wait_time)
            else:
                count_tag = 1

            sku_dict = data.get('sku_dict', {})
            '''
            sku_dict = dict()
            num = 0
            for i in product_sku:
                sku_dict[i] = str(shopsku[num])
                num += 1
            '''

            auth_info = self.get_auth_info(shopname, Site, db_conn)
            if not auth_info:
                error = 'Can not get auth info for shopname: %s' % shopname
                logger.error(error)
                self.execute_error_mess(result_id, shopname, error, db_conn)
                return
            logger.debug('auth_info: ', auth_info)
            appinfos = dict()
            appinfos['appid'] = auth_info[shopname]['appID']
            appinfos['devid'] = auth_info[shopname]['deviceID']
            appinfos['certid'] = auth_info[shopname]['certID']
            appinfos['runame'] = auth_info[shopname]['runame']
            appinfos['runip'] = auth_info[shopname]['runip']
            token = auth_info[shopname]['token']
            auth_info[shopname]['title'] = title

            # seller = auth_info[shopname]['storeOwner']
            # ExcelFile = product_info['ExcelFile']

            # TO DEFINE EBAY API
            try:
                # api = EBayStoreAPI(appinfos, token, siteID=auth_info[shopname]['siteID'])
                api = EBayStoreAPI(appinfos, token, siteID=Site)
            except Exception as e:
                error = 'Define ebay store api error: %s' % e
                error = self.clear_string(error)
                logger.error(error)
                self.execute_error_mess(result_id, shopname, error, db_conn)
                return
            # api = EBayStoreAPI(appinfos_1, sandbox_stoken)

            # TO GET PRODUCT INFO
            product_info = self.get_product_info(uploadtaskid, auth_info[shopname], db_conn)
            if not product_info:
                error = 'Can not get product info, uploadtaskid: %s, shopname: %s' % (uploadtaskid, shopname)
                logger.error(error)
                self.execute_error_mess(result_id, shopname, error, db_conn)
                return

            # GET IMAGES URL
            images_url = []
            images_url = product_info['Images']
            if not main_images:
                images_url = images_url.split(',')
                main_images = self.get_images(images_url)
                if not main_images:
                    error = 'Can not get main images'
                    return
            logger.debug('main_images: %s' % main_images)

            # UPLOAD ALL IMAGES
            main_pic_url = self.upload_image(main_images, api).values()
            if not main_pic_url or len(main_images) != len(main_pic_url):
                retry_result = 0
                for i in range(3):
                    time.sleep(5)
                    main_pic_url_retry = self.upload_image(main_images, api).values()
                    if not main_pic_url_retry or not len(main_images) == len(main_pic_url_retry):
                        if i == 2:
                            error = 'Upload image all failed'
                            print(error)
                            logger.error(error)
                            self.execute_error_mess(result_id, shopname, error, db_conn)
                            break
                        else:
                            continue
                    elif len(main_images) == len(main_pic_url_retry):
                        main_pic_url = main_pic_url_retry
                        retry_result = 1
                        break
                if not retry_result:
                    return

            # UPDATE PRODUCT VARIATION INFO
            if product_info['Variation']:
                product_info, var_images = self.update_product_info(product_info, sku_dict, api, var_images=var_images)
                if product_info.get('error'):
                    error = 'product info update error: %s' % product_info.get('error')
                    logger.error(error)
                    self.execute_error_mess(result_id, shopname, error, db_conn)
                    return

            product_info['shop_site'] = Site

            logger.debug('product_info: %s' % product_info)
            logger.debug('var_images: %s' % var_images)

            # GET EBAY ITEM OBJECT
            auth_info['shopsku'] = sku_dict
            ebay_item = self.get_ebay_item(product_info, main_pic_url, auth_info, shopname)
            logger.debug('ebay_item: %s' % ebay_item)

            # PUBLISH EBAY PRODUCT AND RETURN RESULT TO DB
            if isinstance(ebay_item, dict) and ebay_item.get('error'):
                error = ebay_item.get('error')
                logger.error(error)
                self.execute_error_mess(result_id, shopname, error, db_conn)
                result = None
            else:
                try:
                    result = api.publishItem(ebay_item)
                except Exception as e:
                    error = 'Api Publish Item Error: %s' % e
                    error = self.clear_string(error)
                    logger.error(error)
                    self.execute_error_mess(result_id, shopname, error, db_conn)
                    result = None
            logger.debug(result)
            if hasattr(result, 'itemid') and result.itemid:
                msg = 'publish item success, itme id : %s' % result.itemid
                logger.debug(msg)
                sql = "update t_templet_ebay_upload_result set Status='SUCCESS', ErrorMessage='%s' where id='%s' and ShopName='%s';" % (msg, result_id, shopname)
                self.execute_db(sql, db_conn)

                '''
                for k, v in sku_dict.items():
                    insert_sql = "insert into t_shopsku_information_binding " \
                                 "(SKU,ShopSKU,Memo,PersonCode,Filename,SubmitTime,BindingStatus) " \
                                 "values ('%s','%s','%s','%s','%s','%s','wait')" % (k, v, shopname, seller, ExcelFile, datetime.datetime.now())
                    logger.debug('Insert into t_shopsku_information_binding: \n%s' % insert_sql)
                    self.execute_db(insert_sql, db_conn)
                '''

            elif hasattr(result, 'errors') and result.errors:
                logger.debug('publish item failed')
                LongMessage = result.LongMessage
                LongMessage = self.clear_string(LongMessage)
                ShortMessage = result.ShortMessage
                ShortMessage = self.clear_string(ShortMessage)
                error = 'Publish ebay item failed, Error ShortMessage: %s, Error LongMessage: %s, ErrorClassification: %s' % (ShortMessage, LongMessage, result.ErrorClassification)
                self.execute_error_mess(result_id, shopname, error, db_conn)
            # else:
            #    logger.debug('publish item failed')
            #    error = 'Publish ebay item failed, Return result does not have itemid and error messages'
            #    self.execute_error_mess(result_id, shopname, error, db_conn)

        # TO REMOVE LOCAL IMAGES
        logger.debug('Start to remove local images')
        self.remove_local_image(main_images)
        self.remove_local_image(var_images)
        logger.debug('End to remove local images')
        db_conn.close()

    def clear_string(self, msg):
        '''
        To clear exception error message for writting to db.
        '''
        clear_msg = msg.split()
        clear_msg = ' '.join(clear_msg)
        clear_msg = clear_msg.replace('\"', '\\\"')
        clear_msg = clear_msg.replace('\'', '\\\'')
        return clear_msg

    def get_auth_info(self, shopname, Site, db_conn):
        '''
        Select store ebay info;
        Select developer ebay info;
        Select config site ebay;
        '''
        sql = "select storeName, appID, token, paypalAccountLarge, paypalAccountHalf, description_prefix_file, description_postfox_file, siteID, storeOwner from t_config_store_ebay where storeName='%s';" % shopname
        store_info = self.get_db_info(sql, db_conn)
        if not store_info:
            logger.error('Can not get config store ebay info for shopname: %s, sql: %s' % (shopname, sql))
            return None
        store_dict = dict()
        appids = []
        for i in store_info:
            if i.get('siteID'):
                i['siteID'] = Site
            store_dict[i['storeName']] = i
            if i['appID'] not in appids:
                appids.append(json.dumps(i['appID']))

        appids = ', '.join(appids)
        sql = "select appID, deviceID, certID, runame, runIP from t_developer_info_ebay where appID in (%s)" % appids
        auth_info = self.get_db_info(sql, db_conn)
        if not auth_info:
            logger.error('Can not get developer ebay info for shopname: %s, appids: %s, sql: %s' % (shopname, appids, sql))
            return None
        auth_dict = dict()
        for i in auth_info:
            auth_dict[i['appID']] = i

        logger.debug('auth_dict: %s' % auth_dict)

        for i in store_dict:
            store_dict[i]['deviceID'] = auth_dict[store_dict[i]['appID']]['deviceID']
            store_dict[i]['certID'] = auth_dict[store_dict[i]['appID']]['certID']
            store_dict[i]['runame'] = auth_dict[store_dict[i]['appID']]['runame']
            store_dict[i]['runip'] = auth_dict[store_dict[i]['appID']]['runIP']

        sql = 'select siteID, dispatchTimeMax, siteCurrency from t_config_site_ebay'
        site_info = self.get_db_info(sql, db_conn)
        if not site_info:
            logger.error('Can not get config site ebay info, sql: %s' % sql)
            return None
        site_dict = dict()
        for i in site_info:
            site_dict[i['siteID']] = i['dispatchTimeMax']

        for i in store_dict:
            store_dict[i]['dispatchTimeMax'] = site_dict[store_dict[i]['siteID']]

        c_dict = dict()
        for i in site_info:
            c_dict[i['siteID']] = i['siteCurrency']

        for i in store_dict:
            store_dict[i]['siteCurrency'] = c_dict[store_dict[i]['siteID']]

        return store_dict

    def get_product_info(self, uploadtaskid, auth_info, db_conn):
        sql = "select * from t_templet_ebay_wait_upload where id='%s'" % uploadtaskid
        product_info = self.get_db_info(sql, db_conn)
        if not product_info:
            logger.error('Can not get template ebay upload info for uploadtaskid: %s, sql: %s' % (uploadtaskid, sql))

        sql = "select * from t_config_ebay_ext where attrName='thresholdOfPaypalChoice';"
        ebay_conf = self.get_db_info(sql, db_conn)
        if not ebay_conf:
            logger.error('Can not get config ebay ext info, sql: %s' % sql)

        if product_info and ebay_conf:
            price = product_info[0]['BuyItNowPrice']
            currency = auth_info['siteCurrency']
            attrValue = eval(ebay_conf[0]['attrValue'])
            if attrValue[currency] > price:
                useemail = 'large'
            else:
                useemail = 'half'
            product_info[0]['useemail'] = useemail
        else:
            return None

        description = product_info[0]['Description']
        description = description.replace('https', 'http')
        description = description.replace('http', 'https')
        product_info[0]['Description'] = description

        return product_info[0]

    def update_product_info(self, product_info, sku_dict, api, var_images=None):
        # Update product sku to shop sku
        variation = eval(product_info['Variation'])
        logger.debug('variation: %s' % variation)
        for i in variation['Variation']:
            if sku_dict.get(i['SKU']):
                i['SKU'] = sku_dict.get(i['SKU'])
            else:
                product_info = {'error': 'variation product sku does not compare with rabbitmq message product sku'}
                return product_info, var_images
        product_info['Variation'] = str(variation)
        logger.debug("product_info['Variation']: %s" % product_info['Variation'])

        # Get image
        variation = eval(product_info['Variation'])
        pics = variation['Pictures']
        if not var_images:
            pic_url = []
            for i in pics:
                for j in i['VariationSpecificPictureSet']['PictureURL']:
                    pic_url.append(j)
            var_images = self.get_images(pic_url)

        var_remote_img = self.upload_image(var_images, api)
        for i in pics:
            p_c_u = i['VariationSpecificPictureSet']['PictureURL']
            p_c_u_c = []
            for j in p_c_u:
                if var_remote_img.get(j):
                    p_c_u_c.append(var_remote_img.get(j))
            i['VariationSpecificPictureSet']['PictureURL'] = []
            i['VariationSpecificPictureSet']['PictureURL'] = p_c_u_c

        variation['Pictures'] = pics
        product_info['Variation'] = str(variation)

        return product_info, var_images

    def upload_image(self, images, api):
        pic_url = dict()
        for i in images:
            logger.debug('start time: %s' % datetime.datetime.now())
            logger.debug('send image info: %s' % images[i])
            try:
                pics = api.uploadImgBin(images[i])
            except Exception as e:
                logger.error('api UploadImgBin error: %s' % e)
                pics = None
            logger.debug('end time: %s' % datetime.datetime.now())
            logger.debug('send image result: %s' % pics)
            if not pics:
                logger.error('Upload image error, image url: %s, image local file: %s' % (i, images[i]))
                continue
            pic_size = i.split('$_')[-1].split('.')[0]
            for pic in pics:
                logger.debug('pic url ------- %s' % pic.url)
                pic_res_img = pic.url.split('$_')[-1].split('.')[0]
                if pic_res_img == pic_size:
                    pic_url[i] = pic.url
                    continue
        logger.debug('UploadImgBin pics: %s' % pic_url)
        return pic_url

    def get_ebay_item(self, product_info, images, auth_info, shopname):
        item = EBayUnissuedItem()
        item.returnPolicy.description = product_info['Description']
        if str(auth_info[shopname]['siteID']) == '2':
            item.returnPolicy.refundOption = None
        else:
            item.returnPolicy.refundOption = product_info.get('RefundOptions', '')
        item.pictureDetail = images
        title = auth_info.get(shopname).get('title') or product_info['Title']
        title = title.replace('&', '')
        item.title = title

        if product_info['useemail'] == 'large':
            item.payPalEmailAddress = auth_info.get(shopname).get('paypalAccountLarge') or ''
        elif product_info['useemail'] == 'half':
            item.payPalEmailAddress = auth_info.get(shopname).get('paypalAccountHalf') or ''
        else:
            item.payPalEmailAddress = ''

        ship_key = {
            'shipping_key_1': 'ShippingService',
            'shipping_key_2': 'ShippingServiceCost',
            'shipping_key_3': 'ShippingServiceAdditionalCost',
        }
        for i in range(4):
            ship_ser = product_info[ship_key['shipping_key_1'] + str(i + 1)]
            freeship = product_info[ship_key['shipping_key_2'] + str(i + 1)]
            shippingCost = freeship
            shippingAdditionalCost = product_info[ship_key['shipping_key_3'] + str(i + 1)]
            if not shippingCost or float(freeship) == 0.0:
                freeship = 'true'
            elif float(freeship) > 0.0:
                freeship = ''
            else:
                freeship = 'true'

            if ship_ser and freeship:
                shippingServiceOption = EBayUnissuedItem.ShippingDetails.ShippingServiceOptions()
                shippingServiceOption.shippingService = ship_ser
                shippingServiceOption.freeShipping = freeship
                shippingServiceOption.shippingServicePriority = i + 1
                item.shippingDetails.shippingServiceOptions.append(shippingServiceOption)
            elif ship_ser:
                shippingServiceOption = EBayUnissuedItem.ShippingDetails.ShippingServiceOptions()
                shippingServiceOption.shippingService = ship_ser
                shippingServiceOption.shippingServiceCost = shippingCost
                shippingServiceOption.freeShipping = 'false'
                shippingServiceOption.shippingServiceAdditionalCost = shippingAdditionalCost
                shippingServiceOption.shippingServicePriority = i + 1
                item.shippingDetails.shippingServiceOptions.append(shippingServiceOption)

        item.shippingDetails.globalShipping = 'false'

        inter_ship_key = {
            'inter_shipping_key_1': 'InternationalShippingService',
            'inter_shipping_key_2': 'InternationalShippingServiceCost',
            'inter_shipping_key_3': 'InternationalShippingServiceAdditionalCost',
            'inter_shipping_key_4': 'InternationalShipToLocation',
        }

        for i in range(5):
            service = product_info[inter_ship_key['inter_shipping_key_1'] + str(i + 1)]
            servicecost = product_info[inter_ship_key['inter_shipping_key_2'] + str(i + 1)]
            serviceaddicost = product_info[inter_ship_key['inter_shipping_key_3'] + str(i + 1)]
            location = product_info[inter_ship_key['inter_shipping_key_4'] + str(i + 1)]
            if service and servicecost and serviceaddicost and location:
                internationalShippingServiceOption = EBayUnissuedItem.ShippingDetails.ShippingServiceOptions()
                internationalShippingServiceOption.shippingService = service
                internationalShippingServiceOption.shippingServicePriority = i + 1
                internationalShippingServiceOption.shippingServiceCost = servicecost
                internationalShippingServiceOption.shippingServiceAdditionalCost = serviceaddicost
                internationalShippingServiceOption.shipToLocations = location
                item.shippingDetails.internationalShippingServiceOptions.append(internationalShippingServiceOption)
        item.shippingDetails.excludeShipToLocation = product_info['ExcludeShipToLocation']

        # TODO auth_info description_prefix_file, description_postfox_file
        item.description = product_info['Description']

        item.dispatchTimeMax = auth_info.get(shopname).get('dispatchTimeMax') or 2

        item.quantity = product_info['Quantity']
        item.primaryCategory = product_info['Category1']
        item.conditionID = product_info['Condition']
        item.startPrice = product_info['StartPrice']
        item.listingDuration = product_info['Duration']
        item.paymentMethods = product_info['AcceptPayment']
        item.location = product_info['Location']
        item.country = product_info['LocationCountry']
        item.galleryType = product_info['GalleryType']
        item.hitCounter = product_info['HitCounter']
        item.EAN = product_info['EAN']

        item.currency = auth_info.get(shopname).get('siteCurrency')

        logger.debug('item.currency \n%s' % item.currency)

        key = 'Specifics'
        spe_dict = dict()
        for i in range(30):
            spe = product_info[key + str(i + 1)]
            logger.debug('%s, %s' % ((key + str(i + 1)), spe))
            if spe:
                spe = str(spe)
                spe = spe.split(':')
                if spe[0] not in spe_dict.keys():
                    spe_dict[spe[0]] = list()
                spe_dict[spe[0]].append(spe[1].replace('&', ''))

        if len(auth_info['shopsku'].keys()) < 2:
            item.itemSpecifics = spe_dict
            logger.debug('itemSpecifics: %s' % spe_dict)
            for i in auth_info['shopsku']:
                item.SKU = auth_info['shopsku'][i]
                break
        else:
            if str(auth_info[shopname]['siteID']) in ['2', '3', '15']:
                var_item_spe = dict()
                var_item_spe['MPN'] = spe_dict.get('MPN', 'Does Not Apply')
                var_item_spe['Brand'] = spe_dict.get('Brand', 'Unbranded')
                if str(auth_info[shopname]['siteID']) == '15':
                    var_item_spe['UPC'] = spe_dict.get('UPC', 'Does Not Apply')
                item.itemSpecifics = var_item_spe
            else:
                item.itemSpecifics = spe_dict

            item.SKU = ''
            variationdict = eval(product_info['Variation'])
            VariationSpecificsSet = variationdict['VariationSpecificsSet']
            for i in VariationSpecificsSet['NameValueList']:
                if i['Name'] not in ['ISBN', 'UPC', 'EAN']:
                    vss_key = i['Name']
                    vss_value = i['Value']
                    if isinstance(vss_value, list):
                        item.variationSpecificsSet[vss_key] = vss_value
                    elif isinstance(vss_value, dict):
                        item.variationSpecificsSet[vss_key] = vss_value.values()
                    elif isinstance(vss_value, str):
                        item.variationSpecificsSet[vss_key] = vss_value.split(',')
                    else:
                        continue

            item.variationSpecificName = variationdict.get('assoc_pic_key')
            variations = variationdict.get('Variation')
            pics = variationdict.get('Pictures', [])

            for i in range(0, len(variations)):
                variation = EBayUnissuedItem.Variation()
                variation.startPrice = variations[i].get('StartPrice')
                variation.SKU = variations[i].get('SKU')
                nameValueList = variations[i].get('VariationSpecifics').get("NameValueList")
                for j in range(0, len(nameValueList)):
                    name = nameValueList[j].get('Name')
                    if name == 'UPC':
                        variation.UPC = nameValueList[j].get('Value')
                    elif name == 'EAN':
                        variation.EAN = nameValueList[j].get('Value')
                    elif name == 'ISBN':
                        pass
                    else:
                        variation.variationSpecifics[name] = nameValueList[j].get('Value')
                variation.quantity = variations[i].get('Quantity')
                item.variations.append(variation)

            for pic in pics:
                if pic is not None and isinstance(pic, dict) and item.variationSpecificName:
                    if pic.get('Value') not in item.variationSpecificsSet.get(item.variationSpecificName):
                        continue
                    item.variationSpecificPictureSets[pic.get('Value')] = pic.get('VariationSpecificPictureSet').get('PictureURL')
                    pass

            if auth_info[shopname]['siteID'] == 71 and item.variations is not None and len(item.variations) > 0:
                if item.itemSpecifics:
                    if 'Color' in item.itemSpecifics.kyes():
                        item.itemSpecifics.pop('Color')
                else:
                    pass
        return item

    def get_db_info(self, sql, db_conn):
        logger.debug('execute sql: \n%s' % sql)
        cursor = db_conn.cursor()
        cursor.execute(sql)
        columns = cursor.description
        result = []
        for value in cursor.fetchall():
            tmp = {}
            for (index, column) in enumerate(value):
                tmp[columns[index][0]] = column
            result.append(tmp)
        cursor.close()
        return result

    def execute_error_mess(self, result_id, shopname, error, db_conn):
        sql = "update t_templet_ebay_upload_result set Status='FAILED', ErrorMessage='%s' where id='%s' and ShopName='%s';" % (error, result_id, shopname)
        self.execute_db(sql, db_conn)

    def execute_db(self, sql, db_conn):
        try:
            cursor = db_conn.cursor()
            cursor.execute(sql)
            cursor.execute('commit;')
            cursor.close()
        except Exception as e:
            logger.error('Update product info faild, Execute sql: %s, Error info: %s' % (sql, e))

    def get_images(self, images_url):
        image_dict = dict()

        for img in images_url:
            try:
                i = img.replace('\\', '')
                r = requests.get(i, allow_redirects=True)
                filename = i.split('/')
                filename = filename[-2] + filename[-1].split('?')[0]
                local_file = LOCALPATH + filename
                open(local_file, 'wb').write(r.content)
                image_dict[img] = local_file
            except Exception as e:
                logger.error('Get image from ebay error: %s' % e)
                continue

        return image_dict

    def remove_local_image(self, images):
        for i in images:
            try:
                os.remove(images[i])
            except Exception as e:
                logger.error('remove image failed: %s' % e)
                continue


def retry_server():
    try:
        c = Server()
        c.listen_client()
    except Exception as e:
        logger.error('Define server error: %s' % repr(e))
        logger.error('traceback.format_exc():\n%s' % traceback.format_exc())
        time.sleep(5)
        retry_server()


if __name__ == '__main__':

    logger.debug('[x] start ebay product')
    # c = Server()
    # c.listen_client()
    retry_server()
