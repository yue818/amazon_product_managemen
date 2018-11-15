#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_wish_pb_productdailystats_Plugin.py
 @time: 2018-05-25 14:39
"""
from xadmin.views import BaseAdminPlugin
from django.template import loader
from django.contrib import messages
from skuapp.table.t_wish_pb_productdailystats import t_wish_pb_productdailystats
import json

class t_wish_pb_productdailystats_Plugin(BaseAdminPlugin):
    performance_plugin_p = False

    def init_request(self, *args, **kwargs):
        return bool(self.performance_plugin_p)

    def block_search_cata_nav(self, context, nodes):

        request = self.request
        #v_campaign_id = request.GET.get('campaign_id', '')
        v_product_id = request.GET.get('product_id', '')
        v_startdate = request.GET.get('startdate', '')
        v_enddate = request.GET.get('enddate', '')
        #back_ref = request.GET.get('back_ref', '')

        s1 = {}
        if v_product_id != '':
            s1['product_id__exact'] = v_product_id
        if v_startdate != '':
            s1['p_date__gte'] = v_startdate
        if v_enddate != '':
            s1['p_date__lt'] = v_enddate
        objs = t_wish_pb_productdailystats.objects.filter(**s1).order_by('p_date')

        datelist = []
        impressions = []
        paid_impressions = []
        sales = []
        gmv = []
        title = ''

        if objs.exists():
            for info in objs:
                tt = info.p_date.strftime('%Y-%m-%d')
                datelist.append(tt)
                imp, paid = info.impressions, info.paid_impressions
                impressions.append(int(imp.replace(',', '') if isinstance(imp, str) else imp))
                paid_impressions.append(int(paid.replace(',', '') if isinstance(paid, str) else paid))
                sales.append(int(info.sales))
                gmv.append(float(info.gmv))

            title = u'活动在%s到%s期间的每日表现' % (min(datelist), max(datelist),)
        else:
            messages.error(request, u'无相关数据, 活动已取消或还没有开始.')
        
        sourceURL = '/Project/admin/skuapp/t_wish_pb_campaignproductstats/'
        '''if back_ref != '':
            back_ref = back_ref.replace('%20', '/')
            back_ref = base64.b64decode(back_ref)
            if back_ref != '/':
                sourceURL += back_ref'''
        sourceURL = request.session.get('back_ref', sourceURL)

        context = {
            'title': title,
            'datelist': json.dumps(datelist),
            'impressions': impressions,
            'paid_impressions': paid_impressions,
            'sales': sales,
            'gmv': gmv,
            'sourceURL': sourceURL   # 用于返回
        }

        nodes.append(loader.render_to_string('productboost_performance_p.html', context))