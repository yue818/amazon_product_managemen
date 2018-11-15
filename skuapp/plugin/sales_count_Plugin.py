#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Time    : 2018-08-20 10:45
@Author  : chenchen
@Site    : aliexpress_left_Plugin
@File    : aliexpress_left_Plugin.py
@Software: PyCharm
'''
# -*-coding:utf-8-*-

import json

from xadmin.views import BaseAdminPlugin
from django.db.models import Q
from django.db import connection
from django.template import loader
from django.contrib import messages
from django.template import RequestContext

from skuapp.table.b_goods_sales_count import b_goods_sales_count
from skuapp.table.t_product_enter_ed_aliexpress import t_product_enter_ed_aliexpress
import datetime


# from lzd_app.table.t_online_info_lazada import t_online_info_lazada
# from lzd_app.table.t_online_info_lazada_detail import t_online_info_lazada_detail


class sales_count_Plugin(BaseAdminPlugin):
    sales_count_left_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.sales_count_left_flag)

    def block_left_navbar(self, context, nodes):
        publish_url = '/Project/admin/skuapp/b_goods_sales_count/?'
        count_all = b_goods_sales_count.objects.count()
        count_0 = b_goods_sales_count.objects.filter(inter_val=3).count()
        # tt = datetime.datetime.today() - datetime.timedelta(days=30)
        # count_0_month = b_goods_sales_count.objects.filter(inter_val=3).count()
        count_1 = b_goods_sales_count.objects.filter(inter_val=6).count()
        count_2 = b_goods_sales_count.objects.filter(inter_val=9).count()
        count_3 = b_goods_sales_count.objects.filter(inter_val=12).count()


        publish_url1 = publish_url + 'pub=6'
        publish_url2 = publish_url + 'pub=9'
        publish_url3 = publish_url + 'pub=12'


        publish_count = self.request.GET.get('pub')
        if publish_count == '3':
            flag = '0'
        elif publish_count == '6':
            flag = '1'
        elif publish_count == '9':
            flag = '2'
        elif publish_count == '12':
            flag = '3'
        else:
            flag = 'info_all'

        menu_list = [{
            "name": u"全部月份销量统计(%s)" % count_all,
            "code": "011",
            "icon": "icon-th",
            "parentCode": "",
            "selected": "",
            "to_url": "/Project/admin/skuapp/b_goods_sales_count/",
            "flag": "info_all",
            "child": [
                {
                    "name": u"3个月无销量(%s)" % count_0,
                    "code": "0111",
                    "icon": "",
                    "parentCode": "011",
                    "selected": "",
                    "to_url": publish_url + 'pub=3',
                    "flag": "0",
                    "child": []
                },
                {
                    "name": u"6个月无销量(%s)" % count_1,
                    "code": "0112",
                    "icon": "",
                    "parentCode": "011",
                    "selected": "",
                    "to_url": publish_url1,
                    "flag": "1",
                    "child": []
                },
                {
                    "name": u"9个月无销量(%s)" % count_2,
                    "code": "0113",
                    "icon": "",
                    "parentCode": "011",
                    "selected": "",
                    "to_url": publish_url2,
                    "flag": "2",
                    "child": []
                },
                {
                    "name": u"12个月无销量(%s)" % count_3,
                    "code": "0113",
                    "icon": "",
                    "parentCode": "011",
                    "selected": "",
                    "to_url": publish_url3,
                    "flag": "3",
                    "child": []
                },

            ]
        }]

        show_flag = 0
        for menu_obj in menu_list:
            if menu_obj['flag'] == flag:
                menu_obj['selected'] = 'selected'
                show_flag = 1
            for menu_c in menu_obj['child']:
                if menu_c['flag'] == flag:
                    menu_c['selected'] = 'selected'
                    show_flag = 1

        if show_flag == 1:
            nodes.append(
                loader.render_to_string('site_left_menu_tree_Plugin.html', {'menu_list': json.dumps(menu_list)},
                                        context_instance=RequestContext(self.request)))
