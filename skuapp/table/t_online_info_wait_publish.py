# -*- coding: utf-8 -*-
from django.db import models
from public import *


class t_online_info_wait_publish(models.Model):
    PlatformName    =   models.CharField(u'平台名称',max_length=16,blank = True,null = True)
    ProductID       =   models.CharField(u'产品ID',max_length=32,blank = True,null = True)
    ShopIP          =   models.CharField(u'店铺IP',max_length=32,blank = True,null = True)
    ShopName        =   models.CharField(u'店铺名称',max_length=32,blank = True,null = True)
    Title           =   models.TextField(u'标题',blank = True,null = True)
    SKU             =   models.CharField(u'子SKU',max_length=32,blank = True,null = True)
    ShopSKU         =   models.CharField(u'店铺SKU',max_length=128,blank = True,null = True)
    Price           =   models.CharField(u'价格',max_length=32,blank = True,null = True)
    Quantity        =   models.PositiveSmallIntegerField(u'库存量',blank = True,null = True)
    Orders7Days     =   models.PositiveSmallIntegerField(u'7天order数',blank = True,null = True)
    SoldYesterday   =   models.PositiveSmallIntegerField(u'昨日售出量',blank = True,null = True)
    SoldTheDay      =   models.PositiveSmallIntegerField(u'当日售出量',blank = True,null = True)
    SoldXXX         =   models.PositiveSmallIntegerField(u'销售差值',blank = True,null = True)
    DateOfOrder     =   models.CharField(u'出单日期 ',max_length=32,blank = True,null = True)
    Remarks         =   models.TextField(u'操作备注',blank = True,null = True)
    RefreshTime     =   models.DateTimeField(u'刷新时间',blank = True,null = True)
    Image           =   models.CharField(u'图片',max_length=200,blank = True,null = True)
    Status          =   models.CharField(u'状态',choices=getChoices(ChoiceStatus_wish),max_length=16,blank = True,null = True)
    ReviewState     =   models.CharField(u'Wish查看状态',choices=getChoices(ChoiceReviewState),max_length=16,blank = True,null = True)
    DateUploaded    =   models.DateTimeField(u'上架日期/UTC',blank = True,null = True)
    LastUpdated     =   models.DateTimeField(u'最近更新日期/UTC',blank = True,null = True)
    OfSales         =   models.CharField(u'总销量',max_length=10,blank = True,null = True)
    ParentSKU       =   models.CharField(u'父SKU',max_length=32,blank = True,null = True)
    Seller          =   models.CharField(u'店长/销售员',max_length=32,blank = True,null = True)
    ispublished     =   models.CharField(u'是否刊登',choices=getChoices(ChoicePublish),max_length=32)


    class Meta:
        verbose_name=u'全部商品信息'
        verbose_name_plural=verbose_name
        db_table = 't_online_info_wait_publish'
        ordering = ['-Orders7Days']
    def __unicode__(self):
        return u'id:%s'%(self.id)