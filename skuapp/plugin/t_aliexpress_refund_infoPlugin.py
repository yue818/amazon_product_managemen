# -*- coding: utf-8 -*-
import xadmin
import logging
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader
from skuapp.table.B_PackInfo import  *
from skuapp.table.b_goods import *


class t_aliexpress_refund_infoPlugin(BaseAdminPlugin):
    show_aliexpress_refund_info = False
    def init_request(self, *args, **kwargs):     
        return bool(self.show_aliexpress_refund_info)

    def block_after_fieldsets(self, context, nodes):
        nodes.append(loader.render_to_string('t_aliexpress_refund_infoPlugin.html'))
