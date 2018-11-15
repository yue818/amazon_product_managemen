#-*-coding:utf-8-*-
from django.utils.safestring import mark_safe
from django.contrib import messages
import logging,json, re, time
import xadmin
from aliapp.models import *

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_erp_aliexpress_shop_info_Admin.py
 @time: 2018/7/2 14:38
"""   
class t_erp_aliexpress_shop_info_Admin(object):
    site_left_menu_tree_flag_ali = True

    search_box_flag = True

    def show_accountName(self, obj):
        rt = '<a href="/Project/admin/aliapp/t_erp_aliexpress_online_info/?accountName=%s">%s</a>'%(obj.accountName,obj.accountName)
        return  mark_safe(rt)
    show_accountName.short_description = mark_safe(u'<p align="center"style="color:#428bca;">店铺账号</p>')

    def show_status(self, obj):
        shop_status = {"online": u'在用', "offline": u'停用'}
        rt = shop_status[obj.shop_status]
        return mark_safe(rt)

    show_status.short_description = mark_safe(u'<p align="center"style="color:#428bca;">店铺状态</p>')

    list_display = ('shopName', 'show_accountName', 'sessionkey', 'session_create_time', 'session_out_time', 'seller_zh', 'cata_zh', 'show_status')

    list_display_links = ('shopName',)

    def get_list_queryset(self,):
        """显示可显示的，自己本人的"""
        from skuapp.table.t_sys_staff_auth import t_sys_staff_auth
        flag = 0
        try:
            flag = t_sys_staff_auth.objects.filter(StaffID=self.request.user.username,urltable="t_erp_aliexpress_online_info").count()
        except:
            pass
        request = self.request
        qs = super(t_erp_aliexpress_shop_info_Admin, self).get_list_queryset()
        if self.request.user.is_superuser or flag != 0:
            pass
        else:
            print self.request.user.first_name
            qs = qs.filter(seller_zh=self.request.user.first_name)
        shopName = request.GET.get('shopName', '')
        accountName = request.GET.get('accountName', '')
        seller_zh = request.GET.get('seller_zh', '')
        searchList = {'shopName__contains': shopName, 'accountName__exact': accountName,
                      'seller_zh__exact': seller_zh,
                      }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')
        return qs.order_by("-shop_status","session_out_time")