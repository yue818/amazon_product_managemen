# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_product_cost_refresh_plugin.py
 @time: 2018/9/7 11:14
"""
from xadmin.views import BaseAdminPlugin
from django.template import loader


class t_amazon_product_cost_refresh_plugin(BaseAdminPlugin):
    amazon_product_cost_refresh_plugin = False

    def init_request(self, *args, **kwargs):
        return bool(self.amazon_product_cost_refresh_plugin)

    def block_search_cata_nav(self, context, nodes):
        if 't_amazon_product_inventory_cost' in self.request.get_full_path():
            refresh_type = 'inventory_cost'
        elif 't_amazon_product_remove_cost' in self.request.get_full_path():
            refresh_type = 'remove_cost'
        elif 't_amazon_product_order_pend_cost' in self.request.get_full_path():
            refresh_type = 'pend_cost'
        elif 't_amazon_orders_by_receive_day_total' in self.request.get_full_path():
            refresh_type = 'orders_by_receive_day'
        elif 't_amazon_conversion_result' in self.request.get_full_path():
            refresh_type = 'conversion_result'
        else:
            refresh_type = ''

        nodes.append(loader.render_to_string('t_amazon_product_cost_refresh_plugin.html', {'refresh_type': refresh_type, }))