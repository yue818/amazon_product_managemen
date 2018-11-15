# -*- coding: utf-8 -*-
from django.db import models
from public import *


class t_online_info_ebay(models.Model):
    itemid          =   models.CharField(u'产品标识ID',max_length=32,blank = True,null = True)
    title           =   models.TextField(u'标题',blank = True,null = True)
    currentprice    =   models.FloatField(u'现在价格',max_length=12)
    available       =   models.PositiveSmallIntegerField(u'库存量',blank = True,null = True)
    Orders7Days     =   models.PositiveSmallIntegerField(u'7天销量',blank = True,null = True)
    SoldYesterday   =   models.PositiveSmallIntegerField(u'昨日售出量',blank = True,null = True)
    SoldTheDay      =   models.PositiveSmallIntegerField(u'当日售出量',blank = True,null = True)
    SoldXXX         =   models.PositiveSmallIntegerField(u'销售差值',blank = True,null = True)
    DateOfOrder     =   models.CharField(u'出单日期 ',max_length=32,blank = True,null = True)
    Remarks         =   models.TextField(u'操作备注',blank = True,null = True)
    img             =   models.CharField(u'图片',max_length=200,blank = True,null = True)
    status          =   models.CharField(u'链接状态',max_length=16,blank = True,null = True)
    starttime       =   models.CharField(u'上架日期/UTC',max_length=32,blank = True,null = True)
    endtime         =   models.CharField(u'下架日期/UTC',max_length=32,blank = True,null = True)
    sold            =   models.CharField(u'总销量',max_length=10,blank = True,null = True)
    ShopName        =   models.CharField(u'店铺名',max_length=64,blank = True,null = True)
    site            =   models.CharField(u'站点',max_length=10,blank = True,null = True)
    # Variations      =   models.TextField(u'变体',blank = True,null = True)
    SKU             =   models.CharField(u'SKU',max_length=64,blank = True,null = True)
    seller          =   models.TextField(u'店长/销售员',blank = True,null = True)
    lastRefreshTime =   models.DateField(u'在线刷新时间',blank = True,null = True)
    Published       =   models.TextField(u'刊登人',max_length=32,blank = True,null = True)
    # DateUploaded    =   models.TextField(u'上架日期/UTC',max_length=32,blank = True,null = True)
    LastUpdated     =   models.TextField(u'最近更新日期/UTC',blank = True,null = True)
    is_promoted     =   models.TextField(u'是否营销',max_length=8,blank = True,null = True)
    dostatus        =   models.CharField(u'操作状态',max_length=32,blank = True,null = True)
    info            =   models.TextField(u'错误信息',max_length=32,blank = True,null = True)

    hitCount        =   models.IntegerField(u'浏览量', max_length=11, blank=True, null=True)
    watchCount      =   models.IntegerField(u'收藏量', max_length=11, blank=True, null=True)
    Operator        =   models.CharField(u'操作人', max_length=32, blank=True, null=True)
    OperaType       =   models.CharField(u'操作类型', max_length=32, blank=True, null=True)

    Productstatus   =   models.CharField(u'商品SKU状态',max_length=12,blank=True, null=True)
    Productsku      =   models.CharField(u'商品SKU',max_length=100,blank=True, null=True)
    Country         =   models.CharField(u'发货城市',max_length=20,blank=True, null=True)
    UseNumber = models.IntegerField(u'可用数量', max_length=11, blank=True, null=True)
    SaleDay = models.DecimalField(u'可售天数', max_digits = 18, decimal_places = 2, blank=True, null=True)
    Location = models.CharField(u'发货地址', max_length=18, blank=True, null=True)
    realavailable =  models.IntegerField(u'发货地址', max_length=11, blank=True, null=True)
    SKURefreshTime =  models.DateField(u'商品最近刷新时间', blank=True, null=True)
    isVariations   =  models.CharField(u'是否有变体', max_length=8,blank=True, null=True)
    ShipToLocations = models.CharField(u'配送地', max_length=50,blank=True, null=True)
    TortInfo = models.CharField(u'侵权状态', max_length=10,blank=True, null=True)
    MainSKU  = models.CharField(u'主SKU',max_length=20,blank=True,null=True)
    currency = models.CharField(u'币种', max_length=8, blank=True, null=True)
    profitrate = models.CharField(u'利润率', max_length=20, blank=True, null=True)

    Campaign_id = models.BigIntegerField(u'活动ID', )
    Campaign_name = models.CharField(u'活动名称', max_length=100, blank=True, null=True)
    Campaign_status = models.CharField(u'活动状态', max_length=20, blank=True, null=True)
    Campaign_creater = models.CharField(u'创建人', max_length=20, blank=True, null=True)
    ad_id = models.BigIntegerField(u'广告ID', )
    bidPercentage = models.DecimalField(u'广告费率', max_digits=5, decimal_places=1)

    isnormal =  models.CharField(u'手标状态', choices=getChoices(Choiceisnormal),max_length=20, blank=True, null=True)

    class Meta:
        verbose_name=u'全部商品信息'
        verbose_name_plural=verbose_name
        db_table = 't_online_info_ebay'
        ordering = ['-sold']
    def __unicode__(self):
        return u'id:%s'%(self.id)