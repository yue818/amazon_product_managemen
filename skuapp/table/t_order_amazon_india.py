# -*- coding: utf-8 -*-
from django.db import models
from .public import *

class t_order_amazon_india(models.Model):
    LatestShipDate          = models.CharField(u'最迟物流日期',max_length=64,blank = True,null = True)
    EarliestShipDate        = models.CharField(u'最早物流日期',max_length=64,blank = True,null = True)
    OrderType               = models.CharField(u'订单类型',max_length=64,blank = True,null = True)
    BuyerEmail              = models.CharField(u'买家邮箱',max_length=100,blank = True,null = True)
    IsReplacementOrder      = models.CharField(u'替换订单',max_length=32,blank = True,null = True)
    NumberOfItemsShipped    = models.PositiveSmallIntegerField(u'已物流总数',max_length=12,blank = True,null = True)
    NumberOfItemsUnshipped  = models.PositiveSmallIntegerField(u'未物流总数',max_length=12,blank = True,null = True)
    ShipServiceLevel        = models.CharField(u'物流服务等级',max_length=32,blank = True,null = True)
    IsBusinessOrder         = models.CharField(u'商业订单',max_length=32,blank = True,null = True)
    PaymentMethodDetail     = models.CharField(u'付款方式',max_length=32,blank = True,null = True)
    BuyerName               = models.CharField(u'买家姓名',max_length=64,blank = True,null = True)
    CurrencyCode            = models.CharField(u'货币代码',max_length=32,blank = True,null = True)
    Amount                  = models.DecimalField(u'消费金额',max_digits=11,decimal_places=2,blank = True,null = True)
    IsPremiumOrder          = models.CharField(u'高级订单',max_length=32,blank = True,null = True)
    AmazonOrderId           = models.CharField(u'Amazon订单号',max_length=32,blank = True,null = True)
    PaymentMethod           = models.CharField(u'付款渠道', max_length=32, blank=True, null=True)
    PurchaseDate            = models.CharField(u'付款日期', max_length=32, blank=True, null=True)
    LastUpdateDate          = models.CharField(u'最近更新时间', max_length=32, blank=True, null=True)
    # OrderStatus values:
    # PendingAvailability
    # This status is available for pre - orders only.The order has been placed, payment has not been authorized, and the release date of the item is in the future.The order is not ready for shipment.Note that Preorder is a possible OrderType value in Japan (JP) only.
    # Pending
    # The order has been placed but payment has not been authorized.The order is not ready for shipment.Note that for orders with OrderType = Standard, the initial order status is Pending.For orders with OrderType = Preorder (available in JP only), the initial order status is PendingAvailability, and the order passes into the Pending status when the payment authorization process begins.
    # Unshipped
    # Payment has been authorized and order is ready for shipment, but no items in the order have been shipped.
    # PartiallyShipped
    # One or more(but not all) items in the order have been shipped.
    # Shipped
    # All items in the order have been shipped.
    # InvoiceUnconfirmed
    # All items in the order have been shipped.The seller has not yet given confirmation to Amazon that the invoice has been shipped to the buyer.Note: This value is available only in China(CN).
    # Canceled
    # The order was canceled.
    # Unfulfillable
    # The order cannot be fulfilled.This state applies only to Amazon - fulfilled orders that were not placed on Amazon's retail web site.
    OrderStatus             = models.CharField(u'Amazon订单状态', max_length=32, blank=True, null=True)
    FulfillmentChannel      = models.CharField(u'发货渠道', choices=getChoices(TrackChannel), max_length=32, blank=True, null=True)
    SalesChannel            = models.CharField(u'销售渠道', max_length=32, blank=True, null=True)
    shipStateOrRegion       = models.CharField(u'州/区', max_length=32, blank=True, null=True)
    shipCity                = models.CharField(u'城市', max_length=32, blank=True, null=True)
    shipPostalCode          = models.CharField(u'邮编', max_length=32, blank=True, null=True)
    shipName                = models.CharField(u'收件人姓名', max_length=100, blank=True, null=True)
    shipPhone               = models.CharField(u'收件人电话', max_length=32, blank=True, null=True)
    shipCountryCode         = models.CharField(u'国家代码', max_length=12, blank=True, null=True)
    shipAddressLine1        = models.CharField(u'详细地址1', max_length=120, blank=True, null=True)
    shipAddressLine2        = models.CharField(u'详细地址2', max_length=120, blank=True, null=True)
    IsPrime                 = models.CharField(u'重要物品', max_length=32, blank=True, null=True)
    ShipmentServiceLevelCategory = models.CharField(u'物流类别', max_length=64, blank=True, null=True)
    ShopName                = models.CharField(u'店铺名', max_length=32, blank=True, null=True)
    UpdateTime              = models.DateTimeField(u'Amazon订单同步时间',blank = True,null = True)
    # track_info              = models.TextField(u'物流信息',blank = True,null = True)
    # track_status            = models.CharField(u'物流状态', max_length=64, blank=True, null=True)
    # trackNumber             = models.CharField(u'运单号', max_length=32, blank=True, null=True)
    # track_TDate             = models.CharField(u'取件日期', max_length=64, blank=True, null=True)
    # track_From              = models.CharField(u'出发地', max_length=64, blank=True, null=True)
    # track_Des               = models.CharField(u'目的地', max_length=64, blank=True, null=True)
    # track_StateDesc         = models.CharField(u'状态描述', max_length=64, blank=True, null=True)
    # track_ADate             = models.CharField(u'签收日期', max_length=64, blank=True, null=True)
    # track_Sign              = models.CharField(u'签收人', max_length=64, blank=True, null=True)
    # track_Place             = models.CharField(u'服务地点', max_length=64, blank=True, null=True)
    # track_DateTime          = models.CharField(u'日期时间', max_length=64, blank=True, null=True)
    # track_company           = models.CharField(u'物流公司', max_length=64, blank=True, null=True)
    # track_service           = models.CharField(u'配送服务', max_length=32, blank=True, null=True)
    is_sure_feed            = models.CharField(u'同步至Amazon平台', max_length=32, blank=True, null=True)
    DeclaredValue           = models.DecimalField(u'申报价值',max_digits=8,decimal_places=2,blank = True,null = True)
    DeclareCurrency         = models.CharField(u'申报货币类型', max_length=32, blank=True, null=True)
    EarliestDeliveryDate    = models.CharField(u'最早交付时间', max_length=32, blank=True, null=True)
    LatestDeliveryDate      = models.CharField(u'最迟交付时间', max_length=32, blank=True, null=True)
    applyTracking           = models.CharField(u'正在申请', max_length=32, blank=True, null=True)
    # LableData               = models.CharField(u'物流运单面单URL', max_length=200, blank=True, null=True)dealResultInfo
    dealUser                = models.CharField(u'处理人', max_length=64, blank=True, null=True)
    dealResult              = models.CharField(u'处理结果', max_length=64, blank=True, null=True)
    dealTime                = models.DateTimeField(u'处理时间',blank = True,null = True)
    pyOrderNumber           = models.CharField(u'PY订单号', max_length=64, blank=True, null=True)
    dealAction              = models.CharField(u'操作', max_length=32, blank=True, null=True)
    dealResultInfo          = models.CharField(u'处理结果详情', max_length=64, blank=True, null=True)
    applyTrackNoTime        = models.DateTimeField(u'申请运单号时间', blank=True, null=True)
    OrderWarningDays        = models.PositiveSmallIntegerField(u'预警天数',max_length=11,blank = True,null = True)
    OrderWarningType        = models.CharField(u'预警类型', max_length=32, blank=True, null=True)
    # pdfStatus               = models.CharField(u'面单下载状态', max_length=32, blank=True, null=True)

    class Meta:
        verbose_name=u'Amazon印度站订单物流信息'
        verbose_name_plural=u'Amazon印度站订单物流信息'
        db_table = 't_order_amazon_india'
        ordering = ['LatestShipDate']
    def __unicode__(self):
        return u'%s'%(self.id)