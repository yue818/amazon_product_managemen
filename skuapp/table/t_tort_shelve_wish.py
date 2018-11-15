# -*- coding: utf-8 -*-
from django.db import models
from public import *


class t_tort_shelve_wish(models.Model):
    PlatformName = models.CharField(u'平台名称', max_length=16, blank=True, null=True)
    ProductID = models.CharField(u'产品ID', max_length=63, blank=True, null=True)
    ShopIP = models.CharField(u'店铺IP', max_length=16, blank=True, null=True)
    ShopName = models.CharField(u'店铺名称', max_length=63, blank=True, null=True)
    Seller = models.CharField(u'销售员', max_length=63, blank=True, null=True)
    Published = models.CharField(u'刊登员', max_length=63, blank=True, null=True)
    Title = models.TextField(u'标题', blank=True, null=True)
    SKU = models.CharField(u'SKU', max_length=31, blank=True, null=True)
    ShopSKU = models.CharField(u'店铺SKU', max_length=127, blank=True, null=True)
    Price = models.CharField(u'价格', max_length=31, blank=True, null=True)
    Quantity = models.CharField(u'库存', max_length=31, blank=True, null=True)
    RefreshTime = models.DateTimeField(u'刷新时间', blank=True, null=True)
    Image = models.CharField(u'图片URL', max_length=200, blank=True, null=True)
    Status = models.CharField(u'状态', choices=getChoices(ChoiceStatus_wish), max_length=16, blank=True, null=True)
    DateUploaded = models.CharField(u'上传时间', max_length=31, blank=True, null=True)
    ParentSKU = models.CharField(u'父SKU', max_length=31, blank=True, null=True)
    ReviewState = models.CharField(u'Wish查看状态', choices=getChoices(ChoiceReviewState), max_length=16, blank=True,
                                   null=True)
    OfWishes = models.PositiveSmallIntegerField(u'收藏数', max_length=8, blank=True, null=True)
    OfSales = models.PositiveSmallIntegerField(u'订单量', max_length=8, blank=True, null=True)
    LastUpdated = models.CharField(u'最近更新时间', max_length=31, blank=True, null=True)
    Shipping = models.CharField(u'运费', max_length=8, blank=True, null=True)
    Color = models.CharField(u'颜色', max_length=31, blank=True, null=True)
    Size = models.CharField(u'尺寸', max_length=31, blank=True, null=True)
    msrp = models.CharField(u'标签价', max_length=15, blank=True, null=True)
    ShippingTime = models.CharField(u'运输时间', max_length=31, blank=True, null=True)
    ExtraImages = models.TextField(u'副图', blank=True, null=True)
    VariationID = models.CharField(u'变体ID', max_length=31, blank=True, null=True)
    Description = models.TextField(u'描述', blank=True, null=True)
    Tags = models.TextField(u'标签', blank=True, null=True)
    MainSKU = models.CharField(u'主SKU', max_length=31, blank=True, null=True)
    MainShopSKU = models.CharField(u'主店铺SKU', max_length=31, blank=True, null=True)
    OperationState = models.CharField(u'API执行状态', choices=getChoices(ChoiceOperationState), max_length=15, blank=True,null=True)
    onemark = models.TextField(u'---备注---',blank = True,null = True)
    Orders7Days = models.PositiveSmallIntegerField(u'7天order数', blank=True, null=True)
    RemarkReason = models.TextField(u'操作原因备注', blank=True, null=True)
    OperationTime = models.CharField(u'下架时间', blank=True, max_length=31, null=True)
    ShelveTime = models.CharField(u'被识别成仿品时间', blank=True, max_length=31, null=True)
    OperationMan = models.CharField(u'操作人', blank=True, max_length=31, null=True)

    class Meta:
        verbose_name=u'wish仿品_一键下架'
        verbose_name_plural=verbose_name
        db_table = 't_tort_shelve_wish'
        ordering =  ['-Orders7Days']
        
    def __unicode__(self):
        return u'%s'%(self.id)