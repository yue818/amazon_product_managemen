# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: amazon_sort_bar_plugin.py
 @time: 2018/9/8 9:03
"""  
# -*- coding: utf-8 -*-
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.template import RequestContext
from urllib import urlencode
import collections


class amazon_sort_bar_plugin(BaseAdminPlugin):
    amzon_sort_bar = False

    def init_request(self, *args, **kwargs):
        return bool(self.amzon_sort_bar)

    def block_search_loaction_after(self, context, nodes):
        ordering = ''

        params = dict(self.request.GET.items())
        if 'o' in params:
            ordering = params['o']
            del params['o']

        list_dict = collections.OrderedDict()
        if self.model._meta.model_name == 't_online_info_amazon_listing':
            # list_dict = {'orders_7days': u'按7天订单量', 'orders_15days': u'按15天订单量', 'orders_30days': u'按30天订单量', 'orders_total': u'按总订单量', 'orders_refund_total': u'按退款单数', 'refund_rate': u'按退款率' }
            list_dict['orders_7days'] = u'按7天订单量'
            list_dict['orders_15days'] = u'按15天订单量'
            list_dict['orders_30days'] = u'按30天订单量'
            list_dict['orders_total'] = u'按总订单量'
            list_dict['orders_refund_total'] = u'按退款单数'
            list_dict['refund_rate'] = u'按退款率'

        paramDict = collections.OrderedDict()
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

        nodes.append(
            loader.render_to_string('amazon_sort_bar.html',
                {'paramDict': paramDict},
                context_instance=RequestContext(self.request)
            )
        )
