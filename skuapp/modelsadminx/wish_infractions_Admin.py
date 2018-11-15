# encoding: utf-8
'''
@author: zhangyu
@contact: 292724306@qq.com
@software: pycharm
@file: wish_infractions_Admin.py
@time: 2018-06-13 14:56
'''
import logging
from django.contrib import messages
from django.utils.safestring import mark_safe

logger = logging.getLogger('sourceDns.webdns.views')


class wish_infractions_Admin(object):
    wish_site_tree_in = True
    wish_in = True
    list_display_links = ("",)
    list_display = ['shopName', 'infractions_count', 'Operators', 'updateTime']

    def save_models(self):
        pass

    def get_list_queryset(self, ):
        request = self.request
        Operators = ''
        errorShop = request.GET.get('errorShop', '')
        # 超级用户和金玉玲可以看到所有运营店铺
        if self.request.user.is_superuser or self.request.user.username == 'jinyuling' or self.request.user.username == 'meidandan':
            Operators = ''
        else:
            Operators = self.request.user.first_name
        qs = super(wish_infractions_Admin, self).get_list_queryset()
        shopname = request.GET.get('shopname', '')
        infr = request.GET.get('in', '')
        list_errorShop = []
        list_errorShop_tmp = ''
        if errorShop == 'yes' or errorShop == 'no':
            from django_redis import get_redis_connection
            r = get_redis_connection(alias='product')
            errorShopName1 = r.get('{}_errorShopName_in1'.format(request.user.username))
            errorShopName2 = r.get('{}_errorShopName_in2'.format(request.user.username))
            errorShopName3 = r.get('{}_errorShopName_in3'.format(request.user.username))
            errorShopName = "{}{}{}".format(errorShopName1, errorShopName2, errorShopName3)
            list_errorShop_tmp = errorShopName.replace('[', '').replace(']', '').replace('u', '').replace("'",
                                                                                                          "") if errorShopName else ''
            list_errorShop = list_errorShop_tmp.split(',')
            for i in range(len(list_errorShop)):
                list_errorShop[i] = 'Wish-' + list_errorShop[i]
        searchList = {'shopName': shopname, 'Operators': Operators}
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
                else:
                    qs = qs.filter(**sl)
                if infr == '1':
                    qs = qs.exclude(infractions_count__exact=0)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')
        return qs
