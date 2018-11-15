# -*- coding: utf-8 -*-

# 更新t_product_enter_ed表的Aliexpress_PL字段(速卖通品类)

from skuapp.table.t_config_aliexpress_pl import t_config_aliexpress_pl
from skuapp.table.t_product_enter_ed_aliexpress import t_product_enter_ed_aliexpress
from aliapp.models import t_erp_aliexpress_shop_info
from django.contrib.auth.models import User
import datetime


def update_Aliexpress_PL():
    start_time = datetime.datetime.now()
    print 'start time: %s' % start_time
    data = t_product_enter_ed_aliexpress.objects.all()
    for d in data:
        LargeCategory = d.LargeCategory
        aliexpress_list = list()
        aliexpress_data = t_config_aliexpress_pl.objects.all()
        for a_d in aliexpress_data:
            py_pl_list = a_d.py_pl.split(';')
            if LargeCategory in py_pl_list:
                aliexpress_list.append(a_d.aliexpress_pl)
        if '' in aliexpress_list:
            aliexpress_list.remove('')
        if aliexpress_list:
            d.Aliexpress_PL = ','.join(aliexpress_list)
            d.save()
    end_time = datetime.datetime.now()
    print 'end time: %s' % end_time
    handle_time = (end_time - start_time).total_seconds()
    print 'handle time: %s' % handle_time
