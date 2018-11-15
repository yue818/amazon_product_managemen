# -*- coding: utf-8 -*-

"""
 @desc:
 @author: 孙健
 @site:
"""

import datetime
import logging

from django.db import connection
from django.db.models import Q

from brick.ebay.api.utils import ObjectDict
from brick.ebay.api.eBay_Public_API import eBayAPI
from skuapp.table.t_config_store_ebay import t_config_store_ebay
from ebayapp.table.t_config_site_ebay import t_config_site_ebay
from ebayapp.table.t_developer_info_ebay import t_developer_info_ebay

logger = logging.getLogger('django.brick.ebay.ebay_publish')


def handle_description(description):
    html_des = str()
    if description:
        descriptions = description.split('<!--[Datacaciques code start')
        for i in descriptions:
            if i and not i.endswith('<!--[Datacaciques code end]-->'):
                if i.find('<!--[Datacaciques code end]-->'):
                    html_des += i.split('<!--[Datacaciques code end]-->')[-1]
                else:
                    html_des += i
            else:
                continue
        html_des = html_des.replace('\n', '').replace('\t', '')
    return html_des


def handle_variations(variations):
    variation_data = dict()
    if variations:
        Variation = variations.get('Variation')
        VariationSpecificsSet = variations.get('VariationSpecificsSet')
        VariationSpecificPictureSet = variations.get('Pictures', {}).get('VariationSpecificPictureSet')

        assoc_pic_key = variations.get('Pictures', {}).get('VariationSpecificName', {}).get('value')

        assoc_pic_count = 0
        if type(VariationSpecificPictureSet) is list:
            assoc_pic_count = len(VariationSpecificPictureSet)
        elif type(VariationSpecificPictureSet) is ObjectDict:
            assoc_pic_count = 1
        else:
            pass

        variation_data['Variation'] = handle_variations_var(Variation)
        variation_data['Pictures'] = handle_variations_pic(VariationSpecificPictureSet)
        variation_data['VariationSpecificsSet'] = handle_variations_varspeset(VariationSpecificsSet)
        variation_data['assoc_pic_key'] = assoc_pic_key
        variation_data['assoc_pic_count'] = assoc_pic_count

    if not variation_data:
        variation_data = None

    return variation_data


def handle_variations_var(Variation):
    variations_list = list()
    if Variation:
        if type(Variation) is list:
            for i in Variation:
                variations_dict = dict()
                variations_dict['SKU'] = i.get('SKU', {}).get('value')
                variations_dict['StartPrice'] = i.get('StartPrice', {}).get('value')
                variations_dict['SellingStatus'] = dict()
                variations_dict['SellingStatus']['QuantitySold'] = i.get('SellingStatus', {}).get('QuantitySold', {}).get('value')
                variations_dict['Quantity'] = i.get('Quantity', {}).get('value')
                variations_dict['VariationSpecifics'] = dict()
                variations_dict['VariationSpecifics']['NameValueList'] = list()
                NameValueList = i.get('VariationSpecifics', {}).get('NameValueList')
                if type(NameValueList) is list:
                    for j in NameValueList:
                        kv = dict()
                        kv['Name'] = j.get('Name', {}).get('value')
                        kv['Value'] = j.get('Value', {}).get('value')
                        variations_dict['VariationSpecifics']['NameValueList'].append(kv)
                elif type(NameValueList) is ObjectDict:
                    kv = dict()
                    kv['Name'] = NameValueList.get('Name', {}).get('value')
                    kv['Value'] = NameValueList.get('Value', {}).get('value')
                    variations_dict['VariationSpecifics']['NameValueList'].append(kv)
                variations_list.append(variations_dict)
        elif type(Variation) is ObjectDict:
            variations_dict = dict()
            variations_dict['SKU'] = Variation.get('SKU', {}).get('value')
            variations_dict['StartPrice'] = Variation.get('StartPrice', {}).get('value')
            variations_dict['SellingStatus'] = dict()
            variations_dict['SellingStatus']['QuantitySold'] = Variation.get('SellingStatus', {}).get('QuantitySold', {}).get('value')
            variations_dict['Quantity'] = Variation.get('Quantity', {}).get('value')
            variations_dict['VariationSpecifics'] = dict()
            variations_dict['VariationSpecifics']['NameValueList'] = list()
            NameValueList = Variation.get('VariationSpecifics', {}).get('NameValueList')
            if type(NameValueList) is list:
                for j in NameValueList:
                    kv = dict()
                    kv['Name'] = j.get('Name', {}).get('value')
                    kv['Value'] = j.get('Value', {}).get('value')
                    variations_dict['VariationSpecifics']['NameValueList'].append(kv)
            elif type(NameValueList) is ObjectDict:
                kv = dict()
                kv['Name'] = NameValueList.get('Name', {}).get('value')
                kv['Value'] = NameValueList.get('Value', {}).get('value')
                variations_dict['VariationSpecifics']['NameValueList'].append(kv)
            variations_list.append(variations_dict)
        else:
            pass

    return variations_list


def handle_variations_pic(VariationSpecificPictureSet):
    pic_list = list()
    if VariationSpecificPictureSet:
        if type(VariationSpecificPictureSet) is list:
            for i in VariationSpecificPictureSet:
                vsps = dict()
                vsps['VariationSpecificPictureSet'] = dict()
                vsps['VariationSpecificPictureSet']['PictureURL'] = list()
                vsps['Value'] = dict()
                PictureURL = i.get('PictureURL')
                pics = list()
                if PictureURL:
                    if type(PictureURL) is ObjectDict:
                        pics.append(PictureURL.get('value', ''))
                    elif type(PictureURL) is list:
                        for pic_j in PictureURL:
                            pics.append(pic_j.get('value', ''))
                vsps['VariationSpecificPictureSet']['PictureURL'] = pics
                vsps['Value'] = i.get('VariationSpecificValue', {}).get('value')
                pic_list.append(vsps)
        elif type(VariationSpecificPictureSet) is ObjectDict:
            vsps = dict()
            vsps['VariationSpecificPictureSet'] = dict()
            vsps['VariationSpecificPictureSet']['PictureURL'] = list()
            vsps['Value'] = dict()
            PictureURL = VariationSpecificPictureSet.get('PictureURL')
            pics = list()
            if PictureURL:
                if type(PictureURL) is ObjectDict:
                    pics.append(PictureURL.get('value', ''))
                elif type(PictureURL) is list:
                    for i in PictureURL:
                        pics.append(i.get('value', ''))
            vsps['VariationSpecificPictureSet']['PictureURL'] = pics
            vsps['Value'] = VariationSpecificPictureSet.get('VariationSpecificValue', {}).get('value')
            pic_list.append(vsps)
        else:
            pass

    return pic_list


def handle_variations_varspeset(VariationSpecificsSet):
    vss = dict()
    vss['NameValueList'] = list()
    if VariationSpecificsSet:
        NameValueList = VariationSpecificsSet.get('NameValueList')
        if type(NameValueList) is list:
            for i in NameValueList:
                kv = dict()
                kv['Name'] = i.get('Name', {}).get('value')
                kv['Value'] = list()
                if type(i.get('Value')) is list:
                    for j in i.get('Value'):
                        kv['Value'].append(j.get('value'))
                elif type(i.get('Value')) is ObjectDict:
                    kv['Value'].append(i.get('Value', {}).get('value'))
                else:
                    pass
                vss['NameValueList'].append(kv)
        elif type(NameValueList) is ObjectDict:
            kv = dict()
            kv['Name'] = NameValueList.get('Name', {}).get('value')
            kv['Value'] = list()
            if type(NameValueList.get('Value')) is list:
                for j in NameValueList.get('Value'):
                    kv['Value'].append(j.get('value'))
            elif type(NameValueList.get('Value')) is ObjectDict:
                kv['Value'].append(NameValueList.get('Value', {}).get('value'))
            else:
                pass
            vss['NameValueList'].append(kv)

    return vss


def handle_specifics(NameValueList):
    NameValueList_dict = dict()
    if type(NameValueList) is list:
        for i in NameValueList:
            name = i.get('Name').get('value')
            value = i.get('Value')
            NameValueList_dict[name] = list()
            if type(value) is list:
                for j in value:
                    NameValueList_dict[name].append(j.get('value'))
            elif type(value) is ObjectDict:
                NameValueList_dict[name].append(value.get('value'))
            else:
                pass
    elif type(NameValueList) is ObjectDict:
        name = NameValueList.get('Name').get('value')
        value = NameValueList.get('Value')
        NameValueList_dict[name] = list()
        if type(value) is list:
            for j in value:
                NameValueList_dict[name].append(j.get('value'))
        elif type(value) is ObjectDict:
            NameValueList_dict[name].append(value.get('value'))
        else:
            pass
    else:
        pass

    nv_list = list()
    if NameValueList_dict:
        for i in NameValueList_dict.keys():
            for j in NameValueList_dict[i]:
                key_value = i + ':' + j
                nv_list.append(key_value)

    if 'Brand' not in NameValueList_dict.keys():
        key_value = 'Brand:Unbranded'
        nv_list.append(key_value)
    if 'MPN' not in NameValueList_dict.keys():
        key_value = 'MPN:Does Not Apply'
        nv_list.append(key_value)

    return nv_list


def handle_images(images):
    pics = list()
    if images:
        if type(images) is list:
            for i in images:
                if i.get('value'):
                    pics.append(i.get('value'))
        elif type(images) is ObjectDict:
            pics.append(images.get('value'))
        else:
            pass
    image_str = str()
    if pics:
        image_str = ','.join(pics)

    return image_str


def handle_ExcludeShipToLocation(ExcludeShipToLocation):
    ExcludeShipToLocation_str = str()
    ExcludeShipToLocation_list = list()
    if ExcludeShipToLocation:
        if type(ExcludeShipToLocation) is list:
            for i in ExcludeShipToLocation:
                ExcludeShipToLocation_list.append(i.get('value'))
        elif type(ExcludeShipToLocation) is ObjectDict:
            ExcludeShipToLocation_list.append(ExcludeShipToLocation.get('value'))
        else:
            pass
    ExcludeShipToLocation_str = ','.join(ExcludeShipToLocation_list)

    return ExcludeShipToLocation_str


def get_site_id(sitename):
    site_id = None
    if sitename:
        try:
            site_id = t_config_site_ebay.objects.get(Q(siteDescription=sitename) | Q(siteName=sitename)).siteID
        except t_config_site_ebay.DoesNotExist:
            pass
    return site_id


def ebay_get_item_response(shopname, itemid):
    store_info = t_config_store_ebay.objects.get(storeName=shopname)
    developer_info = t_developer_info_ebay.objects.get(appID=store_info.appID)
    appinfo = dict()
    appinfo['appID'] = developer_info.appID
    appinfo['deviceID'] = developer_info.deviceID
    appinfo['certID'] = developer_info.certID
    appinfo['runame'] = developer_info.runame
    appinfo['runIP'] = developer_info.runIP
    storeinfo = dict()
    storeinfo['siteID'] = str(store_info.siteID)
    storeinfo['token'] = store_info.token
    ebay_obj = eBayAPI(appinfo, storeinfo)
    response = ebay_obj.GetItem(ItemID=itemid)
    return response


def ebay_get_item_info(ebayInfo):
    ebay_data = dict()
    if not ebayInfo:
        return ebay_data
    ebay_data['Category1'] = ebayInfo.get('PrimaryCategory', {}).get('CategoryID', {}).get('value')
    ebay_data['Category2'] = ebayInfo.get('SecondaryCategory', {}).get('CategoryID', {}).get('value')
    ebay_data['Condition'] = ebayInfo.get('ConditionID', {}).get('value')
    ebay_data['ConditionBewrite'] = None
    ebay_data['Quantity'] = ebayInfo.get('Quantity', {}).get('value')
    ebay_data['LotSize'] = ebayInfo.get('LotSize', {}).get('value')
    ebay_data['Duration'] = ebayInfo.get('ListingDuration', {}).get('value')
    ebay_data['ReservePrice'] = ebayInfo.get('ReservePrice', {}).get('value')
    ebay_data['BestOffer'] = ebayInfo.get('BestOfferDetails', {}).get('BestOfferEnabled', {}).get('value')
    ebay_data['BestOfferAutoAcceptPrice'] = ebayInfo.get('ListingDetails', {}).get('BestOfferAutoAcceptPrice', {}).get('value')
    ebay_data['BestOfferAutoRefusedPrice'] = None
    ebay_data['AcceptPayment'] = ebayInfo.get('PaymentMethods', {}).get('value')
    ebay_data['PayPalEmailAddress'] = ebayInfo.get('PayPalEmailAddress', {}).get('value')
    ebay_data['Location'] = ebayInfo.get('Location', {}).get('value')
    ebay_data['LocationCountry'] = ebayInfo.get('Country', {}).get('value')
    ebay_data['ReturnsAccepted'] = ebayInfo.get('ReturnPolicy', {}).get('ReturnsAccepted', {}).get('value')
    ebay_data['RefundOptions'] = ebayInfo.get('ReturnPolicy', {}).get('RefundOption', {}).get('value')
    ebay_data['ReturnsWithin'] = ebayInfo.get('ReturnPolicy', {}).get('ReturnsWithinOption', {}).get('value')
    ebay_data['ReturnPolicyShippingCostPaidBy'] = ebayInfo.get('ReturnPolicy', {}).get('ShippingCostPaidByOption', {}).get('value')
    ebay_data['ReturnPolicyDescription'] = ebayInfo.get('ReturnPolicy', {}).get('Description', {}).get('value')
    ebay_data['GalleryType'] = ebayInfo.get('PictureDetails', {}).get('GalleryType', {}).get('value')
    ebay_data['Bold'] = None
    ebay_data['PrivateListing'] = ebayInfo.get('PrivateListing', {}).get('value')
    ebay_data['HitCounter'] = ebayInfo.get('HitCounter', {}).get('value')
    ebay_data['sku'] = ebayInfo.get('SKU', {}).get('value')
    ebay_data['Title'] = ebayInfo.get('Title', {}).get('value')
    ebay_data['SubTitle'] = ebayInfo.get('SubTitle', {}).get('value')
    ebay_data['StartPrice'] = ebayInfo.get('StartPrice', {}).get('value')
    ebay_data['BuyItNowPrice'] = ebayInfo.get('BuyItNowPrice', {}).get('value')
    ebay_data['other_itemnum'] = None
    ebay_data['GalleryType'] = ebayInfo.get('PictureDetails', {}).get('GalleryType', {}).get('value')

    ShippingServiceOptions = ebayInfo.get('ShippingDetails', {}).get('ShippingServiceOptions')
    if type(ShippingServiceOptions) is list:
        for i in range(len(ShippingServiceOptions)):
            num = i + 1
            key_1 = 'ShippingService' + str(num)
            value_1 = ShippingServiceOptions[i].get('ShippingService', {}).get('value')
            key_2 = 'ShippingServiceCost' + str(num)
            value_2 = ShippingServiceOptions[i].get('ShippingServiceCost', {}).get('value')
            key_3 = 'ShippingServiceAdditionalCost' + str(num)
            value_3 = ShippingServiceOptions[i].get('ShippingServiceAdditionalCost', {}).get('value')
            ebay_data[key_1] = value_1
            ebay_data[key_2] = value_2
            ebay_data[key_3] = value_3
            if (num) == 4:
                break
    elif type(ShippingServiceOptions) is ObjectDict:
        num = 1
        key_1 = 'ShippingService' + str(num)
        value_1 = ShippingServiceOptions.get('ShippingService', {}).get('value')
        key_2 = 'ShippingServiceCost' + str(num)
        value_2 = ShippingServiceOptions.get('ShippingServiceCost', {}).get('value')
        key_3 = 'ShippingServiceAdditionalCost' + str(num)
        value_3 = ShippingServiceOptions.get('ShippingServiceAdditionalCost', {}).get('value')
        ebay_data[key_1] = value_1
        ebay_data[key_2] = value_2
        ebay_data[key_3] = value_3
    else:
        pass

    InternationalShippingServiceOption = ebayInfo.get('ShippingDetails', {}).get('InternationalShippingServiceOption')
    if type(InternationalShippingServiceOption) is list:
        for i in range(len(InternationalShippingServiceOption)):
            num = i + 1
            key_1 = 'InternationalShippingService' + str(num)
            value_1 = InternationalShippingServiceOption[i].get('ShippingService', {}).get('value')
            key_2 = 'InternationalShippingServiceCost' + str(num)
            value_2 = InternationalShippingServiceOption[i].get('ShippingServiceCost', {}).get('value')
            key_3 = 'InternationalShippingServiceAdditionalCost' + str(num)
            value_3 = InternationalShippingServiceOption[i].get('ShippingServiceAdditionalCost', {}).get('value')
            key_4 = 'InternationalShipToLocation' + str(num)
            ShipToLocation = InternationalShippingServiceOption[i].get('ShipToLocation')
            value_4 = handle_ExcludeShipToLocation(ShipToLocation)
            ebay_data[key_1] = value_1
            ebay_data[key_2] = value_2
            ebay_data[key_3] = value_3
            ebay_data[key_4] = value_4
            if (num) == 5:
                break
    elif type(InternationalShippingServiceOption) is ObjectDict:
        num = 1
        key_1 = 'InternationalShippingService' + str(num)
        value_1 = InternationalShippingServiceOption.get('ShippingService', {}).get('value')
        key_2 = 'InternationalShippingServiceCost' + str(num)
        value_2 = InternationalShippingServiceOption.get('ShippingServiceCost', {}).get('value')
        key_3 = 'InternationalShippingServiceAdditionalCost' + str(num)
        value_3 = InternationalShippingServiceOption.get('ShippingServiceAdditionalCost', {}).get('value')
        key_4 = 'InternationalShipToLocation' + str(num)
        ShipToLocation = InternationalShippingServiceOption.get('ShipToLocation')
        value_4 = handle_ExcludeShipToLocation(ShipToLocation)
        ebay_data[key_1] = value_1
        ebay_data[key_2] = value_2
        ebay_data[key_3] = value_3
        ebay_data[key_4] = value_4
    else:
        pass

    ebay_data['DispatchTimeMax'] = ebayInfo.get('DispatchTimeMax', {}).get('value')
    ExcludeShipToLocation = ebayInfo.get('ShippingDetails', {}).get('ExcludeShipToLocation')
    ebay_data['ExcludeShipToLocation'] = handle_ExcludeShipToLocation(ExcludeShipToLocation)
    ebay_data['StoreCategory1'] = ebayInfo.get('Storefront', {}).get('StoreCategoryID', {}).get('value')
    ebay_data['StoreCategory2'] = ebayInfo.get('Storefront', {}).get('StoreCategory2ID', {}).get('value')

    description = ebayInfo.get('Description', {}).get('value', '')
    ebay_data['Description'] = handle_description(description)
    ebay_data['Language'] = None
    variations = ebayInfo.get('Variations')
    Variation_info = handle_variations(variations)
    if Variation_info:
        Variation_info = str(Variation_info)
    ebay_data['Variation'] = Variation_info
    outofstockcontrol = ebayInfo.get('OutOfStockControl', {}).get('value')
    if outofstockcontrol:
        if outofstockcontrol == 'true':
            ebay_data['outofstockcontrol'] = 1
        elif outofstockcontrol == 'false':
            ebay_data['outofstockcontrol'] = 0
        else:
            pass
    ebay_data['EPID'] = 'Does Not Apply'
    ebay_data['ISBN'] = ebayInfo.get('ProductListingDetails', {}).get('ISBN', {}).get('value', 'Does Not Apply')
    ebay_data['UPC'] = ebayInfo.get('ProductListingDetails', {}).get('UPC', {}).get('value', 'Does Not Apply')
    ebay_data['EAN'] = ebayInfo.get('ProductListingDetails', {}).get('EAN', {}).get('value', 'Does Not Apply')
    ebay_data['SecondOffer'] = 0
    ebay_data['ImmediatelyPay'] = None
    ebay_data['Currency'] = ebayInfo.get('Currency', {}).get('value')
    ebay_data['LinkedPayPalAccount'] = None
    ebay_data['MBPVCount'] = None
    ebay_data['MBPVPeriod'] = None
    ebay_data['MUISICount'] = None
    ebay_data['MUISIPeriod'] = None
    ebay_data['MaximumItemCount'] = ebayInfo.get('BuyerRequirementDetails', {}).get('MaximumItemRequirements', {}).get('MaximumItemCount', {}).get('value')
    ebay_data['MinimumFeedbackScore'] = ebayInfo.get('BuyerRequirementDetails', {}).get('MaximumItemRequirements', {}).get('MinimumFeedbackScore', {}).get('value')
    ebay_data['listingcategory_id'] = None
    NameValueList = ebayInfo.get('Variations', {}).get('VariationSpecificsSet', {}).get('NameValueList')
    Specifics_infos = handle_specifics(NameValueList)
    for i in range(len(Specifics_infos)):
        num = i + 1
        key = 'Specifics' + str(num)
        ebay_data[key] = Specifics_infos[i]
        if i == 30:
            break
    ebay_data['variationSpecificsSet'] = None
    images = ebayInfo.get('PictureDetails', {}).get('PictureURL')
    ebay_data['Images'] = handle_images(images)
    ebay_data['PictureURL'] = ebay_data['Images'].replace(',', '\n')
    sitename = ebayInfo.get('Site', {}).get('value')
    ebay_data['Site'] = get_site_id(sitename)

    return ebay_data


def handle_ebaydata(ebay_data, shopname, username):
    res = {'code': -1, 'message': ''}
    if not ebay_data:
        res['message'] = 'No eBay Item Info.'
        return res
    ebay_data['Selleruserid'] = shopname
    ebay_data['CreateStaff'] = username
    ebay_data['UpdateStaff'] = username
    ebay_data['Status'] = 'NO'
    ebay_data['CreateTime'] = datetime.datetime.now()
    ebay_data['UpdateTime'] = datetime.datetime.now()

    keys = ', '.join(ebay_data.keys())
    keys = keys.replace('Condition,', '`Condition`,').replace('Language', '`Language`')
    values = tuple(ebay_data.values())
    values_num = len(values)

    values_str = '%s, ' * (values_num - 1) + '%s'

    sql = "INSERT INTO t_templet_ebay_collection_box (%s) VALUES (%s);" % (keys, values_str)

    cur = connection.cursor()
    try:
        cur.execute(sql, values)
        cur.execute('commit')
        res['code'] = 0
    except Exception as e:
        res['message'] = repr(e)
    cur.close()

    return res


def ebay_get_item(shopname, itemid, username=None):
    res = {'code': -1, 'message': ''}
    response = ebay_get_item_response(shopname, itemid)
    if response.response.status_code == 200:
        ebayInfo = response._response_dict.get('Item')
        # print '============', json.dumps(ebayInfo)
        ebay_data = ebay_get_item_info(ebayInfo)
        # print '============', json.dumps(ebay_data)
        res = handle_ebaydata(ebay_data, shopname, username)
    else:
        res['message'] = response.content

    return res
