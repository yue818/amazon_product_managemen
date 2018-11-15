# -*- coding: utf-8 -*-
from django.db import models
from public import *
from pyapp.models import *


class t_goods_shelves(models.Model):
    PlatformName       =   models.CharField(u'平台名称',max_length=16,blank = True,null = True)
    ProductID          =   models.CharField(u'产品ID',max_length=63,blank = True,null = True)
    ShopIP             =   models.CharField(u'店铺IP',max_length=16,blank = True,null = True)
    ShopName           =   models.CharField(u'店铺名称',max_length=63,blank = True,null = True)
    Seller             =   models.CharField(u'销售员',max_length=63,blank = True,null = True)
    Published          =   models.CharField(u'刊登员',max_length=63,blank = True,null = True)
    Title              =   models.TextField(u'标题',blank = True,null = True)
    SKU                =   models.CharField(u'SKU',max_length=31,blank = True,null = True)
    ShopSKU            =   models.CharField(u'店铺SKU',max_length=127,blank = True,null = True)
    Price              =   models.CharField(u'价格',max_length=31,blank = True,null = True)
    Quantity           =   models.CharField(u'库存',max_length=31,blank = True,null = True)
    RefreshTime        =   models.DateTimeField(u'刷新时间',blank = True,null = True)
    Image              =   models.CharField(u'图片URL',max_length=200,blank = True,null = True)
    Status             =   models.CharField(u'状态',choices=getChoices(ChoiceStatus_wish),max_length=16,blank = True,null = True)
    DateUploaded       =   models.CharField(u'上传时间',max_length=31,blank = True,null = True)
    ParentSKU          =   models.CharField(u'父SKU',max_length=31,blank = True,null = True)
    ReviewState        =   models.CharField(u'Wish查看状态',choices=getChoices(ChoiceReviewState),max_length=16,blank = True,null = True)
    OfWishes           =   models.PositiveSmallIntegerField(u'收藏数',max_length=8,blank = True,null = True)
    OfSales            =   models.PositiveSmallIntegerField(u'订单量',max_length=8,blank = True,null = True)
    LastUpdated        =   models.CharField(u'最近更新时间',max_length=31,blank = True,null = True)
    Shipping           =   models.CharField(u'运费',max_length=8,blank = True,null = True)
    Color              =   models.CharField(u'颜色',max_length=31,blank = True,null = True)
    Size               =   models.CharField(u'尺寸',max_length=31,blank = True,null = True)
    msrp               =   models.CharField(u'标签价',max_length=15,blank = True,null = True)
    ShippingTime       =   models.CharField(u'运输时间',max_length=31,blank = True,null = True)
    ExtraImages        =   models.TextField(u'副图',blank = True,null = True)
    VariationID        =   models.CharField(u'变体ID',max_length=31,blank = True,null = True)
    Description        =   models.TextField(u'描述',blank = True,null = True)
    Tags               =   models.TextField(u'标签',blank = True,null = True)
    MainSKU            =   models.CharField(u'主SKU',max_length=31,blank = True,null = True)
    MainShopSKU        =   models.CharField(u'主店铺SKU',max_length=31,blank = True,null = True)
    APIState           =   models.CharField(u'api执行状态',choices=getChoices(ChoiceAPIState),max_length=15,blank = True,null = True)
    OperationState     =   models.CharField(u'下架状态',choices=getChoices(ChoiceOperationState),max_length=15,blank = True,null = True)
    Orders7Days        =   models.PositiveSmallIntegerField(u'7天order数',blank = True,null = True)
    GoodsStatus        =   models.CharField(u'商品状态',choices=getChoices(ChoiceGoodsStatus),max_length=10,blank=True,null=True)
    DepartmentID       =   models.CharField(u'部门编号',max_length=5,blank = True,null = True)
    Error              =   models.TextField(u'api错误信息',blank = True,null = True)
    filtervalue        =   models.IntegerField(u'过滤条件',max_length = 1,blank = True,null = True)
    AvailableStock_SKU =   models.IntegerField(u'可用库存',max_length = 8,blank = True,null = True)

    class Meta:
        verbose_name=u'Wish商品下架'
        verbose_name_plural=verbose_name
        db_table = 't_online_info'
        ordering =  ['-Orders7Days']
        
    def __unicode__(self):
        return u'%s'%(self.id)