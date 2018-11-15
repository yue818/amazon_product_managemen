# coding=utf-8

from xadmin.views import BaseAdminPlugin
from django.template import loader
from skuapp.table.t_online_info_wish import *
from django.db.models import Q
from django.contrib import messages
import logging
from urllib import unquote


class wish_search_barPlugin(BaseAdminPlugin):
    search_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.search_flag)

    def get_media(self, media):
        media.add_js([self.static('xadmin/js/xadmin.plugin.button.color.js')])
        return media

    def block_search_cata_nav(self, context, nodes):
        sourceURL = str(context['request']).split("'")[1]

        paramList = ['&status=online','&status=offline','&status=reject',
                     'status=online&','status=offline&','status=reject&',
                     'status=online','status=offline','status=reject']

        if 'status=online' in sourceURL:
            flag = 1
        elif 'status=offline' in sourceURL:
            flag = 2
        elif 'status=reject' in sourceURL:
            flag = 3
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

        nodes.append(loader.render_to_string('wish_search_bar.html',
                                             {'url':oldUrl, 'flag':flag,}))