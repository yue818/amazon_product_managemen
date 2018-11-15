# -*- coding: utf-8 -*-
from .t_product_Admin import *
from skuapp.table.t_product_mainsku_sku import *
import logging


class t_aliexpress_compare_price_Admin(object):
    aliexpress_compare_price = True
    list_display_links = ('',)

    def show_df_OurProductID(self, obj):
        rt = u'<a href="https://www.aliexpress.com/item/abc/%s.html" target="_blank">%s</a>' %(obj.OurProductID,obj.OurProductID)
        return mark_safe(rt)
    show_df_OurProductID.short_description = u'<span style="color: #428bca">我方ProductID</span>'

    def show_wf_OppositeProductID(self, obj):
        rt = u'<a href="https://www.aliexpress.com/item/abc/%s.html" target="_blank">%s</a>' %(obj.OppositeProductID,obj.OppositeProductID)
        return mark_safe(rt)
    show_wf_OppositeProductID.short_description = u'<span style="color: #428bca">对方ProductID</span>'

    list_display = ('id','show_df_OurProductID','OurMainSKU','OurSales','OurWeekSales','OurPrice','show_wf_OppositeProductID','OppositeSales','OppositeWeekSales','OppositePrice','QueryTime')