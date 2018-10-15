# -*- coding: utf-8 -*-
from django.db import models
from skuapp.table.public import getChoices, ChoiceStatus_wish, \
    ChoiceReviewState, ChoiceTortYN, ChoiceOperationState, ChioceWishExpressType

class t_online_info_wish_store(models.Model):
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
    OfSales         = models.PositiveSmallIntegerField(u'总销量', blank=True, null=True)
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

    Order7daysDE     = models.PositiveSmallIntegerField(u'7天order数(德国仓)', blank=True, null=True)
    OfsalesDE        = models.PositiveSmallIntegerField(u'总订单量(德国仓)', blank=True, null=True)
    Order7daysGB     = models.PositiveSmallIntegerField(u'7天order数(英国仓)', blank=True, null=True)
    OfsalesGB        = models.PositiveSmallIntegerField(u'总订单量(英国仓)', blank=True, null=True)
    Order7daysUS     = models.PositiveSmallIntegerField(u'7天order数(美国仓)', blank=True, null=True)
    OfsalesUS        = models.PositiveSmallIntegerField(u'总订单量(美国仓)', blank=True, null=True)

    Order7daysFBW     = models.PositiveSmallIntegerField(u'7天order数(FBW)', blank=True, null=True)
    OfsalesFBW        = models.PositiveSmallIntegerField(u'总订单量(FBW)', blank=True, null=True)
    FBW_Flag          = models.CharField(u'FBW标记',max_length=16, blank=True, null=True)

    class Meta:
        verbose_name = u'Wish 店铺管理'
        verbose_name_plural = verbose_name
        db_table = 't_online_info_wish'

    def __unicode__(self):
        return u'ShopName:%s;id:%s'%(self.ShopName,self.ProductID)

class t_add_variant_information(models.Model):
    ProductID       = models.CharField(u'产品ID', max_length=32, blank=True, null=True)
    Country         = models.CharField(u'国家', max_length=32, blank=True, null=True)
    ParentSKU       = models.CharField(u'父SKU', max_length=32, blank=True, null=True)
    ShopSKU         = models.CharField(u'店铺SKU', max_length=32, blank=True, null=True)
    Param           = models.TextField(u'入参', blank=True, null=True)
    Content         = models.TextField(u'出参', blank=True, null=True)
    Information     = models.TextField(u'详细信息', blank=True, null=True)
    Sresult         = models.CharField(u'结果', max_length=32, blank=True, null=True)
    Shipping_Price  = models.DecimalField(u'调价后运费', max_digits=10, decimal_places=2, blank=True, null=True)
    MaxVariablePrice  = models.DecimalField(u'最高变量价格', max_digits=10, decimal_places=2, blank=True, null=True)
    OldShippingPrice  = models.DecimalField(u'调前运费', max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name=u'Wish 国际运费调整'
        verbose_name_plural=verbose_name
        db_table = 't_add_variant_information'
        ordering = ['-id']

    def __unicode__(self):
        return u'ProductID:%s;Country:%s'%(self.ProductID,self.Country)


class t_wish_product_api_log(models.Model):
    SynName        = models.CharField(u'操作编号', max_length=64, blank=True, null=True)
    StartTime      = models.DateTimeField(u'开始时间', blank=True, null=True)
    EndTime        = models.DateTimeField(u'结束时间', blank=True, null=True)
    Person         = models.CharField(u'操作人', max_length=64, blank=True, null=True)
    Time           = models.DateTimeField(u'操作时间', blank=True, null=True)
    Status         = models.CharField(u'操作执行结果', max_length=64, blank=True, null=True)
    Type           = models.CharField(u'操作类型', max_length=32, blank=True, null=True)
    elogs          = models.TextField(u'执行的错误日志', blank=True, null=True)
    aNum           = models.PositiveSmallIntegerField(u'全部', blank=True, null=True)
    rNum           = models.PositiveSmallIntegerField(u'已成功', blank=True, null=True)
    eNum           = models.PositiveSmallIntegerField(u'已失败', blank=True, null=True)

    class Meta:
        verbose_name=u'Wish店铺管理操作日志'
        verbose_name_plural=verbose_name
        db_table = 't_wish_product_api_log'
        ordering = ['-id']

    def __unicode__(self):
        return u'SynName:%s;Person:%s'%(self.SynName,self.Person)


