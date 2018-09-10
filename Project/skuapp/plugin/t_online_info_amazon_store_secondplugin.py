# -*- coding: utf-8 -*-

# from django.db import connection
# from skuapp.table.t_sys_param import t_sys_param
# from brick.table.t_config_online_amazon import t_config_online_amazon
# from brick.table.t_config_amazon_shop_status import t_config_amazon_shop_status
# from brick.table.t_large_small_corresponding_cate import t_large_small_corresponding_cate
# from xadmin.views import BaseAdminPlugin
# from django.template import loader
# from django.template import RequestContext
# from django.contrib.auth.models import Group
# import logging
# from brick.table.get_wish_product_order_updatetime import get_wish_product_order_updatetime
# from django.db import connection
# from datetime import datetime as timetime
# from django.contrib import messages
# from django_redis import get_redis_connection
# from brick.classredis.classshopname import classshopname
# from Project.settings import connRedis

import json
from django.db.models import Q
from django.template import loader
from django.contrib.auth.models import User
from xadmin.views import BaseAdminPlugin
from skuapp.table.t_store_configuration_file import t_store_configuration_file


class t_online_info_amazon_store_secondplugin(BaseAdminPlugin):
    amazon_listing_secondplugin = False

    def init_request(self, *args, **kwargs):
        return bool(self.amazon_listing_secondplugin)

    def block_search_cata_nav(self, context, nodes):
        # messages.error(self.request,'search1-------%s' % timetime.now())
        # redis_coon = get_redis_connection(alias='product')

        if self.request.GET.get('shopname', '') != '':
            flag = self.request.GET.get('shopname', '')
        else:
            flag = ''
        if flag.find('AMZ-') == -1:
            flag = 'AMZ-' + flag.zfill(4)
        # lastupdatetime = ''
        # if flag != 'AMZ-':
        #     get_wish_product_order_updatetime_obj = get_wish_product_order_updatetime(connection, flag)
        #     up_obj = get_wish_product_order_updatetime_obj.get_updatetime('Product')
        #     if up_obj:
        #         lastupdatetime = up_obj[1]  # 上次增量更新的时间

        # classshopname_obj = classshopname(redis_cnxn=redis_coon)
        # refreshstatus = classshopname_obj.get_api_status_by_shopname(flag)
        # if refreshstatus is None:
        #     refreshstatus = ''

        # synurl = ''
        # if flag != 'Wish-0000' and refreshstatus == '':
        #     synurl = '/syndata_by_wish_api_shopname/?shopname=%s' % flag

        buttonlist = []
        if self.request.user.is_superuser:
            objs = t_store_configuration_file.objects.filter(ShopName__startswith='AMZ-').values('ShopName')
        else:
            allobj = User.objects.filter(groups__id__in=[38])
            userID = []
            for each in allobj:
                userID.append(each.id)
            if (self.request.user.id in userID):
                objs = t_store_configuration_file.objects.filter(ShopName__startswith='AMZ-').values('ShopName')
            else:
                objs = t_store_configuration_file.objects.filter(
                    Q(Seller=context['user'].first_name) | Q(Published=context['user'].first_name) | Q(
                        Operators=context['user'].first_name)).values('ShopName_temp')
        for obj in objs:
            buttonlist.append(obj['ShopName'])
        buttonlist.sort()

        activeflag = self.request.GET.get('FBFLAG', '')

        nowurl = self.request.get_full_path().replace('FBFLAG=FBA', '').replace('FBFLAG=FBM', '').replace(
            'FBFLAG=ALL', '').replace('?&', '?').replace('&&', '&')
        if nowurl[-1:] in ['?', '&']:
            nowurl = nowurl[:-1]
        if nowurl.find('?') == -1:
            nowurl = nowurl + '?'
        else:
            nowurl = nowurl + '&'
        # messages.error(self.request, 'search2-------%s' % timetime.now())
        nodes.append(
            loader.render_to_string(
                'amazon_products_listing_base_secondtemplate.html',
                {
                    'objs': json.dumps(buttonlist),
                    'flag': flag,
                    'nowurl': nowurl,
                    'activeflag': activeflag
                }
            )
        )
