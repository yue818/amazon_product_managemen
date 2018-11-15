# -*- coding: utf-8 -*-
import urllib2
from lxml import etree
from random import choice
from brick.function.get_ip_proxy import get_ip_proxy
# import json
# import time
# import xlrd
# from random import uniform
# from datetime import datetime
# from django.db import connection


UA_AGENT = ['Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/6.0)',
            'Mozilla/5.0 (Windows NT 6.1; rv:2.1.1) Gecko/20110415 Firefox/4.0.2pre Fennec/4.0.1',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0']


# class GetOpponentInfoByURL(object):
#     """
#     通过URL获取对手商品信息和销量数据
#     """
#
#     def get_OneWeek_Sum(self, id):
#         """
#         抓取订单记录，求取七天订单数
#         :param id:
#         :return:
#         """
#         quantity_sum = 0
#         ua_header = {"User-Agent": choice(UA_AGENT)}
#         for i in range(1, 11):
#             time.sleep(uniform(1, 3))
#             opener = get_ip_proxy()
#             url = "https://feedback.aliexpress.com/display/evaluationProductDetailAjaxService.htm?callback=&productId=%s&type=default&page=%s" % (
#             id, i)
#             req = urllib2.Request(url, headers=ua_header)
#             resp = opener.open(req)
#             if resp.code == 200:
#                 data = resp.read()
#                 print 'data---------------%s' % data
#                 jdata = json.loads(data)
#                 records = jdata.get('records', '')
#                 if records:
#                     print 'id:%s--------page:%s------success' % (id, i)
#                     for record in records:
#                         this_date = datetime.strptime(record['date'], "%d %b %Y %H:%M")
#                         if (datetime.utcnow() - this_date).days < 7:
#                             quantity_sum += int(record['quantity'])
#                 # page数超出最大页数，records返回空列表
#                 elif records == []:
#                     break
#                 # API请求返回反爬虫信息，跳出返回error
#                 else:
#                     return 'Error'
#         return quantity_sum
#
#
#     def get_price_sum(self, id):
#         """
#         抓取商品信息
#         :param id:
#         :return:
#         """
#         image, title, unit, price, orders = ''
#         opener = get_ip_proxy()
#         ua_header = {"User-Agent": choice(UA_AGENT)}
#         url = "https://www.aliexpress.com/item/abc/%s.html" % (id)
#         req = urllib2.Request(url, headers=ua_header)
#         resp = opener.open(req)
#         if resp.code == 200:
#             data = resp.read()
#             html = etree.HTML(data)
#             image_list = html.xpath('//*[@id="j-image-thumb-list"]/li[1]/span/img/@src')
#             title_list = html.xpath('//*[@id="j-product-detail-bd"]/div[1]/div/h1')
#             image = image_list[0].split('.jpg_')[0] + '.jpg_120x120.jpg'
#             title = title_list[0].text
#             discount_price_range_list = html.xpath('//*[@id="j-sku-discount-price"]/span[1]')   # 折后价(范围价)
#             discount_price_only_list = html.xpath('//*[@id="j-sku-discount-price"]')    # 折后价(唯一价)
#             original_price_range_list = html.xpath('//*[@id="j-sku-price"]/span[1]')    # 原价(范围价)
#             original_price_only_list = html.xpath('//*[@id="j-sku-price"]')     # 原价(唯一价)
#             # 价格
#             if discount_price_range_list:
#                 low_price_list = discount_price_range_list
#                 high_price_list = html.xpath('//*[@id="j-sku-discount-price"]/span[2]')
#                 price = low_price_list[0].text + '-' + high_price_list[0].text
#             elif discount_price_only_list:
#                 price = discount_price_only_list[0].text
#             else:
#                 if original_price_range_list:
#                     low_price_list = original_price_range_list
#                     high_price_list = html.xpath('//*[@id="j-sku-price"]/span[2]')
#                     price = low_price_list[0].text + '-' + high_price_list[0].text
#                 else:
#                     price = original_price_only_list[0].text
#             # 单位
#             unithx = html.xpath('//*[@itemprop="priceCurrency"]')
#             if len(unithx) == 1:
#                 unit = unithx[0].text
#             else:
#                 unit = ''
#             # 总订单
#             orders_list = html.xpath('//*[@id="j-order-num"]')
#             if orders_list:
#                 orders = (orders_list[0].text).replace(' orders', '')
#         return image, title, unit + price, orders
#
#
# class GetOurInfoByProductID(object):
#     """
#     通过产品ID获取我方商品信息和订单信息
#     """
#
#     def get_mainsku_orders(self, product_id):
#         """
#         根据product_id在数据库查询主SKU
#         :param product_id:
#         :return:
#         """
#         main_sku = ''
#         cur = connection.cursor()
#         sql = 'select DISTINCT MainSKU from t_report_sales_daily where ProductID=%S; '
#         cur.execute(sql, (product_id, ))
#         order_info = cur.fetchone()
#         if order_info:
#             main_sku = order_info[0]
#         return main_sku
#
#     def get_image_title(self, product_id):
#         pass


def get_product_info(product_id):
    """
    抓取商品图片，标题，价格，总订单
    :param id:
    :return:
    """
    image, title, unit, price, orders, ratingValue = '', '', '', '', '', ''
    opener = get_ip_proxy()
    ua_header = {"User-Agent": choice(UA_AGENT)}
    url = "https://www.aliexpress.com/item/abc/%s.html" % (product_id)

    try:
        req = urllib2.Request(url, headers=ua_header)
        resp = opener.open(req)
    except Exception as e:
        print e
        return image, title, unit, price, orders, ratingValue

    if resp.code == 200:
        data = resp.read()
        html = etree.HTML(data)

        try:
            image_list = html.xpath('//*[@id="j-image-thumb-list"]/li[1]/span/img/@src')
            image = image_list[0]
        except Exception as e:
            print e

        try:
            title_list = html.xpath('//*[@id="j-product-detail-bd"]/div[1]/div/h1')
            title = title_list[0].text
        except Exception as e:
            print e

        # 价格
        try:
            discount_price_range_list = html.xpath('//*[@id="j-sku-discount-price"]/span[1]')   # 折后价(范围价)
            discount_price_only_list = html.xpath('//*[@id="j-sku-discount-price"]')    # 折后价(唯一价)
            original_price_range_list = html.xpath('//*[@id="j-sku-price"]/span[1]')    # 原价(范围价)
            original_price_only_list = html.xpath('//*[@id="j-sku-price"]')     # 原价(唯一价)
            if discount_price_range_list:
                low_price_list = discount_price_range_list
                high_price_list = html.xpath('//*[@id="j-sku-discount-price"]/span[2]')
                price = low_price_list[0].text + '-' + high_price_list[0].text
            elif discount_price_only_list:
                price = discount_price_only_list[0].text
            else:
                if original_price_range_list:
                    low_price_list = original_price_range_list
                    high_price_list = html.xpath('//*[@id="j-sku-price"]/span[2]')
                    price = low_price_list[0].text + '-' + high_price_list[0].text
                else:
                    price = original_price_only_list[0].text
        except Exception as e:
            print e

        # 单位
        try:
            unithx = html.xpath('//*[@itemprop="priceCurrency"]')
            if len(unithx) == 1:
                unit = unithx[0].text
            else:
                unit = ''
        except Exception as e:
            print e

        # 总订单
        try:
            orders_list = html.xpath('//*[@id="j-order-num"]')
            if orders_list:
                orders = (orders_list[0].text).replace(' orders', '')
        except Exception as e:
            print e

        # 商品评分
        ratingValue = ''
        try:
            rating = html.xpath('//*[@id="j-customer-reviews-trigger"]/span[1]/span/span/span[1]')
            if len(rating) == 1:
                ratingValue = rating[0].text
        except Exception as e:
            print e

    return image, title, unit, price, orders, ratingValue


# def read_aliexpress_excel(file_obj, import_time, import_user):
#     """
#     读取导入的aliexpress待比价Excel
#     :param file_obj: Excel文件
#     :param import_time: 导入时间
#     :param import_user: 导入人
#     :return:
#     """
#     cur = connection.cursor()
#     file_name = file_obj.name
#     data = xlrd.open_workbook(filename=None, file_contents=file_obj.read())
#     table = data.sheets()[0]
#     nrows = table.nrows
#     for rownum in range(nrows):
#         row = table.row_values(rownum)
#         if row:
#             import_product_id = row[0]
#             print 'import_product_id---------%s' % import_product_id
#             params, flag = get_listing_info(import_product_id, import_time, import_user, file_name, cur)
#             insert_listing(params, flag, cur)
#             print '=' * 30
#     insert_possible(import_time, cur)
#     cur.close()


# def get_listing_info(import_product_id, import_time, import_user, file_name, cur):
#     """
#     根据导入的productID查询需要的信息
#     :param import_product_id: 导入的productID
#     :param import_time: 导入时间
#     :param import_user: 导入人
#     :param file_name: 导入Excel文件名
#     :param cur:
#     :return:
#     """
#     params = []
#     now_date = import_time[:10]
#     sql_1 = 'select DISTINCT MainSKU from t_report_sales_daily where ProductID=%s'
#     cur.execute(sql_1, (import_product_id, ))
#     mainsku_info = cur.fetchone()
#     if mainsku_info:
#         mainsku = mainsku_info[0]
#         print 'mainsku------%s' % mainsku
#         sql_2 = 'select ProductID, LEFT(shopname, 8), sum(SalesVolume) from t_report_sales_daily where ' \
#                 'DATE_ADD(OrderDay,INTERVAL+7 DAY) >= %s AND MainSKU=%s AND PlatformName="aliexpress" GROUP BY shopname'
#         cur.execute(sql_2, (now_date, mainsku))
#         sale_infos = cur.fetchall()
#         if sale_infos:
#             for sale_info in sale_infos:
#                 product_id = sale_info[0]
#                 shop_name = sale_info[1]
#                 sale_num_7 = sale_info[2]
#                 seller = ''
#                 sql_3 = 'select Seller from t_store_configuration_file where ShopName_temp=%s'
#                 cur.execute(sql_3, (shop_name, ))
#                 seller_info = cur.fetchone()
#                 if seller_info:
#                     seller = seller_info[0]
#                 print 'product_id------------%s' % product_id
#                 image, title, price, orders_all = get_product_info(product_id)
#                 print 'image, title, price, orders_all-------------%s,%s,%s,%s' % (image, title, price, orders_all)
#                 param = (product_id, mainsku, shop_name, sale_num_7, seller, import_time, import_user, image, title,
#                          price, orders_all, file_name)
#                 params.append(param)
#             flag = 1
#         else:
#             note = u'没找到该MainSKU对应的七天销量信息'
#             param = (import_product_id, mainsku, import_time, import_user, file_name, note)
#             params.append(param)
#             flag = 2
#     else:
#         note = u'未找到该productID对应的商品信息'
#         param = (import_product_id, import_time, import_user, file_name, note)
#         params.append(param)
#         flag = 3
#     print 'params, flag-----%s---%s' % (params, flag)
#     return params, flag
#
#
# def insert_listing(params, flag, cur):
#     """
#     将查询结果插入到在线listing表
#     :param params:
#     :param flag:
#     :param cur:
#     :return:
#     """
#     if flag == 1:
#         sql = 'insert into t_aliexpress_compare_price_listing(OurProductID, OurMainSKU, ShopName, OurWeekOrders, Seller, ' \
#               'ImportTime, ImportName, OurImage, OurTitle, OurPrice, OurOrders, ExcelFile) ' \
#               'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
#         for param in params:
#             cur.execute(sql, param)
#     elif flag == 2:
#         sql = 'insert into t_aliexpress_compare_price_listing(OurProductID, OurMainSKU, ImportTime, ImportName, ' \
#               'ExcelFile, Note) VALUES (%s,%s,%s,%s,%s,%s)'
#         cur.execute(sql, params[0])
#     else:
#         sql = 'insert into t_aliexpress_compare_price_listing(OurProductID, ImportTime, ImportName, ExcelFile, Note) ' \
#               'VALUES (%s,%s,%s,%s,%s)'
#         cur.execute(sql, params[0])
#
#     cur.execute('commit; ')
#
#
# def insert_possible(import_time, cur):
#     """
#     取出本次导入的表格中七天订单数最大一条listing放到可比价表
#     :param import_time:
#     :param cur:
#     :return:
#     """
#     sql = 'insert into t_aliexpress_compare_price_possible(OurProductID, OurMainSKU, ShopName, OurWeekOrders, Seller, ImportTime, ImportName, OurImage, OurTitle, OurPrice, OurOrders, ExcelFile) ' \
#           'select * from (select OurProductID, OurMainSKU, ShopName, OurWeekOrders, Seller, ImportTime, ImportName, OurImage, OurTitle, OurPrice, OurOrders, ExcelFile from t_aliexpress_compare_price_listing as a ' \
#           'where OurWeekOrders=(select max(b.OurWeekOrders) from t_aliexpress_compare_price_listing as b where a.OurMainSKU = b.OurMainSKU)) as c group by OurMainSKU'
#     cur.execute(sql, (import_time, ))
#     cur.execute('commit; ')
#
