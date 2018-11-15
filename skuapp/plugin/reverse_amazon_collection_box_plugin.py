# -*- coding: utf-8 -*-

from xadmin.views import BaseAdminPlugin
from django.template import loader
from skuapp.table.t_sys_param import t_sys_param


class reverse_amazon_collection_box_plugin(BaseAdminPlugin):
    reverse_amazon_collection = False

    def init_request(self, *args, **kwargs):
        return bool(self.reverse_amazon_collection)

    def block_search_cata_nav(self, context, nodes):
        site_list = []
        t_sys_param_objs = t_sys_param.objects.filter(TypeDesc='ChoiceSiteconfiguration').order_by('id')
        for obj in t_sys_param_objs:
            if obj.V != 'ALL':
                site_list.append({obj.V: obj.VDesc})

        nodes.append(loader.render_to_string('reverse_amazon_collection_box.html',{'site_list':site_list}))
