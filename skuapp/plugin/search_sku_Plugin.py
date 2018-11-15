# -*- coding: utf-8 -*-
import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader

class search_sku_Plugin(BaseAdminPlugin):
    show_sku = False
    def init_request(self, *args, **kwargs):
        return bool(self.show_sku)
    def block_after_fieldsets(self, context, nodes):
        nodes.append(loader.render_to_string('search_sku_Plugin.html',))