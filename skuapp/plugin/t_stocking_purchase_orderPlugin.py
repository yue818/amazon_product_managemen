# -*- coding: utf-8 -*-
import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader
from django.contrib import messages
from django.template import RequestContext

class t_stocking_purchase_orderPlugin(BaseAdminPlugin):
    purchase_order_plugin = False
    def init_request(self, *args, **kwargs):
        return bool(self.purchase_order_plugin)
    def block_luru(self, context, nodes):
        current_url = self.request.get_full_path()
        dealpage = 'OTHER'
        if 't_stocking_demand_fba_purchase' in current_url and 'Status=purchasing' in current_url:
            dealpage = 'FBA'
            nodes.append(loader.render_to_string('t_stocking_purchase_order.html',{'dealpage': dealpage},context_instance=RequestContext(self.request) ))
        else:
            nodes.append(loader.render_to_string('t_stocking_purchase_order.html',{'dealpage': dealpage},context_instance=RequestContext(self.request) ))