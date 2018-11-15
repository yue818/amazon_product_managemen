# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from django.contrib import messages
import datetime
from t_config_wishapi_product_analyse_info_Admin import *

class t_config_wishapi_product_analyse_info_xpbs_Admin(t_config_wishapi_product_analyse_info_Admin):

    def get_list_queryset(self, ):
        request = self.request
        qs = super(t_config_wishapi_product_analyse_info_xpbs_Admin, self).get_list_queryset()
        Pid = request.GET.get('Pid', '')
        Name = request.GET.get('Name', '')
        YNDone = request.GET.get('YNDone', '')
        NumBoughtStart = request.GET.get('NumBoughtStart', '')
        NumBoughtEnd = request.GET.get('NumBoughtEnd', '')
        UnitPriceStart = request.GET.get('UnitPriceStart', '')
        UnitPriceEnd = request.GET.get('UnitPriceEnd', '')
        OrdersLast7DaysStart = request.GET.get('OrdersLast7DaysStart', '')
        OrdersLast7DaysEnd = request.GET.get('OrdersLast7DaysEnd', '')

        OrdersLast7to14DaysStart_rq = request.GET.get('OrdersLast7to14DaysStart', '')
        OrdersLast7to14DaysStart = u'11'
        if OrdersLast7to14DaysStart_rq:
            if int(OrdersLast7to14DaysStart_rq) > int(OrdersLast7to14DaysStart):
                OrdersLast7to14DaysStart = OrdersLast7to14DaysStart_rq
                messages.error(request, '请输入大于11的前8-14天order数' )
        OrdersLast7to14DaysEnd = request.GET.get('OrdersLast7to14DaysEnd', '')

        SupplierID = request.GET.get('SupplierID', '')
        DealName = request.GET.get('DealName', '')
        DealTimeStart = request.GET.get('DealTimeStart', '')
        DealTimeEnd = request.GET.get('DealTimeEnd', '')
        Op_timeStart = request.GET.get('Op_timeStart', '')
        Op_timeEnd = request.GET.get('Op_timeEnd', '')

        ShelveDayStart_rq = request.GET.get('ShelveDayStart', '')
        ShelveDayStart = (datetime.datetime.now() + datetime.timedelta(days=-60)).strftime('%Y-%m-%d')
        if ShelveDayStart_rq:
            st = datetime.datetime.strptime(ShelveDayStart_rq, "%Y-%m-%d")
            ed = datetime.datetime.strptime(ShelveDayStart, "%Y-%m-%d")
            daycount = (ed - st).days
            if daycount < 0:
                ShelveDayStart = ShelveDayStart_rq
                messages.error(request, '请输入上架时间为60天内的时间')
        ShelveDayEnd = request.GET.get('ShelveDayEnd', '')

        Collar = request.GET.get('Collar', '')

        searchList = {'Pid__exact': Pid, 'Name__contains': Name,'YNDone__exact': YNDone,
                      'NumBought__gte': NumBoughtStart, 'NumBought__lt': NumBoughtEnd,
                      'UnitPrice__gte': UnitPriceStart, 'UnitPrice__lt': UnitPriceEnd,
                      'OrdersLast7Days__gte': OrdersLast7DaysStart, 'OrdersLast7Days__lt': OrdersLast7DaysEnd,
                      'OrdersLast7to14Days__gte': OrdersLast7to14DaysStart, 'OrdersLast7to14Days__lt': OrdersLast7to14DaysEnd,
                      'SupplierID__exact': SupplierID, 'DealName__exact': DealName,
                      'DealTime__gte': DealTimeStart, 'DealTime__lt': DealTimeEnd,
                      'Op_time__gte': Op_timeStart, 'Op_time__lt': Op_timeEnd,
                      'ShelveDay__gte': ShelveDayStart, 'ShelveDay__lt': ShelveDayEnd,
                      'Collar__exact': Collar,
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
                messages.error(request, u'Please enter the correct content!')
        return qs