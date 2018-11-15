# -*- coding: utf-8 -*-
from django.db import models
from public import *


class t_online_info_wish(models.Model):
    PlatformName    = models.CharField(u'平台名称', max_length=16, blank=True, null=True)
    ProductID       = models.CharField(u'产品ID', max_length=32, blank=True, null=True)
    ShopIP          = models.CharField(u'店铺IP', max_length=32, blank=True, null=True)
    ShopName        = models.CharField(u'店铺名称', max_length=32, blank=True, null=True)
    Title           = models.TextField(u'标题', blank=True, null=True)
    SKU             = models.CharField(u'子SKU', max_length=32, blank=True, null=True)
    ShopSKU         = models.CharField(u'店铺SKU', max_length=128, blank=True, null=True)
    Price           = models.CharField(u'价格', max_length=32, blank=True, null=True)
    Quantity        = models.PositiveSmallIntegerField(u'库存量', blank=True, null=True)
    Orders7Days     = models.PositiveSmallIntegerField(u'7天order数', blank=True, null=True)
    SoldYesterday   = models.PositiveSmallIntegerField(u'昨日售出量', blank=True, null=True)
    SoldTheDay      = models.PositiveSmallIntegerField(u'当日售出量', blank=True, null=True)
    SoldXXX         = models.PositiveSmallIntegerField(u'销售差值', blank=True, null=True)
    DateOfOrder     = models.CharField(u'出单日期 ', max_length=32, blank=True, null=True)
    Remarks         = models.TextField(u'操作备注', blank=True, null=True)
    RefreshTime     = models.DateTimeField(u'刷新时间', blank=True, null=True)
    Image           = models.CharField(u'图片', max_length=200, blank=True, null=True)
    Status          = models.CharField(u'状态', choices=getChoices(ChoiceStatus_wish), max_length=16, blank=True, null=True)
    ReviewState     = models.CharField(u'Wish查看状态', choices=getChoices(ChoiceReviewState), max_length=16, blank=True,null=True)
    BeforeReviewState = models.CharField(u'拒绝前状态', choices=getChoices(ChoiceReviewState), max_length=16, blank=True,null=True)
    DateUploaded    = models.DateTimeField(u'上架日期/UTC', blank=True, null=True)
    LastUpdated     = models.DateTimeField(u'最近更新日期/UTC', blank=True, null=True)
    OfSales         = models.CharField(u'总销量', max_length=10, blank=True, null=True)
    ParentSKU       = models.CharField(u'父SKU', max_length=32, blank=True, null=True)
    Seller          = models.CharField(u'店长/销售员', max_length=32, blank=True, null=True)
    TortInfo        = models.CharField(u'侵权状态', choices=getChoices(ChoiceTortYN), max_length=16, blank=True, null=True)
    MainSKU         = models.CharField(u'MainSKU', max_length=32, blank=True, null=True)
    DataSources     = models.CharField(u'数据来源', max_length=15, blank=True, null=True)
    OperationState  = models.CharField(u'下架状态', choices=getChoices(ChoiceOperationState), max_length=15, blank=True,null=True)
    Published       = models.CharField(u'刊登人', max_length=32, blank=True, null=True)
    is_promoted     = models.CharField(u'是否加钻', max_length=32, blank=True, null=True)
    WishExpress     = models.CharField(u'海外仓标记', max_length=64, blank=True, null=True)
    AdStatus        = models.CharField(u'Listing刷新状态', max_length=64, blank=True, null=True)  # 原为广告状态标记
    market_time     = models.DateTimeField(u'营销时间', blank=True, null=True)
    GoodsFlag       = models.PositiveSmallIntegerField(u'商品SKU状态', blank=True, null=True)
    ShopsFlag       = models.PositiveSmallIntegerField(u'店铺SKU状态', blank=True, null=True)
    BindingFlag     = models.PositiveSmallIntegerField(u'绑定状态标记', blank=True, null=True)
    SName           = models.CharField(u'店铺状态', max_length=64, blank=True, null=True)  #
    WishExpressType = models.CharField(u'海外仓类型', choices=getChoices(ChioceWishExpressType),
                                       max_length=32, blank=True, null=True)  # 海外仓类型
    MainSKULargeCate = models.CharField(u'大类名称',max_length=32, blank=True, null=True)
    MainSKUSmallCate = models.CharField(u'小类名称',max_length=32, blank=True, null=True)

    ADShow           = models.PositiveSmallIntegerField(u'是否有广告', blank=True, null=True)
    SalesTrend       = models.PositiveSmallIntegerField(u'周销售情况', blank=True, null=True)
    Rating           = models.PositiveSmallIntegerField(u'评分', blank=True, null=True)

    class Meta:
        verbose_name=u'Wish 只读'
        verbose_name_plural=verbose_name
        db_table = 't_online_info_wish'
        # ordering = ['-Orders7Days']
    def __unicode__(self):
        return u'id:%s'%(self.id)