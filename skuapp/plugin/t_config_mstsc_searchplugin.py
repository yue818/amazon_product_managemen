# -*- coding: utf-8 -*-
import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader
class t_config_Search_Plugin(BaseAdminPlugin):
    t_config_Plugin = False
    def init_request(self, *args, **kwargs):
        return bool(self.t_config_Plugin)
    def block_search_cata_nav(self, context, nodes):
        nodes.append(loader.render_to_string('t_config_mstsc_searchplugin.html',))