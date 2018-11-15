# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_shop_refund_status_Admin.py
 @time: 2018/10/24 14:31
"""


class t_amazon_shopsku_modify_Admin(object):
    amazon_site_left_menu_tree_flag = True
    list_display = ('shop_name', 'all_order', 'refund_order', 'refund_rate', 'refresh_time')
    search_fields = ('shop_name', 'all_order', 'refund_order', 'refund_rate', 'refresh_time')
    list_filter = ('shop_name', 'all_order', 'refund_order', 'refund_rate', 'refresh_time')
