# coding=utf-8
# coding=utf-8
# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from skuapp.table.t_config_mstsc import t_config_mstsc
from skuapp.table.t_wish_honor import t_wish_honor
from django.db import transaction, connection
from .t_product_Admin import *
from django.contrib import messages


class t_wish_pbShop_Admin(object):
    # top_top_navbar = False
    show_report = False
    actions = ['show_wish_pb',]

    def show_wish_pb(self, request, queryset):
        from app_djcelery.tasks import show_wish_pb as xx
        for querysetid in queryset.all():
            xx.delay(querysetid.ip, 0)
    show_wish_pb.short_description = u'手动刷新店铺广告'

    def show_Activity(self,obj):
        rt='<br><input type="button" value="查看活动列表" onclick="window.open(\'/Project/admin/skuapp/v_wish_pb/?_p_ShopName=%s\')" <br>'%(obj.ShopName)
        return mark_safe(rt)
    show_Activity.short_description = u'店铺活动列表'
    # list_per_page=2000
    # list_display=('id','PlatformName','ShopName','show_user','DepartmentName','show_status','show_CloudName','login_DP')
    list_display = (
    'id', 'ip', 'ShopName', 'seller', 'PlatformName','show_Activity', )
    readonly_fields = (
    'id','ip', 'ShopName', 'seller')
    search_fields = ('ip', 'ShopName', 'seller')

    def get_list_queryset(self):
        request = self.request
        qs = super(t_wish_pbShop_Admin, self).get_list_queryset()
        if request.user.is_superuser:
            return qs
        return qs.filter(seller=request.user.username)

