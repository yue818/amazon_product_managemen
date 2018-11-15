# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_cpc_ad_left_menu_plugin.py
 @time: 2018-05-17 16:35
"""  

from xadmin.views import BaseAdminPlugin
from django.template import loader
from skuapp.table.t_config_amazon_ad_shop_status import *

class t_amazon_cpc_ad_left_menu_plugin(BaseAdminPlugin):
    t_amazon_cpc_ad_left_menu_flag = False

    def init_request(self, *args, **kwargs):
        return bool(self.t_amazon_cpc_ad_left_menu_flag)

    def block_left_navbar(self, context, nodes):
        refresh_success_cnt = t_config_amazon_ad_shop_status.objects.filter(status='success').values('id').count()
        refresh_ing_cnt = t_config_amazon_ad_shop_status.objects.filter(status='refresh').values('id').count()
        refresh_fail_cnt = t_config_amazon_ad_shop_status.objects.filter(status='fail').values('id').count()

        sourceURL = str(context['request']).split("'")[1]
        title_list = [{'title': u'店铺情况', 'selected': '0'}]
        test_list = [{'url': '/Project/admin/skuapp/t_amazon_cpc_ad/', 'value': u'刷新成功('+str(refresh_success_cnt)+')', 'title': u'店铺情况', 'selected': '0'},
                     {'url': '/Project/admin/skuapp/t_amazon_cpc_ad/', 'value': u'刷新中(' + str(refresh_ing_cnt) + ')', 'title': u'店铺情况', 'selected': '0'},
                     {'url': '/Project/admin/skuapp/t_amazon_cpc_ad/', 'value': u'刷新失败(' + str(refresh_fail_cnt) + ')', 'title': u'店铺情况', 'selected': '0'},]
        title = ''
        flag = 0
        new_sourceURL = sourceURL
        if '?p=' in sourceURL:
            new_sourceURL = sourceURL.replace('?p=', '?')
            if '&' in new_sourceURL:
                new_sourceURL = new_sourceURL.split('?')[0] + '?' + new_sourceURL.split('?')[1].split('&')[1]
            else:
                new_sourceURL = new_sourceURL.split('?')[0]
        for tl in test_list:
            to_url = tl['url']
            if to_url != new_sourceURL:
                if '?' not in tl['url']:
                    to_url = to_url + '?'
            if to_url in new_sourceURL:
                title = tl['title']
                tl['selected'] = '1'
                flag = 1
        if title:
            for titleout in title_list:
                if titleout['title'] == title:
                    titleout['selected'] = '1'
        if flag == 1:
            nodes.append(loader.render_to_string('t_amazon_cpc_ad_left_menu_plugin.html',
                                                 {'title_list': title_list, 'test_list': test_list, 'sourceURL': sourceURL}))
