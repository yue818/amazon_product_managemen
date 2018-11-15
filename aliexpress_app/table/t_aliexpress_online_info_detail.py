#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models


class t_aliexpress_online_info_detail(models.Model):
    ProductID = models.CharField(u'ProductID', max_length=255, blank=True, null=True)
    SKU = models.CharField(u'商品SKU', max_length=255, blank=True, null=True)
    MainSKU = models.CharField(u'主SKU', max_length=255, blank=True, null=True)
    ShopSKU = models.CharField(u'店铺SKU', max_length=255, blank=True, null=True)
    Price = models.CharField(u'价格', max_length=32, blank=True, null=True)
    Quantity = models.IntegerField(u'库存', max_length=32, blank=True, null=True)
    Status = models.CharField(u'状态', max_length=32, blank=True, null=True)
    RealPrice = models.CharField(u'实际销售价格', max_length=32, blank=True, null=True)
    Shipping = models.CharField(u'运费', max_length=32, blank=True, null=True)
    Weight = models.FloatField(u'克重(g)', blank=True, null=True)

    class Meta:
        verbose_name = u'Aliexpress 商品变体信息'
        verbose_name_plural = u'Aliexpress 商品变体信息'
        db_table = 't_aliexpress_online_info_detail'

    def __unicode__(self):
        return u'%s' % (self.id)
