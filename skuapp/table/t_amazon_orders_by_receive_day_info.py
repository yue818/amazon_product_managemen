# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_orders_by_receive_day_info.py
 @time: 2018/9/11 11:11
"""  
from django.db import models


class t_amazon_orders_by_receive_day_info(models.Model):
    shopname = models.CharField(u'店铺', max_length=32, blank=True, null=True)
    seller = models.CharField(u'销售员', max_length=32, blank=True, null=True)
    site = models.CharField(u'站点', max_length=32, blank=True, null=True)
    sku = models.CharField(u'商品SKU', max_length=255, blank=True, null=True)
    seller_sku = models.CharField(u'店铺SKU', max_length=255, blank=True, null=True)
    asin = models.CharField(u'ASIN', max_length=64, blank=True, null=True)
    received_date = models.DateTimeField(u'到货时间', blank=True, null=True)
    mainsku = models.CharField(u'主SKU', max_length=64, blank=True, null=True)
    categorycode = models.CharField(u'品类', max_length=64, blank=True, null=True)
    orders_after_14days = models.IntegerField(u'到货后两周订单数', max_length=10, blank=True, null=True)
    time_span = models.CharField(u'到货时间范围', max_length=32, blank=True, null=True)
    refresh_time = models.DateTimeField(u'刷新时间', blank=True, null=True)

    class Meta:
        verbose_name = u'AMZ按到货日期出单详单'
        verbose_name_plural = verbose_name
        db_table = 't_amazon_orders_by_receive_day_info'

    def __unicode__(self):
        return u'%s' % self.id
