# -*- coding: utf-8 -*-
import xadmin
import logging
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader
from skuapp.table.B_PackInfo import  *
from skuapp.table.b_goods import *

#获取普源核价信息
class t_online_info_logisticPlugin(BaseAdminPlugin):
    show_yj = False
    def init_request(self, *args, **kwargs):     
        return bool(self.show_yj)

    def block_search_cata_nav(self, context, nodes):
        sourceURL = str(context['request']).split("'")[1]
        searchList = {}
        param_seach = ''
		
        newurl = ''
        if sourceURL.find('?_p_LogisticInfo=') != -1:
            flag = 1
        else:
            flag = 0
        nodes.append(loader.render_to_string('t_online_info_logisticPlugin.html'))
