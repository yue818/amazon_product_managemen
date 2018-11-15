# coding=utf-8


from xadmin.views import BaseAdminPlugin
from django.template import loader
from skuapp.table.t_online_info_wish import *
from django.db.models import Q
from django.contrib import messages
import logging


class import_joomPlugin(BaseAdminPlugin):
    import_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.import_flag)

    def get_media(self, media):
        media.add_js([self.static('xadmin/js/xadmin.plugin.button.color.js')])
        return media

    def block_search_cata_nav(self, context, nodes):

        nodes.append(loader.render_to_string('import_joom.html',{}))