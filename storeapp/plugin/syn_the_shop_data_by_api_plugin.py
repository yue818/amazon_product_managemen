#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: syn_the_shop_data_by_api_plugin.py
 @time: 2018/1/16 16:18
"""
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.template import RequestContext
import logging
import json
from brick.table.get_wish_product_order_updatetime import get_wish_product_order_updatetime
from django.db import connection
from skuapp.table.t_store_configuration_file import t_store_configuration_file

from django.contrib import messages
from django.db.models import Q
from django_redis import get_redis_connection
from brick.classredis.classshopname import classshopname

logger = logging.getLogger('sourceDns.webdns.views')

class syn_the_shop_data_by_api_plugin(BaseAdminPlugin):
    syn_data = False

    def init_request(self, *args, **kwargs):
        return bool(self.syn_data)

    def block_search_cata_nav(self, context, nodes):
        redis_coon = get_redis_connection(alias='product')

        if self.request.GET.get('shopname', '') != '':
            flag = self.request.GET.get('shopname', '')
        else:
            flag = ''
        if flag.find('Wish-') == -1:
            flag = 'Wish-' + flag.zfill(4)
        lastupdatetime = ''
        if flag != 'Wish-':
            get_wish_product_order_updatetime_obj = get_wish_product_order_updatetime(connection,flag)
            up_obj = get_wish_product_order_updatetime_obj.get_updatetime('Product')
            if up_obj:
                lastupdatetime = up_obj[1] # 上次增量更新的时间

        classshopname_obj = classshopname(redis_cnxn=redis_coon)
        refreshstatus = classshopname_obj.get_api_status_by_shopname(flag)
        if refreshstatus is None:
            refreshstatus = ''

        syndict = {}
        syndict[flag] = '/syndata_by_wish_api_shopname/?shopname=%s' % flag

        buttonlist = []
        if self.request.user.is_superuser:
            objs = t_store_configuration_file.objects.filter(ShopName__startswith='Wish-').values('ShopName_temp')
        else:
            objs = t_store_configuration_file.objects.filter(Q(Seller=context['user'].first_name)|Q(Published=context['user'].first_name)|Q(Operators=context['user'].first_name)).values('ShopName_temp')
        for obj in objs:
            buttonlist.append(obj['ShopName_temp'])
        buttonlist.sort()
        nodes.append(loader.render_to_string('syn_the_shop_data_by_api_plugin.html',{'objs': json.dumps(buttonlist), 'syndict': syndict, 'flag': flag,'lastupdatetime':lastupdatetime,'refreshstatus':refreshstatus},context_instance=RequestContext(self.request)))
