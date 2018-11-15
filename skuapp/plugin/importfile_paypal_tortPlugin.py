# -*- coding: utf-8 -*-

from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.template import RequestContext
import logging

logger = logging.getLogger('sourceDns.webdns.views')
from django.contrib import messages


class importfile_paypal_tortPlugin(BaseAdminPlugin):
    importfile_plugin2 = False

    def init_request(self, *args, **kwargs):
        return bool(self.importfile_plugin2)

    def block_search_cata_nav(self, context, nodes):

        nodes.append(loader.render_to_string('importfile_paypal_tort.html',context_instance=RequestContext(self.request)))