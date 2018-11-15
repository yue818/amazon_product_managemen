# encoding: utf-8
'''
@author: zhangyu
@contact: 292724306@qq.com
@software: pycharm
@file: wish_site_left_Plugin.py
@time: 2018-06-08 10:12
'''
import json
from django_redis import get_redis_connection
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.template import RequestContext
from skuapp.table.wish_processed_order import wish_processed_order
import logging
import re

logger = logging.getLogger('sourceDns.webdns.views')


class wish_site_left_Plugin(BaseAdminPlugin):
    wish_site_tree = False

    def init_request(self, *args, **kwargs):
        return bool(self.wish_site_tree)

    def block_left_navbar(self, context, nodes):
        objs = wish_processed_order.objects
        url = self.request.get_full_path()
        shopName = ''
        shopName_index = re.search(r'Wish-\d{4}', url)
        if shopName_index:
            shopName = url[shopName_index.span()[0]:shopName_index.span()[1]]
        if shopName:
            objs = wish_processed_order.objects.filter(shopName__exact=shopName)
        objs1 = objs.filter(days_to_fulfill__in=[1, 2, 3]).count()
        objs2 = objs.filter(days_to_fulfill=4).count()
        objs3 = objs.filter(days_to_fulfill=5).count()
        count = wish_processed_order.objects.all().count()
        userName = self.request.user.username
        r = get_redis_connection(alias='product')
        errorShopName1 = r.get('{}_errorShopName_1'.format(userName))[:-1] if r.get(
            '{}_errorShopName_1'.format(userName)) else ''
        errorShopName2 = r.get('{}_errorShopName_2'.format(userName))[:-1] if r.get(
            '{}_errorShopName_2'.format(userName)) else ''
        errorShopName3 = r.get('{}_errorShopName_3'.format(userName))[:-1] if r.get(
            '{}_errorShopName_3'.format(userName)) else ''
        errorShopName = '{},{},{}'.format(errorShopName1, errorShopName2, errorShopName3).replace('[', '').replace(']',
                                                                                                                   '').replace(
            'u', '').replace("'", "").split(',')
        for i in range(len(errorShopName)):
            errorShopName[i] = 'Wish-' + errorShopName[i]
        count_errorShopName = wish_processed_order.objects.filter(shopName__in=errorShopName).count()
        count_success = count - count_errorShopName
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
                        "name": u"正常店铺({})".format(count_success),
                        "code": "11",
                        "icon": "icon-minus-sign",
                        "parentCode": "01",
                        "selected": "",
                        "to_url": "",
                        "flag": "",
                        "child": [
                            {
                                "name": u"1-3天({})".format(objs1),
                                "icon": "",
                                "code": "111",
                                "parentCode": "11",
                                "selected": "",
                                "to_url": nowurl + 'status=1',
                                "flag": '1',
                                "child": []
                            },
                            {
                                "name": u"4天({})".format(objs2),
                                "icon": "",
                                "code": "112",
                                "parentCode": "11",
                                "selected": "",
                                "to_url": nowurl + 'status=2',
                                "flag": '2',
                                "child": []
                            },
                            {
                                "name": u"5天({})".format(objs3),
                                "icon": "",
                                "code": "113",
                                "parentCode": "11",
                                "selected": "",
                                "to_url": nowurl + 'status=3',
                                "flag": '3',
                                "child": []
                            },
                        ]
                    },
                    {
                        "name": u"异常店铺({})".format(count_errorShopName),
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
        flag1 = self.request.GET.get('status')
        if flag1:
            flag = flag1

        flag2 = self.request.GET.get('errorShop')
        if flag2 and flag2 == 'yes':
            flag = 'errorShop'

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
