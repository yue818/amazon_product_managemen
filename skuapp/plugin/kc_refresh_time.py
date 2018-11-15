# -*- coding: utf-8 -*-
import xadmin
import logging
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader
from skuapp.table.t_product_inventory_warnning import t_product_inventory_warnning
from django.contrib.auth.models import User
from django.contrib import messages

class kc_refresh_time(BaseAdminPlugin):
    show_kc_refresh = False
    
    def init_request(self, *args, **kwargs):     
        return bool(self.show_kc_refresh)
        
    def block_search_cata_nav(self, context, nodes): 
        kc_refresh_time_objs = t_product_inventory_warnning.objects.values_list('insertTime',flat=True)
        for time in kc_refresh_time_objs:
            kc_refresh_time = time 
            break
        nodes.append(loader.render_to_string('kc_refresh_time.html',{'kc_refresh_time': kc_refresh_time}))
            