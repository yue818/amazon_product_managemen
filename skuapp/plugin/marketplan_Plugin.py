# -*- coding: utf-8 -*-
import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader


class marketplan_Plugin(BaseAdminPlugin):
    show_cc_flag = False
    def init_request(self, *args, **kwargs):
        return bool(self.show_cc_flag)
    def block_search_cata_nav(self, context, nodes):
        nodes.append(loader.render_to_string('marketplan_Plugin.html',))
