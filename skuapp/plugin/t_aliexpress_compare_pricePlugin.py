# -*- coding: utf-8 -*-
import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from skuapp.table.t_product_mainsku_sku import *
from django.template import loader
from skuapp.table.t_aliexpress_compare_price import t_aliexpress_compare_price
from datetime import datetime
from django.http import HttpResponseRedirect
class t_aliexpress_compare_pricePlugin(BaseAdminPlugin):
    aliexpress_compare_price = False
    # 初始化方法根据 ``enter_ed`` 属性值返回
    def init_request(self, *args, **kwargs):
        return bool(self.aliexpress_compare_price)

    def block_nav_form(self, context, nodes):
        # 可以将 HTML 片段加入 nodes 参数中
        nodes.append(loader.render_to_string('ali_compare_price.html', context_instance=context))