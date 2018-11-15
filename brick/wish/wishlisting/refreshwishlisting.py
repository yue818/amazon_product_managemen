# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: refreshwishlisting.py
 @time: 2017-12-22 9:16

"""
from brick.table.t_online_info import t_online_info
from brick.table.t_report_orders1days import t_report_orders1days
from brick.table.t_online_info_wish import t_online_info_wish
from brick.table.t_store_configuration_file import t_store_configuration_file
from brick.classredis.classmainsku import classmainsku
from brick.classredis.classlisting import classlisting
from brick.classredis.classshopsku import classshopsku
from brick.table.t_templet_wish_upload_result import t_templet_wish_upload_result
from brick.table.t_distribution_product_to_store_result import t_distribution_product_to_store_result
from brick.table.t_large_small_corresponding_cate import t_large_small_corresponding_cate
import datetime
import logging
import re
import urllib2

from brick.table.t_wish_pb_campaignproductstats import t_wish_pb_campaignproductstats
from brick.wish.api.wish_rating import product_rating

logger = logging.getLogger('sourceDns.webdns.views')


def get_rating(product_id):
    try:
        r = product_rating(product_id)
        _content = eval(r)
        return _content
    except Exception as e:
        return {"code": -1, "error_info": u"%s" % e}


def get_salestrend(product_id, sales_objs):
    lastobjs = sales_objs.lastweeksSales(product_id)
    nextlastobjs = sales_objs.nextlastweeksSales(product_id)
    if lastobjs['errorcode'] == 1 and nextlastobjs['errorcode'] == 1:
        if nextlastobjs['data'] == 0 and lastobjs['data'] > 0:
            return 1
        elif nextlastobjs['data'] == 0 and lastobjs['data'] == 0:
            return 0
        elif (lastobjs['data']-nextlastobjs['data'])/nextlastobjs['data'] >= 0.2:
            return 1
        elif (lastobjs['data']-nextlastobjs['data'])/nextlastobjs['data'] < -0.2 :
            return -1
        else:
            return 0
    else:
        return 0


def run(params):
    # 获取需要刷新的数据
    t_online_info_objs = t_online_info(params['ShopName'], params['dbcnxn'])
    t_report_orders1days_objs = t_report_orders1days(params['dbcnxn'])
    t_store_configuration_file_obj = t_store_configuration_file(params['dbcnxn'])
    classlisting_obj = classlisting(params['dbcnxn'])
    classmainsku_obj = classmainsku(params['dbcnxn'])
    t_templet_wish_upload_result_obj = t_templet_wish_upload_result(params['dbcnxn'])
    classshopsku_obj = classshopsku(params['dbcnxn'],shopname=params['ShopName'])
    t_online_info_wish_obj = t_online_info_wish(params['dbcnxn'])
    t_distribution_product_to_store_result_obj = t_distribution_product_to_store_result(params['dbcnxn'])
    t_large_small_corresponding_cate_obj = t_large_small_corresponding_cate(params['dbcnxn'])
    t_wish_pb_campaignproductstats_obj = t_wish_pb_campaignproductstats(params['dbcnxn'])

    infodata = t_online_info_objs.getshopproductdata(params['ProductID'])

    for obj in infodata:
        datedict = {}
        datedict['ProductID']   = obj['ProductID']
        datedict['ShopName']    = obj['ShopName']
        datedict['Title']       = obj['Title']
        datedict['SKU']         = obj['SKU']
        datedict['ShopSKU']     = obj['ShopSKU']
        datedict['Price']       = obj['Price']
        datedict['RefreshTime'] = obj['RefreshTime']

        yyyymmdd = obj['RefreshTime'].strftime('%Y%m%d')

        datedict['SoldTheDay']    = t_report_orders1days_objs.getSoldTheDay(obj['ProductID'],yyyymmdd)

        datedict['SoldYesterday'] = t_report_orders1days_objs.getSoldYesterday(obj['ProductID'],yyyymmdd)

        datedict['Orders7Days']   = t_report_orders1days_objs.getOrders7Days(obj['ProductID'],yyyymmdd) # 默认 普通仓

        # 海外仓 7天订单数，总销量 订单不足 数值偏小
        datedict['Order7daysDE']  = t_report_orders1days_objs.getOrders7Days_WarehouseName(obj['ProductID'], yyyymmdd, 'DE')
        datedict['Order7daysGB']  = t_report_orders1days_objs.getOrders7Days_WarehouseName(obj['ProductID'], yyyymmdd, 'GB')
        datedict['Order7daysUS']  = t_report_orders1days_objs.getOrders7Days_WarehouseName(obj['ProductID'], yyyymmdd, 'US')
        datedict['Order7daysFBW'] = t_report_orders1days_objs.getOrders7Days_WarehouseName(obj['ProductID'], yyyymmdd, 'FBW')

        datedict['OfsalesDE'] = t_report_orders1days_objs.ofSales_Of_ProductID_WarehouseName(obj['ProductID'], 'DE')
        datedict['OfsalesGB'] = t_report_orders1days_objs.ofSales_Of_ProductID_WarehouseName(obj['ProductID'], 'GB')
        datedict['OfsalesUS'] = t_report_orders1days_objs.ofSales_Of_ProductID_WarehouseName(obj['ProductID'], 'US')
        datedict['OfsalesFBW'] = t_report_orders1days_objs.ofSales_Of_ProductID_WarehouseName(obj['ProductID'], 'FBW')

        classlisting_obj.set_order7days_listingid(datedict['ProductID'],datedict['Orders7Days'])

        datedict['SoldXXX']       = int(datedict['SoldTheDay']) - int(datedict['SoldYesterday'])

        datedict['DateOfOrder'] = None
        datedict['Image']       = obj['Image']
        datedict['Status']      = obj['Status']
        datedict['ReviewState'] = obj['ReviewState']
        datedict['DateUploaded']= obj['DateUploaded']
        datedict['LastUpdated'] = obj['LastUpdated']
        datedict['OfSales']     = obj['OfSales']
        datedict['ParentSKU']   = obj['ParentSKU']

        datedict['is_promoted']   = obj['is_promoted']
        datedict['WishExpress']   = obj['WishExpress']

        datedict['Seller'] = t_store_configuration_file_obj.getsellerbyshopcode(params['ShopName'][0:9])

        datedict['MainSKU'] = obj['MainSKU']

        datedict['TortInfo'] = 'N'
        mainskulist = classlisting_obj.getmainsku(obj['ProductID'])
        if mainskulist:
            tortlist = []
            for mainsku in set(mainskulist):
                tortsite = classmainsku_obj.get_tort_by_mainsku(mainsku)
                if tortsite is not None:
                    tortlist = tortlist + tortsite
            if tortlist:
                if 'Wish' in tortlist:
                    datedict['TortInfo'] = 'WY'
                else:
                    datedict['TortInfo'] = 'Y'

        datedict['DataSources'] = "NORMAL"
        if t_templet_wish_upload_result_obj.get_count_num(obj['ParentSKU'],obj['ShopName']) >= 1:
            datedict['DataSources'] = "UPLOAD"
        else:
            if t_distribution_product_to_store_result_obj.get_count_num(obj['ParentSKU'],obj['ShopName']) >= 1:
                datedict['DataSources'] = "UPLOAD"

        datedict['OperationState']  = 'No'
        if obj['Status'] == 'Disabled':
            datedict['OperationState'] = 'Yes'

        # MainSKU,大类，小类
        datedict['MainSKULargeCate'] = None
        datedict['MainSKUSmallCate'] = None

        mlist = []
        if datedict['MainSKU']:
            mlist = re.findall(r'[0-9]+|[a-z]+|[A-Z|]+|[-]', datedict['MainSKU'])
        if len(mlist) >= 1:
            datedict['MainSKUSmallCate'] = mlist[0]  # 小类
            lResult = t_large_small_corresponding_cate_obj.getLargeClassBySmallClass(datedict['MainSKUSmallCate'])
            if lResult['code'] == 1:
                datedict['MainSKULargeCate'] = lResult['largecode']

        datedict['SName'] = '0'  # 店铺状态 0 正常 -1 异常
        # 1 正常(在线); 0 正常(不在线); -1 api调用错误; -2 执行代码异常;
        if datedict['ReviewState'] == 'approved'and datedict['Status'] == 'Enabled':
            datedict['AdStatus'] = '1'   # 1 正常(在线)
        else:
            datedict['AdStatus'] = '0'   # 0 正常(不在线)

        datedict['Published'] = None
        if obj['ShopSKU'] is not None and obj['ShopSKU'].strip() != '':
            pub = None
            for shopsku in obj['ShopSKU'].split(','):
                for each_shopsku in shopsku.split('+'):
                    pub = classshopsku_obj.getPublished(each_shopsku.split('*')[0].split('\\')[0].split('/')[0])  # 按照店铺SKU来抓取刊登人
                    if pub:
                        break
                if pub:
                    break
            datedict['Published'] = pub

        datedict['market_time']    = None

        # 这里是商品状态结果集
        statuslist = t_online_info_objs.get_goodsstatus_by_productid(params['ProductID'])
        a1 = 0
        if '1' in statuslist:
            a1 = 1
        a2 = 0
        if '2' in statuslist:
            a2 = 1
        a3 = 0
        if '3' in statuslist:
            a3 = 1
        a4 = 0
        if '4' in statuslist:
            a4 = 1
        datedict['GoodsFlag'] = a1*1000 + a2*100 + a3*10 + a4

        # 店铺SKU状态结果集
        sstatuslist = t_online_info_objs.get_shopskustatus_by_productid(params['ProductID'])
        b1 = 0
        if 'Enabled' in sstatuslist:
            b1 = 1
        b2 = 0
        if 'Disabled' in sstatuslist:
            b2 = 1
        datedict['ShopsFlag'] = b1*10 + b2

        # 绑定状态结果集
        datedict['BindingFlag'] = 1  # 默认全部绑定
        # anum = obj[-1] # 变体数量
        # unum = t_online_info_objs.get_binding_by_productid(params['ProductID'])
        # if int(anum) == int(unum):
        #     datedict['BindingFlag'] = 3
        # elif int(anum) > 0 and int(unum) == 0:
        #     datedict['BindingFlag'] = 1
        # elif int(anum) > 0 and int(unum) != 0:
        #     datedict['BindingFlag'] = 2
        # print datedict

        datedict['BeforeReviewState'] = obj['BeforeReviewState']  # 上一个wish查看状态

        datedict['Rating'] = 0   # 链接的评分
        if float(datedict['OfSales']) > 0:
            rResult = t_online_info_wish_obj.get_product_id_rating(datedict['ProductID'])
            old_rating = rResult.get('rating', 0)

            Gresult = get_rating(datedict['ProductID'])
            new_rating = Gresult.get('rating', 0)

            if new_rating == 0 and datedict['ReviewState'] == 'rejected':  # 被拒绝的连接
                datedict['Rating'] = old_rating
            elif new_rating != 0:
                datedict['Rating'] = new_rating


        datedict['ADShow'] = 0      # 是否有广告   0 没有  1  有
        adResult = t_wish_pb_campaignproductstats_obj.j_ad(datedict['ProductID'])
        if adResult['errorcode'] == 1:
            datedict['ADShow'] = 1

        # 周销量趋势 -1:下降 0:平稳 1:上升
        datedict['SalesTrend'] = get_salestrend(datedict['ProductID'], t_report_orders1days_objs)

        datedict['FBW_Flag'] = obj['FBW_Flag']  # fbw 标记

        print "datedict['ProductID']=============%s" % datedict['ProductID']

        t_online_info_wish_obj.refreshwishdata(datedict)


