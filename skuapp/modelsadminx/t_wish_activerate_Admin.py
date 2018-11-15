#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: changyang  
 @site: 
 @software: PyCharm
 @file: t_wish_activerate_Admin.py
 @time: 2018-08-20 15:37
"""

from django.utils.safestring import mark_safe
from django.contrib import messages

class t_wish_activerate_Admin(object):
    wish_activerate_chart = True
    search_box_flag = True

    def show_weeklytrend(self, obj):

        rt = ''
        if obj.PeriodType == 1:
            rt = "<a id=weeklytrend_%s>周出单趋势</a><script>$('#weeklytrend_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'趋势图',fix:false,shadeClose: true,maxmin:true,area:['1000px','600px'],content:'/wish_activerate/weeklytrend/?PeriodNO=%s',});});</script>" % (
            obj.id, obj.id, obj.PeriodNO)

        return mark_safe(rt)

    show_weeklytrend.short_description = mark_safe('<p style="color:#428bca;">操作</p>')

    list_display = ('PeriodNO', 'PeriodType', 'PeriodStart', 'PeriodEnd', 'UploadCnt', 'OrderCnt', 'ActiveRate', 'Sales', 'show_weeklytrend')

    list_display_links = ('id')

    list_per_page = 50


    def get_list_queryset(self):
        request = self.request
        qs = super(t_wish_activerate_Admin, self).get_list_queryset()

        searchList = {}

        PeriodType = request.GET.get('PeriodType', '1')
        searchList['PeriodType__exact'] = PeriodType

        PeriodStart = request.GET.get('PeriodStart', '')
        if PeriodStart != '':
            searchList['PeriodStart__gte'] = PeriodStart

        PeriodEnd  = request.GET.get('PeriodEnd', '')
        if PeriodEnd != '':
            searchList['PeriodEnd__lt'] = PeriodEnd

        try:
            qs = qs.filter(**searchList)
        except Exception, ex:
            messages.error(request, u'输入的查询数据有问题！')

        return qs