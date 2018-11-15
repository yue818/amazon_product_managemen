#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_wish_pb_left_menu_Plugin.py
 @time: 2018-05-30 13:18
"""

from xadmin.views import BaseAdminPlugin
from django.template import loader
from skuapp.table.t_wish_pb_campaignproductstats import t_wish_pb_campaignproductstats as PB

class t_wish_pb_left_menu_Plugin(BaseAdminPlugin):
    t_wish_pb_left_menu = False

    def init_request(self, *args, **kwargs):
        return bool(self.t_wish_pb_left_menu)

    def block_left_navbar(self, context, nodes):

        selection_cnt = PB.objects.filter(dataflag=1).values('id').count()
        continue_cnt = PB.objects.filter(dataflag=2).values('id').count()
        stop_cnt = PB.objects.filter(dataflag=3).values('id').count()
        soldout_cnt = PB.objects.filter(dataflag=4).values('id').count()
        all_cnt = selection_cnt + continue_cnt + stop_cnt + soldout_cnt

        sourceURL = str(context['request']).split("'")[1]
        title_list = [{'title': u'Wish广告', 'selected': '0'}]

        test_list = [
            {'url': '/Project/admin/skuapp/t_wish_pb_campaignproductstats/', 'value': u'全局查询(' + str(all_cnt) + ')',
             'title': u'Wish广告', 'selected': '0'},
            {'url': '/Project/admin/skuapp/t_wish_pb_campaignproductstats/?dataflag=1', 'value': u'选品广告(' + str(selection_cnt) + ')',
             'title': u'Wish广告', 'selected': '0'},
            {'url': '/Project/admin/skuapp/t_wish_pb_campaignproductstats/?dataflag=2', 'value': u'连续广告(' + str(continue_cnt) + ')',
             'title': u'Wish广告', 'selected': '0'},
            {'url': '/Project/admin/skuapp/t_wish_pb_campaignproductstats/?dataflag=3', 'value': u'停止广告(' + str(stop_cnt) + ')',
             'title': u'Wish广告', 'selected': '0'},
            {'url': '/Project/admin/skuapp/t_wish_pb_campaignproductstats/?dataflag=4', 'value': u'下架列表(' + str(soldout_cnt) + ')',
             'title': u'Wish广告', 'selected': '0'},
            {'url': '/Project/admin/skuapp/t_wish_pb_report/?datatype=week', 'value': u'统计报表', 'title': u'Wish广告', 'selected': '0'},
            {'url': '/Project/admin/skuapp/t_wish_pb_finance_rep/', 'value': u'花费报表', 'title': u'Wish广告', 'selected': '0'},
            {'url': '/Project/admin/skuapp/t_wish_pb_earnings_show/', 'value': u'收益报表', 'title': u'Wish广告', 'selected': '0'},
        ]

        title = ''
        flag = 1

        if 'dataflag=1' in sourceURL:
            test_list[1]['selected'] = '1'
            title = test_list[1]['title']
        elif 'dataflag=2' in sourceURL:
            test_list[2]['selected'] = '1'
            title = test_list[2]['title']
        elif 'dataflag=3' in sourceURL:
            test_list[3]['selected'] = '1'
            title = test_list[3]['title']
        elif 'dataflag=4' in sourceURL:
            test_list[4]['selected'] = '1'
            title = test_list[4]['title']
        elif 't_wish_pb_report' in sourceURL:
            test_list[5]['selected'] = '1'
            title = test_list[5]['title']
        elif 't_wish_pb_finance_rep' in sourceURL:
            test_list[6]['selected'] = '1'
            title = test_list[6]['title']
        elif 't_wish_pb_earnings_show' in sourceURL:
            test_list[7]['selected'] = '1'
            title = test_list[7]['title']
        else:
            test_list[0]['selected'] = '1'
            title = test_list[0]['title']

        if title:
            for titleout in title_list:
                if titleout['title'] == title:
                    titleout['selected'] = '1'

        if flag == 1:
            nodes.append(loader.render_to_string('site_left_menu_wishpbPlugin.html',
                                                 {'title_list': title_list, 'test_list': test_list,
                                                  'sourceURL': sourceURL}))