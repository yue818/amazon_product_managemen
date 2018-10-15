# -*- coding: utf-8 -*-
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.template import RequestContext
import logging
import json
from urllib import urlencode
from django.contrib import messages

class wish_store_sort_bar_plugin(BaseAdminPlugin):
    sort_bar = False

    def init_request(self, *args, **kwargs):
        return bool(self.sort_bar)

    def block_search_loaction_after(self, context, nodes):
        ordering = ''

        params = dict(self.request.GET.items())
        if 'o' in params:
            ordering = params['o']
            del params['o']
        # raise Exception(params)  {u'status': u'all', u'EXPRESS': u'STANDARD'}
        list_dict = {}
        if self.model._meta.model_name == 't_online_info_wish_store':
            list_dict = {
                'DateUploaded': u'上架日期', 'LastUpdated': u'最近更新日期',
                'Rating': u'评分', 'RefreshTime': u'Online 刷新时间'
            }
            activeflag = params.get('EXPRESS', 'STANDARD')
            if activeflag == 'DE':
                list_dict['Order7daysDE'] = u'7天order数(德国仓)'
                list_dict['OfsalesDE'] = u'总订单量(德国仓)'
            elif activeflag == 'GB':
                list_dict['Order7daysGB'] = u'7天order数(英国仓)'
                list_dict['OfsalesGB'] = u'总订单量(英国仓)'
            elif activeflag == 'US':
                list_dict['Order7daysUS'] = u'7天order数(美国仓)'
                list_dict['OfsalesUS'] = u'总订单量(美国仓)'
            elif activeflag == 'FBW':
                list_dict['Order7daysFBW'] = u'7天order数(FBW)'
                list_dict['OfsalesFBW'] = u'总订单量(FBW)'
            else:
                list_dict['Orders7Days'] = u'7天order数'
                list_dict['OfSales'] = u'总销量'
        elif self.model._meta.model_name == 't_online_info_ebay_listing':
            list_dict = {
                'hitCount': u'按浏览量', 'watchCount': u'按收藏量', 'Orders7Days': u'按7天销量', 'sold': u'按总销量',
                'starttime': u'按上架日期', 'endtime': u'按下架日期', 'lastRefreshTime': u'按在线刷新时间'
            }

        paramDict = {}
        for k, v in list_dict.items():
            flag = ('<i class="fa fa-sort-down"></i>' if ordering.startswith('-')  else '<i class="fa fa-sort-up"></i>') \
                if ordering and ordering.replace('-', '') == k  else ''

            paramDict[k] = {
                'descri': v,
                'up': '?%s' % urlencode(params) + '&o=' + k if params else '?o=' + k,
                'down': '?%s' % urlencode(params) + '&o=-' + k if params else '?o=-' + k,
                'times': '?%s' % urlencode(params) + '&o=' if params else '?o=',
                'flag': flag
            }

        # raise Exception(self.request.menus_item.menus.__dict__)

        nodes.append(
            loader.render_to_string('wish_store_sort_bar.html',
                {'paramDict': paramDict},
                context_instance=RequestContext(self.request)
            )
        )
