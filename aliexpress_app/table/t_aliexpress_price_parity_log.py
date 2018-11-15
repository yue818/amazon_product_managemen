#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models


class t_aliexpress_price_parity_log(models.Model):

    ProductID = models.CharField(u'产品ID', max_length=255, blank=True, null=True)
    ShopSKU = models.CharField(u'店铺SKU', max_length=255, blank=True, null=True)
    OldPrice = models.CharField(u'原商品价格', max_length=255, blank=True, null=True)
    OldSales = models.CharField(u'比价前商品销量', max_length=255, blank=True, null=True)
    NewPrice = models.CharField(u'比价后商品价格', max_length=255, blank=True, null=True)
    ChangePriceDatetime = models.DateTimeField(u'比价时间', blank=True, null=True)
    priceParity_Person = models.CharField(u'比价人员', max_length=255, blank=True, null=True)
    ChangeFlag = models.CharField(u'是否比价', max_length=32, blank=True, null=True)
    ChangeRes = models.CharField(u'比价操作结果', max_length=32, blank=True, null=True)
    ChangeResMess = models.TextField(u'比价操作结果信息', blank=True, null=True)

    class Meta:
        verbose_name = u'Aliexpress 比价记录'
        verbose_name_plural = verbose_name
        db_table = 't_aliexpress_price_parity_log'
