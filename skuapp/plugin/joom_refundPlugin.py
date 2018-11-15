# -*- coding: utf-8 -*-

from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.template import RequestContext
import logging

logger = logging.getLogger('sourceDns.webdns.views')
from django.contrib import messages


class joom_refundPlugin(BaseAdminPlugin):
    joom_refund_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.joom_refund_flag)

    def block_search_cata_nav(self, context, nodes):

        nodes.append(loader.render_to_string('joom_refund.html',context_instance=RequestContext(self.request)))