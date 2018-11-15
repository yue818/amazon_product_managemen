# coding=utf-8
# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from skuapp.table.t_config_mstsc import t_config_mstsc
from skuapp.table.t_wish_honor import t_wish_honor
from django.db import transaction, connection
from .t_product_Admin import *
from django.contrib import messages


class t_wish_honorShop_Admin(object):
    # top_top_navbar = False
    show_report = False
    actions = ['show_wish_honor', ]

    def show_wish_honor(self, request, queryset):
        from app_djcelery.tasks import show_wish_honor as xx
        for querysetid in queryset.all():
            xx.delay(querysetid.ip, 0)
    show_wish_honor.short_description = u'手动刷新诚信店铺'

    def wish_honor_list(self, obj):
        from django.db import connection
        rt=''
        rt = '%s<br><input type="button" value="查看诚信店铺" onclick="{window.open(\'/Project/admin/skuapp/t_wish_honor/?_p_ShopNameOfficial=%s\') }" target="_blank" />' % (rt,obj.ShopName)

        return mark_safe(rt)

    wish_honor_list.short_description = u'查看诚信店铺列表'

    # list_per_page=2000
    # list_display=('id','PlatformName','ShopName','show_user','DepartmentName','show_status','show_CloudName','login_DP')
    list_display = (
    'id','ip', 'ShopName', 'seller','PlatformName', 'wish_honor_list', )
    readonly_fields = (
    'id','ip', 'ShopName', 'seller')
    search_fields = ('ip', 'ShopName', 'seller')

    def get_list_queryset(self):
        request = self.request
        qs = super(t_wish_honorShop_Admin, self).get_list_queryset()
        if request.user.is_superuser:
            return qs
        return qs.filter(seller=request.user.username)

