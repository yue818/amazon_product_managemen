#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models


# Aliexpress 对手商品信息
class t_aliexpress_competitor_product_info(models.Model):

    ProductID = models.CharField(u'产品ID', max_length=255, blank=True, null=True, unique=True)
    Image = models.TextField(u'图片', blank=True, null=True)
    Title = models.TextField(u'Title', blank=True, null=True)
    Unit = models.CharField(u'单位', max_length=255, blank=True, null=True)
    maxPrice = models.CharField(u'最高价格', max_length=255, blank=True, null=True)
    minPrice = models.CharField(u'最底价格', max_length=255, blank=True, null=True)
    maxProfitRate = models.CharField(u'最高利润率', max_length=255, blank=True, null=True)
    minProfitRate = models.CharField(u'最底利润率', max_length=255, blank=True, null=True)
    ratingValue = models.CharField(u'商品评分', max_length=255, blank=True, null=True)
    Orders7Days = models.PositiveSmallIntegerField(u'7天order数', blank=True, null=True)
    RefreshDate = models.DateTimeField(u'刷新时间', blank=True, null=True)
    LastRefreshDate = models.DateTimeField(u'上次刷新时间', blank=True, null=True)
    RefreshStatus = models.CharField(u'刷新结果', max_length=255, blank=True, null=True)
    Orders = models.IntegerField(u'order数', blank=True, null=True)

    class Meta:
        verbose_name = u'Aliexpress 对手商品信息'
        verbose_name_plural = verbose_name
        db_table = 't_aliexpress_competitor_product_info'
