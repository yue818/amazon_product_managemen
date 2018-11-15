# -*- coding: utf-8 -*-
from django.db import models
from .t_online_info import t_online_info
from .t_store_configuration_file import t_store_configuration_file
#铺货 choices=getChoices(ChoicePlatformName)
from public import *

def getShopNameChoices():
    return set(t_store_configuration_file.objects.values_list('ShopName','ShopName').filter(ShopName__contains='Wish').order_by('ShopName'))
    

class t_distribution_product_to_store(models.Model):
    PlatformName    =   models.CharField(u'平台名称', max_length=16, blank=True, null=True)
    ProductID       =   models.CharField(u'产品ID', max_length=32, blank=True, null=True)
    ShopIP          =   models.CharField(u'店铺IP', max_length=32, blank=True, null=True)
    ShopName        =   models.CharField(u'店铺名称', max_length=32, blank=True, null=True)
    Title           =   models.TextField(u'标题', blank=True, null=True)
    SKU             =   models.CharField(u'子SKU', max_length=32, blank=True, null=True)
    ShopSKU         =   models.CharField(u'店铺SKU', max_length=128, blank=True, null=True)
    Price           =   models.CharField(u'价格', max_length=32, blank=True, null=True)
    Quantity        =   models.PositiveSmallIntegerField(u'库存量', blank=True, null=True)
    Orders7Days     =   models.PositiveSmallIntegerField(u'7天order数', blank=True, null=True)
    SoldYesterday   =   models.PositiveSmallIntegerField(u'昨日售出量', blank=True, null=True)
    SoldTheDay      =   models.PositiveSmallIntegerField(u'当日售出量', blank=True, null=True)
    SoldXXX         =   models.PositiveSmallIntegerField(u'销售差值', blank=True, null=True)
    DateOfOrder     =   models.CharField(u'出单日期 ', max_length=32, blank=True, null=True)
    Remarks         =   models.TextField(u'操作备注', blank=True, null=True)
    RefreshTime     =   models.DateTimeField(u'刷新时间', blank=True, null=True)
    Image           =   models.CharField(u'图片', max_length=200, blank=True, null=True)
    Status          =   models.CharField(u'状态', choices=getChoices(ChoiceStatus_wish), max_length=16, blank=True, null=True)
    ReviewState     =   models.CharField(u'Wish查看状态', choices=getChoices(ChoiceReviewState), max_length=16, blank=True,
                                   null=True)
    DateUploaded    =   models.DateTimeField(u'上架日期/UTC', blank=True, null=True)
    LastUpdated     =   models.DateTimeField(u'最近更新日期/UTC', blank=True, null=True)
    OfSales         =   models.CharField(u'总销量', max_length=10, blank=True, null=True)
    ParentSKU       =   models.CharField(u'父SKU', max_length=32, blank=True, null=True)
    Seller          =   models.CharField(u'店长/销售员', max_length=32, blank=True, null=True)
    FileName        =   models.FileField(u'SKU铺货',blank = True,null = True)
    csvSKU          =   models.CharField(u'csv内SKU',max_length=32,blank = True,null = True)
    csvShop1        =   models.TextField(u'csv内店铺1',blank = True,null = True)
    csvShop2        =   models.TextField(u'csv内店铺2', blank=True, null=True)
    csvShop3        =   models.TextField(u'csv内店铺3', blank=True, null=True)
    FileName2       =   models.FileField(u'已有数据铺货',blank = True,null = True)
    Submitter       =   models.CharField(u'提交人',max_length=10, blank=True, null=True)
    SubTime         =   models.DateTimeField(u'刷新时间', blank=True, null=True)
    SubStatus       =   models.CharField(u'铺货状态',choices=getChoices(ChoiceDistributionStatus),max_length=20,blank=True, null=True)
    Type            =   models.CharField(u'铺货类型',choices=getChoices(ChoiceDistributionType),max_length=20,blank=True,null=True)
    Description     =   models.TextField(u'描述', blank=True, null=True)
    ExtraImages     =   models.TextField(u'副图', blank=True, null=True)
    Tags            =   models.TextField(u'标签', blank=True, null=True)
    ShopNum         =   models.IntegerField(u'店铺个数',max_length=4, blank=True, null=True)
    TimeInterval    =   models.DecimalField(u'店铺铺货间隔时间',max_digits =8,decimal_places =2, blank=True, null=True)
    StartTime       =   models.DateTimeField(u'铺货开始时间', blank=True, null=True)
    EndTime         =   models.DateTimeField(u'铺货结束时间', blank=True, null=True)
    apiingid        =   models.TextField(u'指令执行计划ID', blank=True, null=True)

    class Meta:
        verbose_name=u'铺货记录'
        verbose_name_plural=verbose_name
        db_table = 't_distribution_product_to_store'
        ordering =  ['-id']
    def __unicode__(self):
        return u'%s'%(self.id)
