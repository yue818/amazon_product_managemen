# encoding: utf-8
'''
@author: zhangyu
@contact: 292724306@qq.com
@software: pycharm
@file: wish_site_left_noti_Plugin.py
@time: 2018-06-09 14:44
'''
import json
import redis
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.template import RequestContext
from skuapp.table.wish_notification import wish_notification
from skuapp.table.wish_noti import wish_noti
import logging
import re
from django_redis import get_redis_connection
redis_coon = get_redis_connection(alias='product')
logger = logging.getLogger('sourceDns.webdns.views')


class wish_site_left_noti_Plugin(BaseAdminPlugin):
    wish_site_tree_noti = False

    def init_request(self, *args, **kwargs):
        return bool(self.wish_site_tree_noti)

    def block_left_navbar(self, context, nodes):
        url = self.request.get_full_path()
        shopName = ''
        shopName_index = re.search(r'Wish-\d{4}', url)
        if shopName_index:
            shopName = url[shopName_index.span()[0]:shopName_index.span()[1]]
        if shopName:
            objs = wish_notification.objects.filter(shopName__exact=shopName)

        userName = self.request.user.username
        r = redis_coon
        errorShopName1 = r.get('{}_errorShopName_noti1'.format(userName))[:-1] if r.get(
            '{}_errorShopName_noti1'.format(userName)) else ''
        errorShopName2 = r.get('{}_errorShopName_noti2'.format(userName))[:-1] if r.get(
            '{}_errorShopName_noti2'.format(userName)) else ''
        errorShopName3 = r.get('{}_errorShopName_noti3'.format(userName))[:-1] if r.get(
            '{}_errorShopName_noti3'.format(userName)) else ''
        errorShopName = '{},{},{}'.format(errorShopName1, errorShopName2, errorShopName3).replace('[', '').replace(']',
                                                                                                                   '').replace(
            'u', '').replace("'", "").split(',')
        for i in range(len(errorShopName)):
            if errorShopName[i]:
                errorShopName[i] = 'Wish-' + errorShopName[i]
        count_errorShopName = wish_notification.objects.filter(shopName__in=errorShopName).count()
        count_ShopName = wish_notification.objects.exclude(shopName__in=errorShopName).count()
        count = wish_notification.objects.count()
        nowurl = url.replace('status=1', '').replace('status=2', '').replace(
            'status=3', '').replace('errorShop=yes', '').replace('code=0', '').replace('code=1', '').replace('?&',
                                                                                                             '?').replace(
            '&&', '&')
        if nowurl[-1:] in ['?', '&']:
            nowurl = nowurl[:-1]
        if nowurl.find('?') == -1:
            nowurl = nowurl + '?'
        else:
            nowurl = nowurl + '&'
        menu_list = [
            {
                "name": u"全部店铺({})".format(count),
                "code": "01",
                "icon": "icon-th",
                "selected": "",
                "to_url": nowurl.split('?')[0],
                "flag": "all",
                "child": [
                    {
                        "name": u"系统信息({})".format(count_ShopName),
                        "code": "11",
                        "icon": "icon-minus-sign",
                        "parentCode": "01",
                        "selected": "",
                        "to_url": nowurl.split('?')[0] + '?errorShop=no',
                        "flag": "rightShop",
                        "child": [
                        ]
                    },
                    {
                        "name": u"同步异常店铺({})".format(count_errorShopName),
                        "code": "12",
                        "icon": "icon-minus-sign",
                        "parentCode": "01",
                        "selected": "",
                        "to_url": nowurl.split('?')[0] + '?errorShop=yes',
                        "flag": "errorShop",
                        "child": []
                    },
                ]
            }
        ]

        flag = 'all'
        flag2 = self.request.GET.get('errorShop')
        if flag2 and flag2 == 'yes':
            flag = 'errorShop'
        elif flag2 and flag2 == 'no':
            flag = 'rightShop'
        for menu_obj in menu_list:
            if menu_obj['flag'] == flag:
                menu_obj['selected'] = 'selected'
            for menu_o in menu_obj['child']:
                if menu_o['flag'] == flag:
                    menu_o['selected'] = 'selected'
                for menu_ in menu_o['child']:
                    if menu_['flag'] == flag:
                        menu_['selected'] = 'selected'

        nodes.append(
            loader.render_to_string('wish_site_menu.html',
                                    {'menu_list': json.dumps(menu_list), 'errorShopName1': errorShopName1,
                                     'errorShopName2': errorShopName2, 'errorShopName3': errorShopName3},
                                    context_instance=RequestContext(self.request)))
