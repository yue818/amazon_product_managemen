# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: amazon_inventory_type_Plugin.py
 @time: 2018-06-23 14:38
"""  
# -*- coding: utf-8 -*-

from xadmin.views import BaseAdminPlugin
from django.template import loader


class amazon_inventory_type(BaseAdminPlugin):
    amazon_inventory_type_plugin = False

    def init_request(self, *args, **kwargs):
        return bool(self.amazon_inventory_type_plugin)

    def block_search_cata_nav(self, context, nodes):

        nodes.append(loader.render_to_string('amazon_inventory_type.html',
                                             {'inventory_type': activeflag}))
