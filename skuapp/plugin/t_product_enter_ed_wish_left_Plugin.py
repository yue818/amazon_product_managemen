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
from skuapp.table.t_product_enter_ed_aliexpress import t_product_enter_ed_aliexpress
import datetime

# from lzd_app.table.t_online_info_lazada import t_online_info_lazada
# from lzd_app.table.t_online_info_lazada_detail import t_online_info_lazada_detail


class t_product_enter_ed_wish_left_Plugin(BaseAdminPlugin):
    t_product_enter_ed_wish_left_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.t_product_enter_ed_wish_left_flag)

    def block_left_navbar(self, context, nodes):

        request = self.request
        user_name = request.user.username
        # conn_mysql = connection
        # cursor_mysql = conn_mysql.cursor()

        conn_mysql = connection
        cursor_mysql = conn_mysql.cursor()

        try:
            flag = 1
            sql = """SELECT DepartmentID FROM t_sys_department_staff WHERE StaffID = %s; """
            args = (user_name,)
            cursor_mysql.execute(sql, args)
            DepartmentID = cursor_mysql.fetchall()

            DepartmentID = DepartmentID[0][0]

            # user_list = []
            sql = """SELECT StaffID FROM t_sys_department_staff WHERE DepartmentID = %s"""
            args = (DepartmentID,)
            cursor_mysql.execute(sql, args)
            user_tuple = cursor_mysql.fetchall()

            conn_mysql.close()

            user_list = []
            for i in user_tuple:
                user_list.append(i[0])
        except:
            flag = 0

        if flag == 1:
            publish_url = '/Project/admin/skuapp/t_product_enter_ed_wish?'
            count_all = ''
            count_0 = ''
            count_1 = ''
            count_2 = ''
            count_3 = ''
            count_4 = ''
            count_5 = ''
            if DepartmentID == '1':
                count_all = t_product_enter_ed_aliexpress.objects.filter(
                                                                         StaffID__in=user_list).count()
                count_0 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0,
                                                                       StaffID__in=user_list).exclude(
                    onebuOperation__exact=2).count()
                tt = datetime.datetime.today() - datetime.timedelta(days=30)
                # count_0_month = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0, MGTime__gte=tt).count()
                count_1 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=1,
                                                                       StaffID__in=user_list).exclude(
                    onebuOperation__exact=2).count()
                count_2 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=2,
                                                                       StaffID__in=user_list).exclude(
                    onebuOperation__exact=2).count()
                count_3 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=3,
                                                                       StaffID__in=user_list).exclude(
                    onebuOperation__exact=2).count()
                count_4 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__gt=3,
                                                                       StaffID__in=user_list).exclude(
                    onebuOperation__exact=2).count()
                count_5 = t_product_enter_ed_aliexpress.objects.filter(onebuOperation__exact=2,
                                                                       StaffID__in=user_list).count()
            if DepartmentID == '2':
                count_all = t_product_enter_ed_aliexpress.objects.filter(StaffID__in=user_list).count()
                count_0 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0,
                                                                       StaffID__in=user_list).exclude(
                    twobuOperation__exact=2).count()
                tt = datetime.datetime.today() - datetime.timedelta(days=30)
                # count_0_month = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0, MGTime__gte=tt).count()
                count_1 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=1,
                                                                       StaffID__in=user_list).exclude(
                    twobuOperation__exact=2).count()
                count_2 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=2,
                                                                       StaffID__in=user_list).exclude(
                    twobuOperation__exact=2).count()
                count_3 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=3,
                                                                       StaffID__in=user_list).exclude(
                    twobuOperation__exact=2).count()
                count_4 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__gt=3,
                                                                       StaffID__in=user_list).exclude(
                    twobuOperation__exact=2).count()
                count_5 = t_product_enter_ed_aliexpress.objects.filter(twobuOperation__exact=2,
                                                                       StaffID__in=user_list).count()
            if DepartmentID == '3':
                count_all = t_product_enter_ed_aliexpress.objects.filter(StaffID__in=user_list).count()
                count_0 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0,
                                                                       StaffID__in=user_list).exclude(
                    threebuOperation__exact=2).count()
                tt = datetime.datetime.today() - datetime.timedelta(days=30)
                # count_0_month = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0, MGTime__gte=tt).count()
                count_1 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=1,
                                                                       StaffID__in=user_list).exclude(
                    threebuOperation__exact=2).count()
                count_2 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=2,
                                                                       StaffID__in=user_list).exclude(
                    threebuOperation__exact=2).count()
                count_3 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=3,
                                                                       StaffID__in=user_list).exclude(
                    threebuOperation__exact=2).count()
                count_4 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__gt=3,
                                                                       StaffID__in=user_list).exclude(
                    threebuOperation__exact=2).count()
                count_5 = t_product_enter_ed_aliexpress.objects.filter(threebuOperation__exact=2,StaffID__in=user_list).count()
            if DepartmentID == '4':
                count_all = t_product_enter_ed_aliexpress.objects.filter(StaffID__in=user_list).count()
                count_0 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0,
                                                                       StaffID__in=user_list).exclude(
                    fourbuOperation__exact=2).count()
                tt = datetime.datetime.today() - datetime.timedelta(days=30)
                count_0_month = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0, MGTime__gte=tt).count()
                count_1 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=1,
                                                                       StaffID__in=user_list).exclude(
                    fourbuOperation__exact=2).count()
                count_2 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=2,
                                                                       StaffID__in=user_list).exclude(
                    fourbuOperation__exact=2).count()
                count_3 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=3,
                                                                       StaffID__in=user_list).exclude(
                    fourbuOperation__exact=2).count()
                count_4 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__gt=3,
                                                                       StaffID__in=user_list).exclude(
                    fourbuOperation__exact=2).count()
                count_5 = t_product_enter_ed_aliexpress.objects.filter(fourbuOperation__exact=2,
                                                                       StaffID__in=user_list).count()
            if DepartmentID == '5':
                count_all = t_product_enter_ed_aliexpress.objects.filter(StaffID__in=user_list).count()
                count_0 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0,
                                                                       StaffID__in=user_list).exclude(
                    fivebuOperation__exact=2).count()
                tt = datetime.datetime.today() - datetime.timedelta(days=30)
                # count_0_month = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0, MGTime__gte=tt).count()
                count_1 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=1,
                                                                       StaffID__in=user_list).exclude(
                    fivebuOperation__exact=2).count()
                count_2 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=2,
                                                                       StaffID__in=user_list).exclude(
                    fivebuOperation__exact=2).count()
                count_3 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=3,
                                                                       StaffID__in=user_list).exclude(
                    fivebuOperation__exact=2).count()
                count_4 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__gt=3,
                                                                       StaffID__in=user_list).exclude(
                    fivebuOperation__exact=2).count()
                count_5 = t_product_enter_ed_aliexpress.objects.filter(fivebuOperation__exact=2,
                                                                       StaffID__in=user_list).count()
            if DepartmentID == '6':
                count_all = t_product_enter_ed_aliexpress.objects.filter(StaffID__in=user_list).count()
                count_0 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0,
                                                                       StaffID__in=user_list).exclude(
                    sixbuOperation__exact=2).count()
                tt = datetime.datetime.today() - datetime.timedelta(days=30)
                # count_0_month = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0, MGTime__gte=tt).count()
                count_1 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=1,
                                                                       StaffID__in=user_list).exclude(
                    sixbuOperation__exact=2).count()
                count_2 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=2,
                                                                       StaffID__in=user_list).exclude(
                    sixbuOperation__exact=2).count()
                count_3 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=3,
                                                                       StaffID__in=user_list).exclude(
                    sixbuOperation__exact=2).count()
                count_4 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__gt=3,
                                                                       StaffID__in=user_list).exclude(
                    sixbuOperation__exact=2).count()
                count_5 = t_product_enter_ed_aliexpress.objects.filter(sixbuOperation__exact=2,
                                                                       StaffID__in=user_list).count()
            if DepartmentID == '7':
                count_all = t_product_enter_ed_aliexpress.objects.filter(StaffID__in=user_list).count()
                count_0 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0,
                                                                       StaffID__in=user_list).exclude(
                    sevenbuOperation__exact=2).count()
                tt = datetime.datetime.today() - datetime.timedelta(days=30)
                # count_0_month = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0, MGTime__gte=tt).count()
                count_1 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=1,
                                                                       StaffID__in=user_list).exclude(
                    sevenbuOperation__exact=2).count()
                count_2 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=2,
                                                                       StaffID__in=user_list).exclude(
                    sevenbuOperation__exact=2).count()
                count_3 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=3,
                                                                       StaffID__in=user_list).exclude(
                    sevenbuOperation__exact=2).count()
                count_4 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__gt=3,
                                                                       StaffID__in=user_list).exclude(
                    sevenbuOperation__exact=2).count()
                count_5 = t_product_enter_ed_aliexpress.objects.filter(sevenbuOperation__exact=2,
                                                                       
                                                                       StaffID__in=user_list).count()
            if DepartmentID == '8':
                count_all = t_product_enter_ed_aliexpress.objects.filter(
                                                                         StaffID__in=user_list).count()
                count_0 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0,
                                                                       StaffID__in=user_list).exclude(
                    eightbuOperation__exact=2).count()
                tt = datetime.datetime.today() - datetime.timedelta(days=30)
                # count_0_month = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0, MGTime__gte=tt).count()
                count_1 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=1,
                                                                       StaffID__in=user_list).exclude(
                    eightbuOperation__exact=2).count()
                count_2 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=2,
                                                                       StaffID__in=user_list).exclude(
                    eightbuOperation__exact=2).count()
                count_3 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=3,
                                                                       StaffID__in=user_list).exclude(
                    eightbuOperation__exact=2).count()
                count_4 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__gt=3,
                                                                       StaffID__in=user_list).exclude(
                    eightbuOperation__exact=2).count()
                count_5 = t_product_enter_ed_aliexpress.objects.filter(eightbuOperation__exact=2,
                                                                       
                                                                       StaffID__in=user_list).count()

            if DepartmentID == '9':
                count_all = t_product_enter_ed_aliexpress.objects.filter(
                                                                         StaffID__in=user_list).count()
                count_0 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0,
                                                                       StaffID__in=user_list).exclude(
                    ninebuOperation__exact=2).count()
                tt = datetime.datetime.today() - datetime.timedelta(days=30)
                # count_0_month = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0, MGTime__gte=tt).count()
                count_1 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=1,
                                                                       StaffID__in=user_list).exclude(
                    ninebuOperation__exact=2).count()
                count_2 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=2,
                                                                       StaffID__in=user_list).exclude(
                    ninebuOperation__exact=2).count()
                count_3 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=3,
                                                                       StaffID__in=user_list).exclude(
                    ninebuOperation__exact=2).count()
                count_4 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__gt=3,
                                                                       StaffID__in=user_list).exclude(
                    ninebuOperation__exact=2).count()
                count_5 = t_product_enter_ed_aliexpress.objects.filter(ninebuOperation__exact=2,
                                                                       StaffID__in=user_list).count()

            if DepartmentID == '10':
                count_all = t_product_enter_ed_aliexpress.objects.filter(
                                                                         StaffID__in=user_list).count()
                count_0 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0,
                                                                       StaffID__in=user_list).exclude(
                    tenbuOperation__exact=2).count()
                tt = datetime.datetime.today() - datetime.timedelta(days=30)
                # count_0_month = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0, MGTime__gte=tt).count()
                count_1 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=1,
                                                                       StaffID__in=user_list).exclude(
                    tenbuOperation__exact=2).count()
                count_2 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=2,
                                                                       StaffID__in=user_list).exclude(
                    tenbuOperation__exact=2).count()
                count_3 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=3,
                                                                       StaffID__in=user_list).exclude(
                    tenbuOperation__exact=2).count()
                count_4 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__gt=3,
                                                                       StaffID__in=user_list).exclude(
                    tenbuOperation__exact=2).count()
                count_5 = t_product_enter_ed_aliexpress.objects.filter(tenbuOperation__exact=2,
                                                                       StaffID__in=user_list).count()

            if DepartmentID == '11':
                count_all = t_product_enter_ed_aliexpress.objects.filter(
                                                                         StaffID__in=user_list).count()
                count_0 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0,
                                                                       StaffID__in=user_list).exclude(
                    elevenbuOperation__exact=2).count()
                tt = datetime.datetime.today() - datetime.timedelta(days=30)
                # count_0_month = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0, MGTime__gte=tt).count()
                count_1 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=1,
                                                                       StaffID__in=user_list).exclude(
                    elevenbuOperation__exact=2).count()
                count_2 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=2,
                                                                       StaffID__in=user_list).exclude(
                    elevenbuOperation__exact=2).count()
                count_3 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=3,
                                                                       StaffID__in=user_list).exclude(
                    elevenbuOperation__exact=2).count()
                count_4 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__gt=3,
                                                                       StaffID__in=user_list).exclude(
                    elevenbuOperation__exact=2).count()
                count_5 = t_product_enter_ed_aliexpress.objects.filter(elevenbuOperation__exact=2,
                                                                       
                                                                       StaffID__in=user_list).count()

            if DepartmentID == '12':
                count_all = t_product_enter_ed_aliexpress.objects.filter(
                                                                         StaffID__in=user_list).count()
                count_0 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0,
                                                                       StaffID__in=user_list).exclude(
                    twelvebuOperation__exact=2).count()
                tt = datetime.datetime.today() - datetime.timedelta(days=30)
                # count_0_month = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0, MGTime__gte=tt).count()
                count_1 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=1,
                                                                       StaffID__in=user_list).exclude(
                    twelvebuOperation__exact=2).count()
                count_2 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=2,
                                                                       StaffID__in=user_list).exclude(
                    twelvebuOperation__exact=2).count()
                count_3 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=3,
                                                                       StaffID__in=user_list).exclude(
                    twelvebuOperation__exact=2).count()
                count_4 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__gt=3,
                                                                       StaffID__in=user_list).exclude(
                    twelvebuOperation__exact=2).count()
                count_5 = t_product_enter_ed_aliexpress.objects.filter(twelvebuOperation__exact=2,
                                                                       
                                                                       StaffID__in=user_list).count()
            if DepartmentID == '13':
                count_all = t_product_enter_ed_aliexpress.objects.filter(
                                                                         StaffID__in=user_list).count()
                count_0 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0,
                                                                       StaffID__in=user_list).exclude(
                    thirteenbuOperation__exact=2).count()
                tt = datetime.datetime.today() - datetime.timedelta(days=30)
                # count_0_month = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0, MGTime__gte=tt).count()
                count_1 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=1,
                                                                       StaffID__in=user_list).exclude(
                    thirteenbuOperation__exact=2).count()
                count_2 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=2,
                                                                       StaffID__in=user_list).exclude(
                    thirteenbuOperation__exact=2).count()
                count_3 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=3,
                                                                       StaffID__in=user_list).exclude(
                    thirteenbuOperation__exact=2).count()
                count_4 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__gt=3,
                                                                       StaffID__in=user_list).exclude(
                    thirteenbuOperation__exact=2).count()
                count_5 = t_product_enter_ed_aliexpress.objects.filter(thirteenbuOperation__exact=2,
                                                                       
                                                                       StaffID__in=user_list).count()
        else:
            publish_url = '/Project/admin/skuapp/t_product_enter_ed_wish?'
            count_all = t_product_enter_ed_aliexpress.objects.filter().count()
            count_0 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0).count()
            tt = datetime.datetime.today() - datetime.timedelta(days=30)
            # count_0_month = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=0,MGTime__gte=tt).count()
            count_1 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=1).count()
            count_2 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=2).count()
            count_3 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__exact=3).count()
            count_4 = t_product_enter_ed_aliexpress.objects.filter(Wish_count__gt=3).count()
            count_5 = t_product_enter_ed_aliexpress.objects.filter().filter(Q(onebuOperation__exact=2) | Q(twobuOperation__exact=2) | Q(threebuOperation__exact=2) | Q(fourbuOperation__exact=2) | Q(fivebuOperation__exact=2) | Q(sixbuOperation__exact=2) | Q(sevenbuOperation__exact=2) | Q(eightbuOperation__exact=2) | Q(ninebuOperation__exact=2) | Q(tenbuOperation__exact=2) | Q(elevenbuOperation__exact=2) | Q(twelvebuOperation__exact=2) | Q(thirteenbuOperation__exact=2)).count()

        datetype = self.request.GET.get('datetype')
        publish_url1 = publish_url + 'pub=1'+ '&datetype=%s'%datetype
        publish_url2 = publish_url + 'pub=2'+ '&datetype=%s'%datetype
        publish_url3 = publish_url + 'pub=3'+ '&datetype=%s'%datetype
        publish_url4 = publish_url + 'pub=4'+ '&datetype=%s'%datetype
        publish_url5 = publish_url + 'pub=5'+ '&datetype=%s'%datetype

        Wish_count = self.request.GET.get('pub')
        if Wish_count == '0':
            flag = '0'
        elif Wish_count == '1':
            flag = '1'
        elif Wish_count == '2':
            flag = '2'
        elif Wish_count == '3':
            flag = '3'
        elif Wish_count == '4':
            flag = '4'
        elif Wish_count == '5':
            flag = '5'
        else:
            flag = 'info_all'

        menu_list = [{
            "name": u"Wish刊登信息(%s)" % count_all,
            "code": "011",
            "icon": "icon-th",
            "parentCode": "",
            "selected": "",
            "to_url": "/Project/admin/skuapp/t_product_enter_ed_aliexpress/",
            "flag": "info_all",
            "child": [
                {
                    "name": u"刊登0次产品(%s)" % count_0,
                    "code": "0111",
                    "icon": "",
                    "parentCode": "011",
                    "selected": "",
                    "to_url": publish_url + 'pub=0'+ '&datetype=%s'%datetype,
                    "flag": "0",
                    "child": []
                },
                {
                    "name": u"刊登1次产品(%s)" % count_1,
                    "code": "0112",
                    "icon": "",
                    "parentCode": "011",
                    "selected": "",
                    "to_url": publish_url1,
                    "flag": "1",
                    "child": []
                },
                {
                    "name": u"刊登2次产品(%s)" % count_2,
                    "code": "0113",
                    "icon": "",
                    "parentCode": "011",
                    "selected": "",
                    "to_url": publish_url2,
                    "flag": "2",
                    "child": []
                },
                {
                    "name": u"刊登3次产品(%s)" % count_3,
                    "code": "0114",
                    "icon": "",
                    "parentCode": "011",
                    "selected": "",
                    "to_url": publish_url3,
                    "flag": "3",
                    "child": []
                },
                {
                    "name": u"刊登3次以上产品(%s)" % count_4,
                    "code": "0115",
                    "icon": "",
                    "parentCode": "011",
                    "selected": "",
                    "to_url": publish_url4,
                    "flag": "4",
                    "child": []
                },
                {
                    "name": u"本部门弃用(%s)" % count_5,
                    "code": "0116",
                    "icon": "",
                    "parentCode": "011",
                    "selected": "",
                    "to_url": publish_url5,
                    "flag": "5",
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
