# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.safestring import mark_safe
from skuapp.table.t_trans_order_ebay import *

class t_report_ebay_orders1days_Admin(object):
    list_display=('id','YYYYMMDD','itemid','ShopName','Platform','OrdersLast1Days','OrdersLast7Days',)
    list_display_links = list_display

    search_fields=('id','YYYYMMDD','itemid','OrdersLast1Days','OrdersLast7Days',)
    list_filter = ('itemid','OrdersLast1Days','OrdersLast7Days')
    data_charts = {
        "产品Order数": {'title': u"产品Order数", "x-field": "YYYYMMDD", "y-field": ("OrdersLast1Days","OrdersLast7Days"), "order": ('YYYYMMDD',)}
    }
