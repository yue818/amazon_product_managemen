# coding=utf-8
import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader
class Main_SKU_countplugin(BaseAdminPlugin):
    sku_count = False
    def init_request(self, *args, **kwargs):
        return bool(self.sku_count)
    def block_search_cata_nav(self, context, nodes):
        nodes.append(loader.render_to_string('Main_SKU_countplugin.html',))


