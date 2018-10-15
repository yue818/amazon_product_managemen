# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_estimated_fba_fees.py
 @time: 2018/10/7 15:11
"""  
from django.db import models


class t_amazon_estimated_fba_fees(models.Model):
    shop_name = models.CharField(u'店铺', max_length=32, blank=True, null=True)
    sku = models.CharField(u'商品SKU', max_length=255, blank=True, null=True)
    asin = models.CharField(u'ASIN', max_length=64, blank=True, null=True)
    longest_side = models.CharField(u'长边', max_length=32, blank=True, null=True)
    median_side = models.CharField(u'中边', max_length=32, blank=True, null=True)
    shortest_side = models.CharField(u'短边', max_length=32, blank=True, null=True)
    unit_of_dimension = models.CharField(u'尺寸单位', max_length=32, blank=True, null=True)
    item_package_weight = models.CharField(u'重量', max_length=32, blank=True, null=True)
    unit_of_weight = models.CharField(u'重量单位', max_length=32, blank=True, null=True)
    product_size_tier = models.CharField(u'尺寸分段', max_length=32, blank=True, null=True)
    estimated_fee = models.CharField(u'预览费用', max_length=32, blank=True, null=True)
    expected_fulfillment_fee_per_unit = models.CharField(u'运费', max_length=32, blank=True, null=True)
    currency = models.CharField(u'货币单位', max_length=32, blank=True, null=True)
    refresh_time = models.DateTimeField(u'刷新时间', blank=True, null=True)

    class Meta:
        verbose_name = u'AMZ预览费用'
        verbose_name_plural = verbose_name
        db_table = 't_amazon_estimated_fba_fees'

    def __unicode__(self):
        return u'%s' % self.id