#-*-coding:utf-8-*-


import json
from xadmin.views import BaseAdminPlugin
from django.template import loader
from skuapp.table.t_store_configuration_file import t_store_configuration_file

class t_trademark_copyright_plugin(BaseAdminPlugin):
    registration_recipients_menu = False

    def init_request(self, *args, **kwargs):
        return bool(self.registration_recipients_menu)

    def block_search_cata_nav(self, context, nodes):

        t = self.request.GET.get('datetype', '')

        activeflag = t if t else '0'

        nodes.append(loader.render_to_string('t_trademark_copyright.html',
                                             {'activeflag': activeflag }))