# -*- coding: utf-8 -*-
import xadmin
import logging
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader


class tort_Plugin(BaseAdminPlugin):
    show_tort = False
    def init_request(self, *args, **kwargs):     
        return bool(self.show_tort)

    def block_search_cata_nav(self, context, nodes):

        nodes.append(loader.render_to_string('tort_Plugin.html'))
