# -*- coding: utf-8 -*-
import xadmin
import logging
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader


class t_tort_wishPlugin(BaseAdminPlugin):
    show_tort_wish = False
    def init_request(self, *args, **kwargs):     
        return bool(self.show_tort_wish)

    def block_search_cata_nav(self, context, nodes):

        nodes.append(loader.render_to_string('tort_wishPlugin.html'))
