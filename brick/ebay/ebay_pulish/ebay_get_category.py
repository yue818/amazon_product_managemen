# -*- coding: utf-8 -*-

"""
 @desc:
 @author: 孙健
 @site:
"""

import datetime
import logging

from django.db import connection

from brick.ebay.api.eBay_Public_API import eBayAPI
from skuapp.table.t_config_store_ebay import t_config_store_ebay
from ebayapp.table.t_developer_info_ebay import t_developer_info_ebay

logger = logging.getLogger('django.brick.ebay.ebay_publish')


def get_ebay_app_store_info(shopname):
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

    return appinfo, storeinfo


def ebay_get_category_response(appinfo, storeinfo, category_id=None, level_limit=None, site_id=None):
    if site_id:
        storeinfo['siteID'] = site_id
    ebay_obj = eBayAPI(appinfo, storeinfo)
    response = ebay_obj.GetCategory(category_id=category_id, level_limit=level_limit)
    return response


def ebay_get_category_info(category_array, site_id):
    now = datetime.datetime.now()
    ebay_category_array = list()
    if isinstance(category_array, dict):
        SiteID = site_id
        AutoPayEnabled = category_array.get('AutoPayEnabled', {}).get('value')
        BestOfferEnabled = category_array.get('BestOfferEnabled', {}).get('value')
        CategoryID = category_array.get('CategoryID', {}).get('value')
        CategoryLevel = category_array.get('CategoryLevel', {}).get('value')
        CategoryName = category_array.get('CategoryName', {}).get('value')
        CategoryParentID = category_array.get('CategoryParentID', {}).get('value')
        LeafCategory = category_array.get('LeafCategory', {}).get('value')
        LastUpdateTime = now
        e_c_t = (SiteID, AutoPayEnabled, BestOfferEnabled, CategoryID, CategoryLevel, CategoryName, CategoryParentID, LeafCategory, LastUpdateTime)
        ebay_category_array.append(e_c_t)
    elif isinstance(category_array, list):
        for i in category_array:
            SiteID = site_id
            AutoPayEnabled = i.get('AutoPayEnabled', {}).get('value')
            BestOfferEnabled = i.get('BestOfferEnabled', {}).get('value')
            CategoryID = i.get('CategoryID', {}).get('value')
            CategoryLevel = i.get('CategoryLevel', {}).get('value')
            CategoryName = i.get('CategoryName', {}).get('value')
            CategoryParentID = i.get('CategoryParentID', {}).get('value')
            LeafCategory = i.get('LeafCategory', {}).get('value')
            LastUpdateTime = now
            e_c_t = (SiteID, AutoPayEnabled, BestOfferEnabled, CategoryID, CategoryLevel, CategoryName, CategoryParentID, LeafCategory, LastUpdateTime)
            ebay_category_array.append(e_c_t)

    return ebay_category_array


def handle_ebay_category(ebay_category_array):
    res = {'code': -1, 'message': ''}
    if not ebay_category_array:
        res['message'] = 'No eBay Category Info.'
        return res
    keys = ['SiteID', 'AutoPayEnabled', 'BestOfferEnabled', 'CategoryID', 'CategoryLevel', 'CategoryName', 'CategoryParentID', 'LeafCategory', 'LastUpdateTime']
    keys_str = ', '.join(keys)

    values_num = len(keys)
    values_str = '%s, ' * (values_num - 1) + '%s'

    sql = "INSERT INTO hq_db.t_config_ebay_category (%s) VALUES (%s);" % (keys_str, values_str)

    cur = connection.cursor()
    try:
        cur.executemany(sql, ebay_category_array)
        cur.execute('commit')
        res['code'] = 0
    except Exception as e:
        res['message'] = repr(e)
    cur.close()

    return res


def clear_ebay_category(site_id):
    res = {'code': -1, 'message': ''}
    sql = "DELETE FROM hq_db.t_config_ebay_category WHERE SiteID=%s"

    cur = connection.cursor()
    try:
        cur.execute(sql, (site_id,))
        res['code'] = 0
    except Exception as e:
        res['message'] = repr(e)
    cur.close()

    return res


def truncate_ebay_category_table():
    res = {'code': -1, 'message': ''}
    sql = "TRUNCATE TABLE hq_db.t_config_ebay_category"

    cur = connection.cursor()
    try:
        cur.execute(sql)
        res['code'] = 0
    except Exception as e:
        res['message'] = repr(e)
    cur.close()

    return res


def ebay_get_category(shopname, category_id=None, level_limit=None, site_id=None):
    res = {'code': -1, 'message': ''}

    logger.info("[.] Start get_ebay_app_store_info")
    appinfo, storeinfo = get_ebay_app_store_info(shopname)

    if not site_id:
        site_id = storeinfo['siteID']

    logger.info("[.] Start clear_ebay_category")
    clear_res = clear_ebay_category(site_id)
    if clear_res['code']:
        res.update(clear_res)
        return res

    logger.info("[.] Start ebay_get_category_response")
    response = ebay_get_category_response(appinfo, storeinfo, category_id=category_id, level_limit=level_limit, site_id=site_id)
    if response.response.status_code == 200:
        category_array = response._response_dict.get('CategoryArray').get('Category')
        # logger.info("[.] category_array: %s" % str(category_array))
        logger.info("[.] Start ebay_get_category_info")
        ebay_category_array = ebay_get_category_info(category_array, site_id)
        logger.info("[.] Start handle_ebay_category")
        res = handle_ebay_category(ebay_category_array)
    else:
        res['message'] = response.content

    return res
