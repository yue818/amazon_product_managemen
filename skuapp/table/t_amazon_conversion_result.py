# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_conversion_result.py
 @time: 2018/12/5 16:27
"""  
from django.db import models


class t_amazon_conversion_result(models.Model):
    conversion_type = models.IntegerField(u'统计类型', max_length=1, blank=True, null=True)
    product_sku = models.CharField(u'商品SKU', max_length=255, blank=True, null=True)
    seller = models.CharField(u'销售员', max_length=32, blank=True, null=True)
    shop_name = models.CharField(u'店铺', max_length=32, blank=True, null=True)
    order_cost = models.DecimalField(u'出单成本', max_digits=10, decimal_places=2, blank=True, null=True)
    inventory_cost = models.DecimalField(u'库存成本', max_digits=10, decimal_places=2, blank=True, null=True)
    conversion_rate = models.DecimalField(u'周转率', max_digits=10, decimal_places=2, blank=True, null=True)
    time_span = models.CharField(u'时间范围', max_length=32, blank=True, null=True)
    refresh_time = models.DateTimeField(u'刷新时间', blank=True, null=True)

    class Meta:
        verbose_name = u'AMZ周转率'
        verbose_name_plural = verbose_name
        db_table = 't_amazon_conversion_result'

    def __unicode__(self):
        return u'%s' % self.id
