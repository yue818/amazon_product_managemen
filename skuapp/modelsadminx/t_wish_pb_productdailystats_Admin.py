#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_wish_pb_productdailystats_Admin.py
 @time: 2018-05-25 14:20
"""
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.db import connection

class t_wish_pb_productdailystats_Admin(object):
    performance_plugin_p = True
    search_box_flag = True

    def show_spend_gmv(self, obj):
        if obj.spend is None or obj.spend == 0:
            rt = u'<span>0.00%</span>'
        elif obj.gmv is None or obj.gmv == 0:
            rt = u'<span>无相关信息</span>'
        else:
            x = round(obj.spend / obj.gmv * 100, 2)
            rt = u'<span>%.2f%%</span>' % (x,)
        return mark_safe(rt)
    show_spend_gmv.short_description = mark_safe('<p style="color:#428bca;text-align:center">AS</p>')

    def show_expose(self, obj):
        if obj.sales is None or obj.sales == 0:
            rt = u'0.000%'
        elif obj.paid_impressions is None or obj.paid_impressions == 0:
            rt = u'无相关信息'
        else:
            x = round(float(obj.sales) / float(obj.paid_impressions.replace(',', '')) * 100, 3)
            rt = u'%.3f%%' % (x,)
        rt = u'<span>%s</span>' % (rt,)
        return mark_safe(rt)
    show_expose.short_description = mark_safe('<p style="color:#428bca;text-align:center">曝光转化率</p>')

    def show_date(self, obj):
        rt = u'<span>%s</span>'%(obj.p_date.strftime('%Y-%m-%d') + u' 活动期间' if obj.date_flag == 0 else obj.p_date.strftime('%Y-%m-%d'))
        return mark_safe(rt)
    show_date.short_description = mark_safe('<p style="color:#428bca;text-align:center">日期</p>')

    def get_newcampaignid(self, product_id):
        sql = '''select campaign_id from t_wish_pb_productdailystats where product_id='%s' and date_flag =0 order by p_date desc limit 1'''
        cursor = connection.cursor()
        cursor.execute(sql % product_id)
        campaign_id = cursor.fetchone()
        cursor.close()
        return campaign_id[0]

    def show_newcampaignFlag(self, obj):
        campaign_id = self.request.session.get('mycampaign_id', False)
        if campaign_id:
            if obj.campaign_id == campaign_id and obj.date_flag == 0:
                rt = '<div style="background-color:#C0C0C0">1</div>'
            else:
                rt = '<div style="background-color:white">0</div>'
        else:
            campaign_id = self.get_newcampaignid(obj.product_id)
            self.request.session['mycampaign_id'] = campaign_id
            if obj.campaign_id == campaign_id and obj.date_flag == 0:
                rt = u'<div style="background-color:#C0C0C0">1</div>'
            else:
                rt = u'<div style="background-color:white">0</div>'
        # messages.error(self.request, u'campaign_id%s！'%campaign_id)
        return mark_safe(rt)
    show_newcampaignFlag.short_description = mark_safe('<p style="color:#428bca;text-align:center">当期</p>')

    list_display_links = ('id',)
    list_display = ('show_newcampaignFlag', 'product_id', 'show_date', 'impressions', 'paid_impressions', 'spend', 'sales', 'gmv', 'show_spend_gmv', 'show_expose')

    def get_list_queryset(self):
        request = self.request
        qs = super(t_wish_pb_productdailystats_Admin, self).get_list_queryset()

        campaign_id = request.GET.get('campaign_id', '')
        product_id = request.GET.get('product_id', '')
        startdate = request.GET.get('startdate', '')
        enddate = request.GET.get('enddate', '')

        searchlist = {'campaign_id__exact': campaign_id,
                      'product_id__exact': product_id,
                      'p_date__gte': startdate,
                      'p_date__lt': enddate,
                      }

        sl = {}
        for k, v in searchlist.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有误！')
        return qs
