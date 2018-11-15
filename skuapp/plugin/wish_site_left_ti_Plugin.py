# encoding: utf-8
'''
@author: zhangyu
@contact: 292724306@qq.com
@software: pycharm
@file: wish_site_left_ti_Plugin.py
@time: 2018-06-11 17:43
'''
import json
from django_redis import get_redis_connection
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.template import RequestContext
from skuapp.table.wish_ticket import wish_ticket
import logging
import re

logger = logging.getLogger('sourceDns.webdns.views')


class wish_site_left_ti_Plugin(BaseAdminPlugin):
    wish_site_tree_ti = False

    def init_request(self, *args, **kwargs):
        return bool(self.wish_site_tree_ti)

    def block_left_navbar(self, context, nodes):
        url = self.request.get_full_path()

        userName = self.request.user.username
        
        r = get_redis_connection(alias='product')
        errorShopName1 = r.get('{}_errorShopName_ti1'.format(userName))[:-1] if r.get(
            '{}_errorShopName_ti1'.format(userName)) else ''
        errorShopName2 = r.get('{}_errorShopName_ti2'.format(userName))[:-1] if r.get(
            '{}_errorShopName_ti2'.format(userName)) else ''
        errorShopName3 = r.get('{}_errorShopName_ti3'.format(userName))[:-1] if r.get(
            '{}_errorShopName_ti3'.format(userName)) else ''
        errorShopName = '{},{},{}'.format(errorShopName1, errorShopName2, errorShopName3).replace('[', '').replace(']',
                                                                                                                   '').replace(
            'u', '').replace("'", "").split(',')
        for i in range(len(errorShopName)):
            errorShopName[i] = 'Wish-' + errorShopName[i]
        count_errorShopName = wish_ticket.objects.filter(shopName__in=errorShopName).count()
        count_success = wish_ticket.objects.exclude(shopName__in=errorShopName).count()
        count = wish_ticket.objects.all().count()
        nowurl = url.replace('code=0', '').replace('code=1', '').replace('?&','?').replace('&&', '&')
        if nowurl[-1:] in ['?', '&']:
            nowurl = nowurl[:-1]
        if nowurl.find('?') == -1:
            nowurl = nowurl + '?'
        else:
            nowurl = nowurl + '&'
        menu_list = [
            {
                "name": u"全部Ticket({})".format(count),
                "code": "01",
                "icon": "icon-th",
                "selected": "",
                "to_url": nowurl.split('?')[0],
                "flag": "all",
                "child": [
                    {
                        "name": u"正常Ticket({})".format(count_success),
                        "code": "11",
                        "icon": "icon-minus-sign",
                        "parentCode": "01",
                        "selected": "",
                        "to_url": nowurl.split('?')[0] + '?errorShop=no',
                        "flag": "success",
                        "child": []
                    },
                    {
                        "name": u"异常Ticket({})".format(count_errorShopName),
                        "code": "12",
                        "icon": "icon-minus-sign",
                        "parentCode": "01",
                        "selected": "",
                        "to_url": nowurl.split('?')[0] + '?errorShop=yes',
                        "flag": "errorShop",
                        "child": []
                    }
                ]
            }
        ]

        flag = 'all'
        flag2 = self.request.GET.get('errorShop')
        if flag2 and flag2 == 'yes':
            flag = 'errorShop'
        if flag2 and flag2 == 'no':
            flag = 'success'
        show_flag = 0
        for menu_obj in menu_list:
            if menu_obj['flag'] == flag:
                menu_obj['selected'] = 'selected'
                show_flag = 1
            for menu_o in menu_obj['child']:
                if menu_o['flag'] == flag:
                    menu_o['selected'] = 'selected'
                    show_flag = 1
                for menu_ in menu_o['child']:
                    if menu_['flag'] == flag:
                        menu_['selected'] = 'selected'
                        show_flag = 1

        if show_flag == 1:
            nodes.append(
                loader.render_to_string('wish_site_menu.html',
                                        {'menu_list': json.dumps(menu_list), 'errorShopName1': errorShopName1,
                                         'errorShopName2': errorShopName2, 'errorShopName3': errorShopName3},
                                        context_instance=RequestContext(self.request)))
