# -*- coding: utf-8 -*-
import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader

class t_product_suringPlugin(BaseAdminPlugin):
    suring_plugin = False
    def init_request(self, *args, **kwargs):
        return bool(self.suring_plugin)
    def block_luru(self, context, nodes):
        nodes.append(loader.render_to_string('t_product_suringPlugin.html',))