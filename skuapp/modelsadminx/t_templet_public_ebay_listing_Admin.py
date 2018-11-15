# -*- coding: utf-8 -*-


from skuapp.modelsadminx.t_online_info_ebay_Admin import *
from django.contrib import messages

class t_templet_public_ebay_listing_Admin(t_online_info_ebay_Admin):
    search_box_flag = True
    plateform_distribution_navigation = True

    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_templet_public_ebay_listing_Admin, self).get_list_queryset()
        id = request.GET.get('id', '')
        status = request.GET.get('status', '')
        ShopName = request.GET.get('ShopName', '')
        itemid = request.GET.get('itemid', '')

        title = request.GET.get('title', '')
        subSKU = request.GET.get('subSKU', '')
        Orders7DaysStart = request.GET.get('Orders7DaysStart', '')
        Orders7DaysEnd = request.GET.get('Orders7DaysEnd', '')

        soldStart = request.GET.get('soldStart', '')
        soldEnd = request.GET.get('soldEnd', '')
        starttime_Start = request.GET.get('starttime_Start', '')
        starttime_End = request.GET.get('starttime_End', '')
        endtime_Start = request.GET.get('endtime_Start', '')
        endtime_End = request.GET.get('endtime_End', '')

        if subSKU:
            t_online_info_ebay_subsku_objs = t_online_info_ebay_subsku.objects.filter(subSKU=subSKU).values('itemid')
            if not t_online_info_ebay_subsku_objs:
                itemid = '1'  # itemid不能为1
            elif itemid and itemid <> t_online_info_ebay_subsku_objs[0]['itemid']:
                itemid = '1'
            elif not itemid:
                itemid = t_online_info_ebay_subsku_objs[0]['itemid']

        searchList = {'id__exact':id, 'status__exact': status, 'ShopName__exact': ShopName, 'itemid__exact': itemid,
                      'title__contains': title,
                      'Orders7Days__gte': Orders7DaysStart, 'Orders7Days__lt': Orders7DaysEnd,
                      'sold__gte': soldStart, 'sold__lt': soldEnd,
                      'starttime__gte': starttime_Start, 'starttime__lt': starttime_End,
                      'endtime__gte': endtime_Start, 'endtime__lt': endtime_End,
                      }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')
        return qs




