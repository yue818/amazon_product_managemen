# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: importfile_stocking_demand_plugin.py
 @time: 2017-12-25 16:27

"""
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.template import RequestContext
import logging

logger = logging.getLogger('sourceDns.webdns.views')
from django.contrib import messages


class importfile_stocking_demand_plugin(BaseAdminPlugin):
    importfile_plugin = False

    def init_request(self, *args, **kwargs):
        return bool(self.importfile_plugin)

    def block_search_cata_nav(self, context, nodes):
        sourceURL = str(context['request']).split("'")[1]
        #messages.info(self.request,sourceURL)
        if "/Project/admin/skuapp/t_stocking_demand_fbw" in sourceURL:
            nodes.append(loader.render_to_string('importfile.html',{'dealFlag': 'FBW'},context_instance=RequestContext(self.request)))
        elif "/Project/admin/skuapp/t_stocking_demand_fba/?Status=notgenpurchase" in sourceURL:
            nodes.append(loader.render_to_string('importfile.html',{'dealFlag': 'FBA'},context_instance=RequestContext(self.request)))
        elif "/Project/admin/skuapp/t_stocking_reject_fba/?Status=reject" in sourceURL:
            nodes.append(loader.render_to_string('importfile.html',{'dealFlag': 'FBAREJECT'},context_instance=RequestContext(self.request)))
        elif "/Project/admin/skuapp/t_saler_profit_config" in sourceURL:
            nodes.append(loader.render_to_string('importfile.html',{'dealFlag': 'SALERPROFITCONFIG'},context_instance=RequestContext(self.request)))
        elif "/Project/admin/skuapp/t_cloth_factory_dispatch_needpurchase" in sourceURL:
            nodes.append(loader.render_to_string('importfile.html',{'dealFlag': 'CLOTHFACTORY'},context_instance=RequestContext(self.request)))
        elif "/Project/admin/reportapp/t_online_aliexpress_affiliate_rate" in sourceURL:
            nodes.append(loader.render_to_string('importfile.html',{'dealFlag': 'AFFILIATE'},context_instance=RequestContext(self.request)))
        else:
            nodes.append(loader.render_to_string('importfile.html',{'dealFlag': 'OTHER'},context_instance=RequestContext(self.request)))