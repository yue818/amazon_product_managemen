# -*- coding: utf-8 -*-
import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from skuapp.table.t_product_mainsku_sku import *
from django.template import loader


class t_product_enter_edPlugin(BaseAdminPlugin):
    enter_ed = False
    object_id = 0
    # 初始化方法根据 ``enter_ed`` 属性值返回
    def init_request(self, *args, **kwargs):
        return bool(self.enter_ed)
    def block_after_fieldsets(self, context, nodes):
        #加载子SKU信息
        t_product_mainsku_sku_objs = None
        t_product_mainsku_sku_objs_count =0
        if context['original']  is  not None :
            t_product_mainsku_sku_objs = t_product_mainsku_sku.objects.filter(pid=context['object_id']).order_by('SKU')
            t_product_mainsku_sku_objs_count = t_product_mainsku_sku_objs.count()
        nodes.append(loader.render_to_string('t_product_sku.html', {'t_product_mainsku_sku_objs': t_product_mainsku_sku_objs,'t_product_mainsku_sku_objs_count': t_product_mainsku_sku_objs_count}))

