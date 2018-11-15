# coding=utf-8

from xadmin.views import BaseAdminPlugin
from django.template import loader
from skuapp.table.t_online_info_wish import *
from django.db.models import Q
from django.contrib import messages
import logging
from urllib import unquote


class t_product_udPlugin(BaseAdminPlugin):
    show_type_product = False

    def init_request(self, *args, **kwargs):
        return bool(self.show_type_product)

    def get_media(self, media):
        media.add_js([self.static('xadmin/js/xadmin.plugin.button.color.js')])
        return media

    def block_search_cata_nav(self, context, nodes):
        sourceURL = str(context['request']).split("'")[1]

        paramList = ['&status=down','&status=up','&status=cleardown','&status=selldown',
                     'status=down&','status=up&','status=cleardown&','status=selldown&',
                     'status=down','status=up','status=cleardown','status=selldown',]

        if 'status=down' in sourceURL:
            flag = 1
        elif 'status=up' in sourceURL:
            flag = 2
        elif 'status=cleardown' in sourceURL:
            flag = 3
        elif 'status=selldown' in sourceURL:
            flag = 4
        else:
            flag = 0

        oldUrl = sourceURL
        if '?' in oldUrl:
            newFlag = True
            for param in paramList:
                if param in oldUrl:
                    oldUrl = oldUrl.replace(param,'')
                    newFlag = False
                    if oldUrl.split('?')[1] == '':
                        oldUrl = oldUrl
                    else:
                        oldUrl = oldUrl + '&'
            if(newFlag):
                oldUrl = oldUrl + '&'
        else:
            oldUrl = oldUrl + '?'

        nodes.append(loader.render_to_string('t_product_udPlugin.html',
                                             {'url':oldUrl, 'flag':flag,}))
