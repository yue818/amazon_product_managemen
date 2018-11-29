# -*- coding: utf-8 -*-

from xadmin.views import BaseAdminPlugin
from django.template import loader
# from django.db import connection
from skuapp.table.t_sys_param import t_sys_param
from brick.table.t_config_online_amazon import t_config_online_amazon
# from brick.table.t_config_amazon_shop_status import t_config_amazon_shop_status
from brick.table.t_large_small_corresponding_cate import t_large_small_corresponding_cate
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import logging
import json
from brick.table.get_wish_product_order_updatetime import get_wish_product_order_updatetime
from django.db import connection

from django.contrib import messages
from django.db.models import Q
from django_redis import get_redis_connection
from brick.classredis.classshopname import classshopname
# from Project.settings import connRedis
from skuapp.table.t_store_configuration_file import t_store_configuration_file
from datetime import datetime as timetime, timedelta
from skuapp.public.check_permission_legality import check_permission_legality
from brick.table.t_country_code_name_table import t_country_code_name_table


class t_online_info_wish_store_secondplugin(BaseAdminPlugin):
    wish_listing_secondplugin = False

    def init_request(self, *args, **kwargs):
        return bool(self.wish_listing_secondplugin)

    def wish_right_button(self):
        return True if check_permission_legality(self) else False

    def block_search_cata_nav(self, context, nodes):
        # messages.error(self.request,'search1-------%s' % timetime.now())
        redis_coon = get_redis_connection(alias='product')

        if self.request.GET.get('shopname', '') != '':
            flag = self.request.GET.get('shopname', '')
        else:
            flag = ''
        if flag.find('Wish-') == -1:
            flag = 'Wish-' + flag.zfill(4)
        lastupdatetime = ''
        if flag != 'Wish-':
            get_wish_product_order_updatetime_obj = get_wish_product_order_updatetime(connection, flag)
            up_obj = get_wish_product_order_updatetime_obj.get_updatetime('Product')
            if up_obj:
                lastupdatetime = up_obj[1]  # 上次增量更新的时间

        classshopname_obj = classshopname(redis_cnxn=redis_coon)
        refreshstatus = classshopname_obj.get_api_status_by_shopname(flag)
        lastrefreshtime = classshopname_obj.get_api_time_by_shopname(flag)

        if lastrefreshtime and (timetime.now() + timedelta(hours=-2)).strftime('%Y-%m-%d %H:%M:%S') > lastrefreshtime:
            classshopname_obj.del_api_time_by_shopname(flag)
            classshopname_obj.del_api_status_by_shopname(flag)
            refreshstatus = ''
        elif not lastrefreshtime:
            classshopname_obj.del_api_status_by_shopname(flag)

        refreshstatus = refreshstatus if refreshstatus else ''
        synurl = ''
        if flag != 'Wish-0000' and refreshstatus == '':
            synurl = '/syndata_by_wish_api_shopname/?shopname=%s' % flag

        buttonlist = []
        if self.request.user.is_superuser or self.model._meta.model_name == 't_online_info_wish':
            objs = t_store_configuration_file.objects.filter(ShopName__startswith='Wish-').values('ShopName_temp')
        else:
            allobj = User.objects.filter(groups__id__in=[38])
            userID = []
            for each in allobj:
                userID.append(each.id)
            if (self.request.user.id in userID):
                objs = t_store_configuration_file.objects.filter(ShopName__startswith='Wish-').values('ShopName_temp')
            else:
                objs = t_store_configuration_file.objects.filter(
                    Q(Seller=context['user'].first_name) | Q(Published=context['user'].first_name) | Q(
                        Operators=context['user'].first_name)).values('ShopName_temp')
        for obj in objs:
            buttonlist.append(obj['ShopName_temp'])
        buttonlist.sort()

        activeflag = self.request.GET.get('EXPRESS','')

        nowurl = self.request.get_full_path().replace('EXPRESS=STANDARD', '').replace('EXPRESS=DE', '').replace(
            'EXPRESS=GB', '').replace('EXPRESS=US', '').replace('EXPRESS=FBW', '').replace('?&', '?').replace('&&', '&')
        if nowurl[-1:] in ['?', '&']:
            nowurl = nowurl[:-1]
        if nowurl.find('?') == -1:
            nowurl = nowurl + '?'
        else:
            nowurl = nowurl + '&'

        readonly = ''
        if self.model._meta.model_name == 't_online_info_wish' or not self.wish_right_button():
            readonly = 'readonly'

        countrys_code = t_country_code_name_table(connection).GetAllCountryCode()
        countrys_code_dict = countrys_code.get('data',{})
        # messages.error(self.request, 'search2-------%s' % timetime.now())
        nodes.append(loader.render_to_string(
            'products_listing_base_secondtemplate.html',
             {'objs': json.dumps(buttonlist), 'synurl': synurl, 'flag': flag,'lastupdatetime':lastupdatetime,
              'refreshstatus':refreshstatus,'nowurl': nowurl, 'activeflag': activeflag, 'readonly':readonly,
              'countrys_code_dict': sorted(countrys_code_dict.items(), key=lambda x: x[0])}
        ))
