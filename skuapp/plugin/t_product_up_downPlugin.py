# -*- coding: utf-8 -*-
import xadmin
import logging
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader
from skuapp.table.B_PackInfo import  *
from skuapp.table.b_goods import *


class t_product_up_downPlugin(BaseAdminPlugin):
    show_search_sku = False
    def init_request(self, *args, **kwargs):     
        return bool(self.show_search_sku)

    def block_after_fieldsets(self, context, nodes):
        nodes.append(loader.render_to_string('t_product_up_downPlugin.html'))
