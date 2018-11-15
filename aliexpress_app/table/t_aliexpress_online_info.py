#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models


# Aliexpress商品信息
class t_aliexpress_online_info(models.Model):
    ProductID = models.CharField(u'产品ID', max_length=255, blank=True, null=True)
    ShopName = models.CharField(u'店铺名称', max_length=255, blank=True, null=True)
    Title = models.TextField(u'标题', blank=True, null=True)
    SKU = models.TextField(u'子SKU', blank=True, null=True)
    # MainSKU = models.TextField(u'MainSKU', blank=True, null=True)
    MainSKU = models.CharField(u'MainSKU', max_length=255, blank=True, null=True)
    ShopSKU = models.TextField(u'店铺SKU', blank=True, null=True)
    Quantity = models.PositiveSmallIntegerField(u'库存量', blank=True, null=True)
    Orders7Days = models.PositiveSmallIntegerField(u'7天order数', blank=True, null=True)
    RefreshTime = models.DateTimeField(u'刷新时间', blank=True, null=True)
    Price = models.CharField(u'价格', max_length=32, blank=True, null=True)
    ProfitRate = models.CharField(u'利润率区间', max_length=255, blank=True, null=True)
    Image = models.TextField(u'图片', blank=True, null=True)
    Status = models.CharField(u'启用状态', max_length=16, blank=True, null=True)
    ReviewState = models.CharField(u'Aliexpress状态', max_length=16, blank=True, null=True)
    OfSales = models.IntegerField(u'总销量', max_length=10, blank=True, null=True)
    TortInfo = models.CharField(u'侵权状态', max_length=16, blank=True, null=True)
    ratingValue = models.IntegerField(u'商品评分', max_length=64, blank=True, null=True)
    competitor_ProductID = models.CharField(u'对手ID', max_length=255, blank=True, null=True,)
    priceParity_Status = models.CharField(u'比价状态', max_length=32, blank=True, null=True)
    priceParity_Person = models.CharField(u'比价人员', max_length=255, blank=True, null=True)
    priceParity_Datetime = models.DateTimeField(u'比价时间', blank=True, null=True)
    priceParity_Remarks = models.TextField(u'备注', blank=True, null=True)

    Weight = models.FloatField(u'克重(g)', blank=True, null=True)
    CanPriceParity = models.BooleanField(u'可比价状态', blank=True, default=False)

    class Meta:
        verbose_name = u'Aliexpress 在线管理'
        verbose_name_plural = verbose_name
        db_table = 't_aliexpress_online_info'
        # db_table = 't_aliexpress_online_info_test0512'
        # ordering = ['-Orders7Days']

    def __unicode__(self):
        return u'id:%s' % (self.id)
