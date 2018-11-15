# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: wangzy
 @site: 
 @software: PyCharm
 @file: importfile_marketing_plugin.py
 @time: 2018-06-04 16:27

"""
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.template import RequestContext
import logging

logger = logging.getLogger('sourceDns.webdns.views')
from django.contrib import messages


class importfile_marketing_Plugin(BaseAdminPlugin):
    importfile_marketing = False

    def init_request(self, *args, **kwargs):
        return bool(self.importfile_marketing)

    def block_search_cata_nav(self, context, nodes):
        nodes.append(loader.render_to_string('importfile_marketing.html',context_instance=RequestContext(self.request)))