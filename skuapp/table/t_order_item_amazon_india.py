# -*- coding: utf-8 -*-
from django.db import models
from public import *

ChoicesIsornot= (
        (u'is', u'是'),
        (u'isnot', u'否'),
               )

class t_order_item_amazon_india(models.Model):
    AmazonOrderId           = models.CharField(u'Amazon订单号', max_length=32, blank=True, null=True)
    ASIN                    = models.CharField(u'asin', max_length=32, blank=True, null=True)
    OrderItemId             = models.CharField(u'Amazon订单详情号', max_length=32, blank=True, null=True)
    SellerSKU               = models.CharField(u'SKU', max_length=64, blank=True, null=True)
    BuyerCustomizedInfo     = models.CharField(u'买家详情', max_length=100, blank=True, null=True)
    Title                   = models.CharField(u'标题', max_length=200, blank=True, null=True)
    QuantityOrdered         = models.PositiveSmallIntegerField(u'商品总数',max_length=8,blank = True,null = True)
    QuantityShipped         = models.PositiveSmallIntegerField(u'已物流总数',max_length=8,blank = True,null = True)
    PointsNumber            = models.CharField(u'授权地点', max_length=64, blank=True, null=True)
    ItemPrice               = models.DecimalField(u'商品价格',max_digits=10,decimal_places=2,blank=True,null=True)
    ShippingPrice           = models.DecimalField(u'物流价格',max_digits=10,decimal_places=2,blank=True,null=True)
    GiftWrapPrice           = models.DecimalField(u'包装价格',max_digits=10,decimal_places=2,blank=True,null=True)
    ItemTax                 = models.DecimalField(u'商品税',max_digits=10,decimal_places=2,blank=True,null=True)
    ShippingTax             = models.DecimalField(u'物流税',max_digits=10,decimal_places=2,blank=True,null=True)
    GiftWrapTax             = models.DecimalField(u'包装税',max_digits=10,decimal_places=2,blank=True,null=True)
    ShippingDiscount        = models.DecimalField(u'物流折扣',max_digits=10,decimal_places=2,blank=True,null=True)
    PromotionDiscount       = models.DecimalField(u'促销折扣',max_digits=10,decimal_places=2,blank=True,null=True)
    PromotionIds            = models.CharField(u'促销商品Id', max_length=100, blank=True, null=True)
    CODFee                  = models.DecimalField(u'COD费用',max_digits=10,decimal_places=2,blank=True,null=True)
    CODFeeDiscount          = models.DecimalField(u'COD费用折扣',max_digits=10,decimal_places=2,blank=True,null=True)
    GiftMessageText         = models.CharField(u'备注消息', max_length=200, blank=True, null=True)
    GiftWrapLevel           = models.CharField(u'包装等级', max_length=64, blank=True, null=True)
    ConditionNote           = models.CharField(u'注意事项', max_length=64, blank=True, null=True)
    ConditionId             = models.CharField(u'注意事项Id', max_length=32, blank=True, null=True)
    ConditionSubtypeId      = models.CharField(u'注意子事项Id', max_length=64, blank=True, null=True)
    ScheduledDeliveryStartDate  = models.CharField(u'计划交付开始时间', max_length=32, blank=True, null=True)
    ScheduledDeliveryEndDate    = models.CharField(u'计划交付结束时间', max_length=32, blank=True, null=True)
    PriceDesignation            = models.CharField(u'指定价格', max_length=64, blank=True, null=True)
    UpdateTime                  = models.DateTimeField(u'同步时间', blank=True, null=True)
    CurrencyCode                = models.CharField(u'货币代码', max_length=32, blank=True, null=True)
    PointsAmount                = models.DecimalField(u'授权价格',max_digits=10,decimal_places=2,blank=True,null=True)
    InvoiceRequirement          = models.CharField(u'发票要求', max_length=64, blank=True, null=True)
    BuyerSelectedInvoiceCategory    = models.CharField(u'发票类别', max_length=64, blank=True, null=True)
    InvoiceTitle                    = models.CharField(u'发票标题', max_length=100, blank=True, null=True)
    InvoiceInformation              = models.CharField(u'发票信息', max_length=64, blank=True, null=True)

    AliasCnName                     =   models.CharField(u'报关中文名',max_length=64,blank = True,null = True)
    AliasEnName                     =   models.CharField(u'报关英文名',max_length=64,blank = True,null = True)
    Unit                            = models.CharField(u'单位', choices=getChoices(ChoiceUnit), max_length=4, null=True)
    SKU                             = models.CharField(u'SKU', max_length=16, db_index=True, blank=True, null=True)
    PackWeight                      = models.DecimalField(u'包装重量', max_digits=10, decimal_places=2, null=True)
    OutLong                         = models.DecimalField(u'外箱长(cm)', max_digits=10, decimal_places=2, null=True)
    OutWide                         = models.DecimalField(u'外箱宽(cm)', max_digits=10, decimal_places=2, null=True)
    OutHigh                         = models.DecimalField(u'外箱高(cm)', max_digits=10, decimal_places=2, null=True)
    IsCharged                       = models.CharField(u'是否带电', choices=ChoicesIsornot, max_length=16, null=True)
    CostPrice                       = models.DecimalField(u'成本价(RMB)', max_digits=10, decimal_places=2, null=True)
    Weight                          = models.DecimalField(u'重量(克)', max_digits=10, decimal_places=2, null=True)
    IsPowder                        = models.CharField(u'是否粉末', choices=ChoicesIsornot, max_length=16, null=True)
    IsLiquid                        = models.CharField(u'是否液体', choices=ChoicesIsornot, max_length=16, null=True)
    isMagnetism                     = models.CharField(u'是否带磁', choices=ChoicesIsornot, max_length=16, null=True)
    ShopSKU                         = models.CharField(u'ShopSKU', max_length=32, blank=True, null=True)

    class Meta:
        verbose_name=u'Amazon印度站订单详情信息'
        verbose_name_plural=u'Amazon印度站订单详情信息'
        db_table = 't_order_item_amazon_india'
    def __unicode__(self):
        return u'%s'%(self.id)