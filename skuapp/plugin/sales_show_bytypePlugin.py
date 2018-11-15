#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: sales_show_bytypePlugin.py
 @time: 2018-04-12 20:08
"""
from __future__ import division
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.db import connection
import json
from django.contrib import messages
from datetime import datetime
import datetime as datime

class sales_show_bytypePlugin(BaseAdminPlugin):

    sales_show_bytype_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.sales_show_bytype_flag)

    def get_media(self, media):
        media.add_js([self.static('xadmin/js/xadmin.plugin.button.color.js')])
        return media

    def get_para(self, sourceURL):

        x = datetime.now() + datime.timedelta(days=-90)
        begdate = x.strftime('%Y-%m-%d')

        sql = 'select SKU,ShopName,ProductID,ShopSKU,MainSKU from t_report_sales_daily order by orderday desc limit 1'
        with connection.cursor() as cursor:
            cursor.execute(sql)
            defaultdata = cursor.fetchone()

        sql = ''
        title = ''
        if 'byshopname' in sourceURL:
            ShopName = self.request.GET.get('ShopName1', '')
            if ShopName == '':
                ShopName = defaultdata[1]
                title = 'ShopName:%s(随机)日销量'% (ShopName,)
            else:
                title = 'ShopName:%s 日销量' % (ShopName,)

            sql = '''select OrderDay,SalesVolume from t_report_sales_daily_byShopName WHERE ShopName='%s' and OrderDay>='%s' ORDER by OrderDay'''%(ShopName, begdate,)

        elif 'byproductid' in sourceURL:
            ProductID = self.request.GET.get('ProductID', '')
            if ProductID == '':
                ProductID = defaultdata[2]
                title = 'ProductID:%s(随机)日销量' % (ProductID,)
            else:
                title = 'ProductID:%s 日销量' % (ProductID,)

            sql = '''select OrderDay,SalesVolume from t_report_sales_daily_byProductID WHERE ProductID='%s' and OrderDay>='%s' ORDER by OrderDay''' %(ProductID, begdate,)

        elif r't_report_sales_daily/' in sourceURL:  #base
            ShopSKU = self.request.GET.get('ShopSKU', '')
            ShopName = self.request.GET.get('ShopName1', '')

            if ShopSKU == '' and ShopName == '':
                ShopSKU = defaultdata[3]
                ShopName = defaultdata[1]
                title = 'ShopName:%s->%s(随机)日销量' % (ShopName,ShopSKU,)
                sql = '''select OrderDay,SalesVolume from t_report_sales_daily WHERE ShopName='%s' and ShopSKU='%s' and OrderDay>='%s' ORDER by OrderDay'''%(
                    ShopName, ShopSKU, begdate,)

            elif ShopSKU != '' and ShopName != '':
                title = 'ShopName:%s->%s 日销量' % (ShopName, ShopSKU,)
                sql = '''select OrderDay,SalesVolume from t_report_sales_daily WHERE ShopName='%s' and ShopSKU='%s' and OrderDay>='%s' ORDER by OrderDay''' % (
                    ShopName, ShopSKU, begdate,)
            elif ShopSKU != '':
                title = 'ShopSKU:%s 日销量' % (ShopSKU,)
                sql = '''select OrderDay,sum(SalesVolume) as SalesVolume from t_report_sales_daily WHERE ShopSKU='%s' and OrderDay>='%s' group by OrderDay ORDER by OrderDay''' % (
                    ShopSKU, begdate,)
            else:
                title = 'ShopName:%s 日销量' % (ShopName,)
                sql = '''select OrderDay,SalesVolume from t_report_sales_daily_byShopName WHERE ShopName='%s' and OrderDay>='%s' ORDER by OrderDay''' % (
                ShopName, begdate,)

        elif 'bymainsku' in sourceURL:
            MainSKU = self.request.GET.get('MainSKU', '')
            if MainSKU == '':
                MainSKU = defaultdata[4]
                title = 'MainSKU:%s(随机)日销量' % (MainSKU,)
            else:
                title = 'MainSKU:%s 日销量' % (MainSKU,)

            sql = '''select OrderDay,SalesVolume from t_report_sales_daily_byMainSKU WHERE MainSKU='%s' and OrderDay>='%s' ORDER by OrderDay''' % (
                MainSKU, begdate,)

        elif 'bysku' in sourceURL:
            SKU = self.request.GET.get('SKU', '')
            if SKU == '':
                SKU = defaultdata[0]
                title = 'SKU:%s(随机)日销量' % (SKU,)
            else:
                title = 'SKU:%s 日销量' % (SKU,)

            sql = '''select OrderDay,SalesVolume from t_report_sales_daily_bySKU WHERE SKU='%s' and OrderDay>='%s' ORDER by OrderDay''' % (
                SKU, begdate,)

        return sql.replace('\\', '\\\\'), title  #MySQL \ 转义问题

    def block_search_cata_nav(self, context, nodes):

        sourceURL = str(context['request']).split("'")[1]
        sql, title = self.get_para(sourceURL)

        #messages.info(self.request, 'sql:%s'%(sql, ))

        with connection.cursor() as cursor:
            cursor.execute(sql)
            objs = cursor.fetchall()

        daylist = []
        saleslist = []
        _saleslist = []
        for obj in objs:
            daylist.append('%s' % obj[0].strftime('%Y%m%d'))
            saleslist.append(int(obj[1]))
            _saleslist.append(int(obj[1]))

        _saleslist.reverse()
        sales7ordery = [round(sum(_saleslist[i:i + 7]) / len(_saleslist[i:i + 7]), 2) for i in range(len(_saleslist))]
        sales7ordery.reverse()

        returndata = {'title': title,
                      'daylist': json.dumps(daylist),
                      'saleslist': json.dumps(saleslist),
                      'sales7ordery': json.dumps(sales7ordery)}

        nodes.append(loader.render_to_string('sales_show2.html', returndata))