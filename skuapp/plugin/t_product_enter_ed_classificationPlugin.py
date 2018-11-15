# -*- coding: utf-8 -*-
import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader
from skuapp.table.t_product_enter_ed import *
from django.db.models import Q
import logging
from skuapp.table.t_sys_department_staff import *
from skuapp.table.t_product_depart_get import *
from django.contrib import messages

class t_product_enter_ed_classificationPlugin(BaseAdminPlugin):
    enter_ed_classification = False

    def init_request(self, *args, **kwargs):
        return bool(self.enter_ed_classification)

    def get_media(self, media):
        media.add_js([self.static('xadmin/js/xadmin.plugin.button.color.js')])
        return media

    def block_search_cata_nav(self, context, nodes):
        url = self.request.get_full_path()

        strUrl = str(context['request']).split("'")[1]
        flag = 3
        if strUrl.find('?') != -1 :
            if strUrl.find('classCloth') != -1 :
                classCloth = (strUrl.split('classCloth=')[1]).split('&')[0]
                strUrl = strUrl + '&'
                if classCloth=='1':
                    strUrl = strUrl.replace('classCloth=1&','')
                    flag = 1
                elif classCloth=='2':
                    strUrl = strUrl.replace('classCloth=2&','')
                    flag = 2
                else:
                    strUrl = strUrl.replace('classCloth=3&','')
            else:
                strUrl = strUrl + '&'
        else:
            strUrl = strUrl + '?'

        page = ''
        if 't_product_information_modify' in url:
            page = 'information_modify'

        nodes.append(loader.render_to_string('t_product_enter_ed_classificationPlugin.html',
                                             { 'strUrl': strUrl, 'flag': flag, 'page': page}))