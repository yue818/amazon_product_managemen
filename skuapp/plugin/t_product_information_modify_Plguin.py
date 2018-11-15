# coding=utf-8

from xadmin.views import BaseAdminPlugin
from django.template import loader


class t_product_information_modify_Plugin(BaseAdminPlugin):
    information_modify_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.information_modify_flag)

    def block_search_cata_nav(self, context, nodes):
        nodes.append(loader.render_to_string('t_product_information_modify.html'))