# encoding: utf-8
'''
@author: zhangyu
@contact: 292724306@qq.com
@software: pycharm
@file: wish_notification_Admin.py
@time: 2018-06-09 13:37
'''
import requests
import logging
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
from brick.table.t_config_online_amazon import t_config_online_amazon
from django.db import connection
from skuapp.public.wish_notification_syn import wish_notification_syn, connection_lll
from brick.wish.wish_api_before.token_verification import verb_token
logger = logging.getLogger('sourceDns.webdns.views')

t_config_online_amazon_obj = t_config_online_amazon(connection_lll)


class wish_notification_Admin(object):
    wish_notification = True
    wish_site_tree_noti = True
    list_display_links = ("",)
    list_display = ['show_shopName', 'title', 'message', 'show_Operators',
                    'updateTime']
    actions = ['be_Viewed']

    def be_Viewed(self, request, queryset):
        for obj in queryset:
            try:
                auth_info = verb_token(obj.shopName, connection)
                assert auth_info['errorcode'] == 1, auth_info['errortext']

                url = "https://merchant.wish.com/api/v2/noti/mark-as-viewed"
                params = {
                    "access_token": auth_info['access_token'],
                    "format": "json",
                    "noti_id": obj.noti_id,
                }

                r = requests.post(url, params=params, timeout=5)
                wish_notification_syn_obj = wish_notification_syn()
                code = wish_notification_syn_obj.insertDB(obj.shopName)
            except Exception, e:
                logger.error(u'已看过----------------------%s' % e)
                pass

        zhangyu = u'%s' % request
        newUrl = zhangyu.split('/')[-1].replace("'", "").replace(">", "").replace('&code=0', '').replace('&code=1', '')
        if newUrl == '':
            newUrl = '?p=0'
        return HttpResponseRedirect(newUrl)

    be_Viewed.short_description = u'已看过'

    def show_shopName(self, obj):
        rt = "<p>{}</p>".format(obj.shopName)
        return mark_safe(rt)

    show_shopName.short_description = mark_safe(
        "<p align='center' style='color:#428BCA'>&nbsp;&nbsp;&nbsp;店铺名称&nbsp;&nbsp;&nbsp;</p>")

    def show_Operators(self, obj):
        rt = "<p>{}</p>".format(obj.Operators)
        return mark_safe(rt)

    show_Operators.short_description = mark_safe(
        "<p align='center' style='color:#428BCA'>&nbsp;&nbsp;运营&nbsp;&nbsp;</p>")

    def save_models(self):
        pass

    def get_list_queryset(self, ):

        # logger = logging.getLogger('sourceDns.webdns.views')
        request = self.request
        Operators = ''
        # 超级用户和金玉玲可以看到所有运营店铺
        if self.request.user.is_superuser or self.request.user.username == 'jinyuling' or self.request.user.username == 'meidandan':
            Operators = ''
        else:
            Operators = self.request.user.first_name
        qs = super(wish_notification_Admin, self).get_list_queryset()
        shopname = request.GET.get('shopname', '')
        status = request.GET.get('status', '')
        errorShop = request.GET.get('errorShop', '')
        list_errorShop = []
        list_errorShop_tmp = ''
        if errorShop == 'yes' or errorShop == 'no':
            from django_redis import get_redis_connection
            r = get_redis_connection(alias='product')
            errorShopName1 = r.get('{}_errorShopName_noti1'.format(request.user.username))
            errorShopName2 = r.get('{}_errorShopName_noti2'.format(request.user.username))
            errorShopName3 = r.get('{}_errorShopName_noti3'.format(request.user.username))
            errorShopName = "{}{}{}".format(errorShopName1, errorShopName2, errorShopName3)
            list_errorShop_tmp = errorShopName.replace('[', '').replace(']', '').replace('u', '').replace("'",
                                                                                                          "") if errorShopName else ''
            list_errorShop = list_errorShop_tmp.split(',')
            for i in range(len(list_errorShop)):
                list_errorShop[i] = 'Wish-' + list_errorShop[i]
        days = []
        if status == '1':
            days = [1, 2, 3]
        elif status == '2':
            days = [4]
        elif status == '3':
            days = [5]
        searchList = {'shopName': shopname, 'days_to_fulfill__in': days,
                      'Operators': Operators}
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if sl is not None:
            try:
                if errorShop == 'yes':
                    qs = qs.filter(**sl).filter(shopName__in=list_errorShop)
                elif errorShop == 'no':
                    qs = qs.filter(**sl).exclude(shopName__in=list_errorShop)
                else:
                    qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')
        return qs
