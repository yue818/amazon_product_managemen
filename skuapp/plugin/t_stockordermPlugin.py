# -*- coding: utf-8 -*-
import xadmin
import logging
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader
from django.contrib import messages
from pyapp.models import t_stockorderm
#获取普源核价信息
class t_stockordermPlugin(BaseAdminPlugin):
    show_warning = False
    def init_request(self, *args, **kwargs):     
        return bool(self.show_warning)
        
    def get_media(self, media):
        media.add_js([self.static('xadmin/js/xadmin.plugin.button.color.js')])
        return media
        
    def block_search_cata_nav(self, context, nodes):
        sourceURL = str(context['request']).split("'")[1]
        flag = 0
        if '_p_WarningFlag__contains=1' in sourceURL:
            flag = 1
        elif '_p_WarningFlag__contains=2' in sourceURL:
            flag = 2
        elif '_p_WarningFlag__contains=3' in sourceURL:
            flag = 3
        elif '_p_WarningFlag__contains=4' in sourceURL:
            flag = 4
        elif '_p_WarningFlag__contains=5' in sourceURL:
            flag = 5
        elif '_p_WarningFlag__contains=6' in sourceURL:
            flag = 6
        refreshTime = t_stockorderm.objects.all()[:1]
        nodes.append(loader.render_to_string('t_stockordermPlugin.html',{'flag':flag,'refreshTime':refreshTime[0].refreshTime}))
