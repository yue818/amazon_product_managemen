# -*- coding: utf-8 -*-
from skuapp.table.t_config_apiurl_asin_operation import *


class t_config_apiurl_asin_operation_Admin(object):
    search_box_flag = True
    list_display = (
        'id', 'OperationWeek', 'OperationMan', 'Developed', 'Repeation', 'Handled',)
    list_editable = None

    def get_list_queryset(self):
        request = self.request
        qs = super(t_config_apiurl_asin_operation_Admin, self).get_list_queryset()

        OperationWeek = request.GET.get('OperationWeek', '')
        OperationMan = request.GET.get('OperationMan', '')

        DevelopedStart = request.GET.get('DevelopedStart', '')
        DevelopedEnd = request.GET.get('DevelopedEnd', '')

        searchList = {'OperationWeek__exact': OperationWeek,
                      'OperationMan__exact': OperationMan,

                      'Developed__gte': DevelopedStart, 'Developed__lt': DevelopedEnd,
                      }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    # if k == 'ShopName__exact':
                    #  v = 'Wish-' + v.zfill(4)
                    # messages.error(request, v)
                    sl[k] = v
        if sl is not None:
            # messages.error(request, sl)
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'输入的查询数据有问题！')

        return qs