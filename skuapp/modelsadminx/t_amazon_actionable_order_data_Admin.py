# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_actionable_order_data_Admin.py
 @time: 2018/10/17 9:51
"""
from django.contrib import messages
from Project.settings import *
from xlwt import *
import errno
import datetime
import oss2


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5 (except OSError, exc: for Python <2.5)
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class t_amazon_actionable_order_data_Admin(object):
    amazon_site_left_menu_tree_flag = True
    search_box_flag = True
    downloadxls = True
    list_display = ('shop_name', 'sku', 'order_id', 'purchase_date', 'payments_date', 'promise_date','days_past_promise','quantity_purchased',
                    'quantity_shipped','quantity_to_ship','ship_service_level', 'refresh_time')

    def get_list_queryset(self, ):
        request = self.request
        shop_name = request.GET.get('shop_name', '')
        sku = request.GET.get('sku', '')
        sku = '' if sku == '' else sku.strip().replace(' ', '+').split(',')
        order_id = request.GET.get('order_id', '')
        order_id = '' if order_id == '' else order_id.strip().split(',')
        payments_date_start = request.GET.get('payments_date_start', '')
        payments_date_end = request.GET.get('payments_date_end', '')

        qs = super(t_amazon_actionable_order_data_Admin, self).get_list_queryset()

        search_list = {
                      'shop_name__icontains':  shop_name,
                      'sku__in': sku,
                      'order_id__in': order_id,
                      'payments_date__gte': payments_date_start,
                      'payments_date__lte': payments_date_end,
                      }
        sl = {}
        for k, v in search_list.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and str(v).strip() != '':
                    sl[k] = v
        if sl is not None:
            try:
                qs = qs.filter(**sl)
            except Exception, ex:
                messages.error(request, u'Please enter the correct content!')
        return qs
