# -*- coding:utf-8 -*-


"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_auto_load_Admin.py
 @time: 2018/11/2 15:43
"""
from django.utils.safestring import mark_safe


class t_amazon_auto_load_Admin(object):
    amazon_site_left_menu_tree_flag = True

    def show_sku_detail(self, obj):
        if obj.com_pro_sku:
            com_sku_html = u"<br>组合商品SKU: %s" % obj.com_pro_sku
        else:
            com_sku_html = ''
        sku_detail = u"商品SKU: %s %s<br>链接状态：%s" % (obj.sku, com_sku_html, obj.status)
        return mark_safe(sku_detail)

    show_sku_detail.short_description = mark_safe('<p align="center"style="color:#428bca;">商品SKU</p>')

    list_display = ('shop_name', 'seller_sku', 'status', 'insert_time', 'deal_type', 'deal_user', 'deal_result', 'deal_remark','deal_time')
    search_fields = ('shop_name', 'seller_sku', 'insert_time', 'deal_type', 'deal_user','deal_result')
    list_filter = ('shop_name', 'seller_sku', 'insert_time', 'deal_type', 'deal_user','deal_result')