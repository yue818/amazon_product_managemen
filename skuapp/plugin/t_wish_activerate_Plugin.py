#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: changyang  
 @site: 
 @software: PyCharm
 @file: t_wish_activerate_Plugin.py
 @time: 2018-08-20 15:46
"""

from xadmin.views import BaseAdminPlugin
from django.template import loader
from skuapp.table.t_wish_activerate import t_wish_activerate
import json


class t_wish_activerate_Plugin(BaseAdminPlugin):
    wish_activerate_chart = False

    def init_request(self, *args, **kwargs):
        return bool(self.wish_activerate_chart)

    def get_media(self, media):
        media.add_js([self.static('xadmin/js/xadmin.plugin.button.color.js')])
        return media

    def block_search_cata_nav(self, context, nodes):
        request = self.request

        searchList = {}

        PeriodType = request.GET.get('PeriodType', '1')
        searchList['PeriodType__exact'] = PeriodType

        PeriodStart = request.GET.get('PeriodStart', '')
        if PeriodStart != '':
            searchList['PeriodStart__gte'] = PeriodStart

        PeriodEnd = request.GET.get('PeriodEnd', '')
        if PeriodEnd != '':
            searchList['PeriodEnd__lt'] = PeriodEnd

        try:
            if PeriodType == '1':
                qs = t_wish_activerate.objects.filter(**searchList).order_by('-PeriodNO')[:54]
                title = u'每周激活率'
                flag = 1
            else:
                qs = t_wish_activerate.objects.filter(**searchList).order_by('-PeriodNO')[:60]
                title = u'每月激活率'
                flag = 2
        except Exception:
            return

        date_data = []
        UploadCnt = []
        OrderCnt = []
        ActiveRate = []
        for info in qs:
            date_data.append(info.PeriodNO)
            UploadCnt.append(int(info.UploadCnt))
            OrderCnt.append(int(info.OrderCnt))
            ActiveRate.append(float(info.ActiveRate))

        date_data.reverse()
        UploadCnt.reverse()
        OrderCnt.reverse()
        ActiveRate.reverse()

        context = {
            'title': title,
            'flag': flag,
            'date_data': json.dumps(date_data),
            'UploadCnt': UploadCnt,
            'OrderCnt': OrderCnt,
            'ActiveRate': ActiveRate
        }

        nodes.append(loader.render_to_string('t_wish_activerate_chart.html', context))