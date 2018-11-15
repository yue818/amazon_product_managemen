# -*- coding: utf-8 -*-

import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader
from skuapp.table.t_product_inventory_warnning import  *
from skuapp.table.t_product_inventory_warnning_dead import  *
from skuapp.table.t_product_inventory_warnning_stocking import *
from django.db.models import Q
import logging
from django.contrib import messages

class kc_current_stockPlugin(BaseAdminPlugin):
    show_kc = False

    def init_request(self, *args, **kwargs):
        return bool(self.show_kc)

    def get_media(self, media):
        media.add_js([self.static('xadmin/js/xadmin.plugin.button.color.js')])
        return media

    def block_search_cata_nav(self, context, nodes):
        sourceURL = str(context['request']).split("'")[1]

        flag = 0
        result = {}

        KC = [{'t_product_inventory_warnning':{'flag':1, 'name':u'库存预警'}},
                {'t_product_inventory_warnning_dead':{'flag':2, 'name':u'死库处理'}},
                {'t_product_inventory_warnning_stocking':{'flag':3, 'name':u'备货策略'}}
               ]

        plateform = [KC]

        for each_plate in plateform:
            for each_model in each_plate:
                for k, v in each_model.items():
                    if k in sourceURL:
                        result = each_plate
                        flag = v['flag']
                        break
                if flag != 0:
                    break
            if flag != 0:
                break

        nodes.append(loader.render_to_string('kc_currentstock.html', {'flag':flag, 'result':result}))