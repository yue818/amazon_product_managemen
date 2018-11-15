# -*- coding: utf-8 -*-
#该插件获取页面的主sku 判断是否有重复的sku
import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader
class repeat_sku_Plugin(BaseAdminPlugin):
    repeat_sku = False
    def init_request(self, *args, **kwargs):
        return bool(self.repeat_sku)
    def block_after_fieldsets(self, context, nodes):
        nodes.append(loader.render_to_string('repeat_sku_plugin.html',))