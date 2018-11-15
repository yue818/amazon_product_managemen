# -*- coding: utf-8 -*-
import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader

#获取普源核价信息
class button_Plugin(BaseAdminPlugin):
    show_detail = False
    def init_request(self, *args, **kwargs):
        return bool(self.show_detail)
    def block_after_fieldsets(self, context, nodes):
        nodes.append(loader.render_to_string('button_Plugin.html',))
