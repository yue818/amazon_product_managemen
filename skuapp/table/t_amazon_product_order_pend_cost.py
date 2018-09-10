# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_product_order_pend_cost.py
 @time: 2018/9/6 14:13
"""  
from django.db import models


class t_amazon_product_order_pend_cost(models.Model):
    product_sku = models.CharField(u'商品SKU', max_length=32, blank=True, null=True)
    sku_unit_price = models.FloatField(u'商品单价', max_length=10, blank=True, null=True)
    quantity = models.IntegerField(u'Pending商品量', max_length=10, blank=True, null=True)
    total_price = models.FloatField(u'总成本', max_length=12, blank=True, null=True)
    refresh_time = models.DateTimeField(u'更新时间', blank=True, null=True)

    class Meta:
        verbose_name = u'AMZ Pending订单汇总'
        verbose_name_plural = verbose_name
        db_table = 't_amazon_product_order_pend_cost'

    def __unicode__(self):
        return u'%s' % self.id