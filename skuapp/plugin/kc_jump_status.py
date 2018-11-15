# -*- coding: utf-8 -*-
import xadmin
import logging
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader
from skuapp.table.B_PackInfo import  *
from skuapp.table.b_goods import *
from skuapp.table.t_product_inventory_warnning import  *


#获取普源核价信息
class kc_jump_status(BaseAdminPlugin):
    kc_jump = False
    def init_request(self, *args, **kwargs):     
        return bool(self.kc_jump)
        
    def get_media(self, media):
        media.add_js([self.static('xadmin/js/xadmin.plugin.button.color.js')])
        return media

    def block_search_cata_nav(self, context, nodes):
        strUrl = str(context['request']).split("'")[1]
        flag = 1
        if strUrl.find('?') != -1 :
            if strUrl.find('handleResults') != -1 :
                handleResults = (strUrl.split('handleResults=')[1]).split('&')[0]
                strUrl = strUrl + '&'
                if handleResults=='Y':
                    strUrl = strUrl.replace('handleResults=Y&','')
                    flag = 2
                elif handleResults=='W':
                    strUrl = strUrl.replace('handleResults=W&','')
                    flag = 3
                elif handleResults=='H':
                    strUrl = strUrl.replace('handleResults=H&','')
                    flag = 4
                else:
                    flag = 1
            else:
                strUrl = strUrl + '&'
        else:
            strUrl = strUrl + '?'
        nodes.append(loader.render_to_string('kc_jump.html',
                                             { 'strUrl': strUrl, 'flag': flag}))