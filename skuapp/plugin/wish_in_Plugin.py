# encoding: utf-8
'''
@author: zhangyu
@contact: 292724306@qq.com
@software: pycharm
@file: wish_in_Plugin.py
@time: 2018-06-13 15:03
'''
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.template import RequestContext
import logging
import json
from skuapp.table.t_store_configuration_file import t_store_configuration_file

logger = logging.getLogger('sourceDns.webdns.views')


class wish_in_Plugin(BaseAdminPlugin):
    wish_in = False

    def init_request(self, *args, **kwargs):
        return bool(self.wish_in)

    def block_search_cata_nav(self, context, nodes):
        if self.request.GET.get('shopname', '') != '':
            flag = self.request.GET.get('shopname', '')
        else:
            flag = ''
        if flag.find('Wish-') == -1:
            flag = 'Wish-' + flag.zfill(4)

        buttonlist = []
        if self.request.user.is_superuser or self.request.user.username == 'jinyuling' or self.request.user.username == 'meidandan':
            objs = t_store_configuration_file.objects.filter(ShopName__startswith='Wish-').values('ShopName_temp')
        else:
            objs = t_store_configuration_file.objects.filter(Operators=context['user'].first_name).values(
                'ShopName_temp')
        for obj in objs:
            buttonlist.append(obj['ShopName_temp'])
        buttonlist.sort()
        nodes.append(loader.render_to_string('wish_in.html',
                                             {'objs': json.dumps(buttonlist), 'flag': flag},
                                             context_instance=RequestContext(self.request)))