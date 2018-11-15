# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: jump_temp_some_page.py
 @time: 2018-01-04 15:01

"""   
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.template import RequestContext
import logging

from skuapp.table.public import *

logger = logging.getLogger('sourceDns.webdns.views')
from django.contrib import messages


class jump_temp_some_page(BaseAdminPlugin):
    jump_temp = False

    def init_request(self, *args, **kwargs):
        return bool(self.jump_temp)

    def block_search_cata_nav(self, context, nodes):
        # models_objs = (u'%s'%context['request']).split('/')
        # if models_objs[1] == 'Project' and models_objs[2] == 'admin':
        #     modelname = models_objs[4]
        # elif models_objs[1] == 'xadmin':
        #     modelname = models_objs[3]

        # logger.info('models_objs====%s',models_objs)
        button_objs = getChoices(eval('Jump_'+ self.model._meta.model_name))
        buttondict = {}
        buttonlist = []
        for button_obj in button_objs:
            if len(button_obj) == 2 and button_obj[0] is not None and button_obj[0].strip() != '' and button_obj[1] is not None and button_obj[1].strip() != '':
                buttondict[button_obj[1]] = button_obj[0]
                buttonlist.append(button_obj[1])
            #buttondict2={'备货需求':'/Project/admin/skuapp/t_stocking_demand_list/','采购计划':'/Project/admin/skuapp/t_stocking_purchase_order/','库存一栏':'/Project/admin/skuapp/t_set_warehouse_storage_situation_list/','发货管理':'/Project/admin/skuapp/t_shipping_management/'}
        nodes.append(loader.render_to_string('purchase_order_button.html',{'objs':buttondict,'list':buttonlist},context_instance=RequestContext(self.request)))