# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_order_type_plugin.py
 @time: 2018/10/9 14:19
"""
from xadmin.views import BaseAdminPlugin
from django.template import loader


class t_amazon_order_type_plugin(BaseAdminPlugin):
    order_type_plugin = False

    def init_request(self, *args, **kwargs):
        return bool(self.order_type_plugin)

    def block_search_cata_nav(self, context, nodes):
        active_flag = self.request.GET.get('_p_order_type', '')


        now_url = self.request.get_full_path().replace('_p_order_type=FBA', '').replace('_p_order_type=FBM', '').replace('_p_order_type=FOLLOW', '').replace('?&', '?').replace('&&', '&')
        if now_url[-1:] in ['?', '&']:
            now_url = now_url[:-1]
        if now_url.find('?') == -1:
            now_url = now_url + '?'
        else:
            now_url = now_url + '&'

        nodes.append(loader.render_to_string('t_amazon_order_type_plugin.html',  { 'now_url': now_url,  'active_flag': active_flag,}))