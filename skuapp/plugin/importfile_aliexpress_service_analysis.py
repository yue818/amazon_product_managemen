# -*- coding: utf-8 -*-

from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.template import RequestContext
import logging

logger = logging.getLogger('sourceDns.webdns.views')
from django.contrib import messages


class importfile_aliexpress_service_analysis(BaseAdminPlugin):
    importfile_aliexpress_plugin = False

    def init_request(self, *args, **kwargs):
        return bool(self.importfile_aliexpress_plugin)

    def block_search_cata_nav(self, context, nodes):
        nodes.append(loader.render_to_string('aliexpress_service_upload.html','',context_instance=RequestContext(self.request)))