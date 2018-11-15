# coding=utf-8


from xadmin.views import BaseAdminPlugin, ListAdminView
from django.template import loader
# from skuapp.table.t_product_info_wish import *
from django.db.models import Q
from django.contrib import messages
import logging


class price_check_categoryPlugin(BaseAdminPlugin):
    category_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.category_flag)

    def get_media(self, media):
        media.add_js([self.static('xadmin/js/xadmin.plugin.button.color.js')])
        return media

    def block_search_cata_nav(self, context, nodes):
        sourceURL = str(context['request']).split("'")[1]

        paramList = ['&cate=price','&cate=weight','&cate=both',
                     'cate=price&','cate=weight&','cate=both&',
                     'cate=price','cate=weight','cate=both']

        if 'cate=price' in sourceURL:
            flag = 1
        elif 'cate=weight' in sourceURL:
            flag = 2
        elif 'cate=both' in sourceURL:
            flag = 3
        elif 't_product_price_suggest' in sourceURL:
            flag = 4
        else:
            flag = 0

        if '?' in sourceURL:
            for param in paramList:
                if param in sourceURL:
                    sourceURL = sourceURL.replace(param,'')
            if sourceURL.split('?')[1] == '':
                sourceURL = sourceURL
            else:
                sourceURL = sourceURL + '&'
        else:
            sourceURL = sourceURL + '?'

        nodes.append(loader.render_to_string('price_check.html', {'url':sourceURL, 'flag':flag}))