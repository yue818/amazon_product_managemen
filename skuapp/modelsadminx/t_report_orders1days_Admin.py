# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.safestring import mark_safe
from skuapp.table.t_online_info import *

class t_report_orders1days_Admin(object):
    list_display=('id','YYYYMMDD','PlatformName','ShopName','ProductID','OrdersLast1Days','OrdersLast7Days','UpdateTime',)
    #readonly_fields = ('id',)
    list_display_links = list_display

    search_fields=('id','YYYYMMDD','PlatformName','ShopName','ProductID','OrdersLast1Days','OrdersLast7Days',)
    list_filter = ('PlatformName','ShopName','ProductID','OrdersLast1Days','OrdersLast7Days','UpdateTime',)
    data_charts = {
        "产品Order数": {'title': u"产品Order数", "x-field": "YYYYMMDD", "y-field": ("OrdersLast1Days","OrdersLast7Days"), "order": ('YYYYMMDD',)}
    }
