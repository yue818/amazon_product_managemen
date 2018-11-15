#!/usr/bin/python
# -*- coding: utf-8 -*-

from aliexpress_app.table.t_aliexpress_online_info import t_aliexpress_online_info


# Aliexpress 比价
class t_aliexpress_price_parity(t_aliexpress_online_info):

    class Meta:
        verbose_name = u'Aliexpress 比价管理'
        verbose_name_plural = verbose_name
        proxy = True
        ordering = ['Orders7Days']
