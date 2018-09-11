# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_orders_by_receive_day_total.py
 @time: 2018/9/10 16:55
"""

from django.db import models


class t_amazon_orders_by_receive_day_total(models.Model):
    is_fba = models.IntegerField(u'是否FBA', max_length=1, blank=True, null=True)
    product_sku = models.CharField(u'商品SKU', max_length=32, blank=True, null=True)
    sku_unit_price = models.FloatField(u'商品单价', max_length=10, blank=True, null=True)
    quantity = models.IntegerField(u'库存量', max_length=10, blank=True, null=True)
    total_price = models.FloatField(u'总成本', max_length=12, blank=True, null=True)
    UpdateTime = models.DateTimeField(u'更新时间', blank=True, null=True)

    class Meta:
        verbose_name = u'AMZ商品库存成本'
        verbose_name_plural = verbose_name
        db_table = 't_amazon_orders_by_receive_day_total'

    def __unicode__(self):
        return u'%s' % self.id