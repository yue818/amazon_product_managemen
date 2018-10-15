#-*-coding:utf-8-*-
u"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_wish_daily_sales_statistics_Admin.py
 @time: 2018/9/5 9:50
"""
from django.contrib import messages

class t_wish_daily_sales_statistics_Admin(object):

    daily_sales_chart = True
    search_box_flag = True

    list_display  = ['id', 'OrderDate', 'OfSales',]
    search_fields = None
    list_filter   = None

    def get_list_queryset(self,):
        request = self.request
        qs = super(t_wish_daily_sales_statistics_Admin, self).get_list_queryset()

        seachfilter = {}
        OfSalesStart = request.GET.get('OfSalesStart')
        if OfSalesStart:
            seachfilter['OfSales__gte'] = OfSalesStart

        OfSalesEnd = request.GET.get('OfSalesEnd')
        if OfSalesEnd:
            seachfilter['OfSales__lt'] = OfSalesEnd

        OrderDateStart = request.GET.get('OrderDateStart')
        if OrderDateStart:
            seachfilter['OrderDate__gte'] = OrderDateStart

        OrderDateEnd = request.GET.get('OrderDateEnd')
        if OrderDateEnd:
            seachfilter['OrderDate__lt'] = OrderDateEnd

        try:
            qs = qs.filter(**seachfilter)
        except Exception as error:
            messages.error(request, u'{}'.format(error))

        return qs