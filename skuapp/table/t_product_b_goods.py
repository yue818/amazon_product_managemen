# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models
from public import *


# 商品信息
class t_product_b_goods(t_base):
    ShopTitle = models.CharField(u'店铺名称', max_length=16, db_index=True, blank=True, null=True)
    BarCode = models.CharField(u'采购渠道', max_length=16, blank=True, null=True)
    FitCode = models.CharField(u'FitCode', max_length=16, db_index=True, blank=True, null=True)
    MultiStyle = models.CharField(u'多款式', max_length=16, db_index=True, blank=True, null=True)
    # Model = models.CharField(u'型号', max_length=16, db_index=True, blank=True, null=True)            #SupplierArtNO
    Style = models.CharField(u'款式', max_length=16, db_index=True, blank=True, null=True)
    Brand = models.CharField(u'品牌', max_length=16, db_index=True, blank=True, null=True)
    LocationID = models.IntegerField(u'LocationID', blank=True, null=True)
    Quantity = models.DecimalField(u'数量(个)', max_digits=10, decimal_places=2, null=True)
    SalePrice = models.DecimalField(u'最低售价($)', max_digits=10, decimal_places=2, null=True)
    # CostPrice = models.DecimalField(u'成本价(RMB)', max_digits=10, decimal_places=2, null=True)        #UnitPrice
    DeclaredValue = models.DecimalField(u'申报价值(美元)', max_digits=10, decimal_places=2, null=True)
    OriginCountry = models.CharField(u'出口国家', max_length=16, blank=True, null=True)
    OriginCountryCode = models.CharField(u'出口国家代码', max_length=16, blank=True, null=True)
    ExpressID = models.IntegerField(u'ExpressID', blank=True, null=True)
    Used = models.PositiveSmallIntegerField(u'Used', blank=True, null=True)
    MaxNum = models.IntegerField(u'库存上限', blank=True, null=True)
    MinNum = models.IntegerField(u'库存下限', blank=True, null=True)
    GoodsCount = models.IntegerField(u'商品数量', blank=True, null=True)
    SampleFlag = models.IntegerField(u'SampleFlag', blank=True, null=True)
    SampleCount = models.IntegerField(u'样品数量', blank=True, null=True)
    SampleMemo = models.CharField(u'SampleMemo', max_length=16, blank=True, null=True)
    GroupFlag = models.IntegerField(u'GroupFlag', blank=True, null=True)
    # SalerName = models.CharField(u'业绩归属人1', max_length=16, blank=True, null=True)    #KFStaffName
    SellCount = models.IntegerField(u'SellCount', blank=True, null=True)
    # SellDays = models.IntegerField(u'库存预警销售周期', blank=True, null=True)            #StockAlarmDays
    PackFee = models.DecimalField(u'包装成本', max_digits=10, decimal_places=2, null=True)
    PackName = models.CharField(u'包装规格', max_length=16, blank=True, null=True)
    GoodsStatus = models.CharField(u'商品状态', max_length=16, null=True)
    # DevDate = models.DateTimeField(u'开发日期', auto_now_add=True, blank=True, null=True)   #KFTime
    # SalerName2 = models.CharField(u'业绩归属人2', max_length=16, blank=True, null=True)   #JZLStaffName
    BatchPrice = models.DecimalField(u'批发价格', max_digits=10, decimal_places=2, null=True)
    MaxSalePrice = models.DecimalField(u'最高售价', max_digits=10, decimal_places=2, null=True)
    RetailPrice = models.DecimalField(u'零售价格', max_digits=10, decimal_places=2, null=True)
    MarketPrice = models.DecimalField(u'市场参考价', max_digits=10, decimal_places=2, null=True)
    PackageCount = models.IntegerField(u'最小包装数', blank=True, null=True)
    # ChangeStatusTime = models.DateTimeField(u'ChangeStatusTime', auto_now=True, blank=True, null=True)       #UpdateTime
    LinkUrl = models.URLField(u'LinkUrl', null=True)
    LinkUrl2 = models.URLField(u'LinkUrl2', null=True)
    LinkUrl3 = models.URLField(u'LinkUrl3', null=True)
    MinPrice = models.DecimalField(u'最低采购单价', max_digits=10, decimal_places=2, null=True)
    HSCODE = models.CharField(u'海关编码', max_length=16, blank=True, null=True)
    ViewUser = models.CharField(u'ViewUser', max_length=16, blank=True, null=True)
    InLong = models.DecimalField(u'内盒长(cm)', max_digits=10, decimal_places=2, null=True)
    InWide = models.DecimalField(u'内盒宽(cm)', max_digits=10, decimal_places=2, null=True)
    InHigh = models.DecimalField(u'内盒高(cm)', max_digits=10, decimal_places=2, null=True)
    InGrossweight = models.DecimalField(u'内盒毛重', max_digits=10, decimal_places=2, null=True)
    InNetweight = models.DecimalField(u'内盒净重', max_digits=10, decimal_places=2, null=True)
    OutLong = models.DecimalField(u'外箱长(cm)', max_digits=10, decimal_places=2, null=True)
    OutWide = models.DecimalField(u'外箱宽(cm)', max_digits=10, decimal_places=2, null=True)
    OutHigh = models.DecimalField(u'外箱高(cm)', max_digits=10, decimal_places=2, null=True)
    OutGrossweight = models.DecimalField(u'外箱毛重', max_digits=10, decimal_places=2, null=True)
    OutNetweight = models.DecimalField(u'外箱净重', max_digits=10, decimal_places=2, null=True)
    ShopCarryCost = models.DecimalField(u'店辅运费', max_digits=10, decimal_places=2, null=True)
    ExchangeRate = models.DecimalField(u'汇率', max_digits=10, decimal_places=2, null=True)
    WebCost = models.DecimalField(u'WebCost', max_digits=10, decimal_places=2, null=True)
    PackWeight = models.DecimalField(u'包装重量', max_digits=10, decimal_places=2, null=True)
    LogisticsCost = models.DecimalField(u'物流成本', max_digits=10, decimal_places=2, null=True)
    GrossRate = models.DecimalField(u'交叉汇率', max_digits=10, decimal_places=2, null=True)
    CalSalePrice = models.DecimalField(u'售价', max_digits=10, decimal_places=2, null=True)
    CalYunFei = models.DecimalField(u'运费', max_digits=10, decimal_places=2, null=True)
    CalSaleAllPrice = models.DecimalField(u'销售总价', max_digits=10, decimal_places=2, null=True)
    PackMsg = models.CharField(u'PackMsg', max_length=16, db_index=True, blank=True, null=True)
    ItemUrl = models.URLField(u'商品URL', null=True)
    DelInFile = models.CharField(u'DelInFile', max_length=16, db_index=True, blank=True, null=True)
    Season = models.CharField(u'季节', choices=getChoices(ChoiceSeason), max_length=16, null=True)
    possessMan1 = models.CharField(u'责任归属人1', max_length=16, blank=True, null=True)
    LinkUrl4 = models.URLField(u'LinkUrl4', null=True)
    LinkUrl5 = models.URLField(u'LinkUrl5', null=True)
    LinkUrl6 = models.URLField(u'LinkUrl6', null=True)
    NoSalesDate = models.CharField(u'NoSalesDate', choices=getChoices(ChoiceIF), max_length=16, null=True)

    class Meta:
        verbose_name = u'商品信息'
        verbose_name_plural = verbose_name
        db_table = 't_product_b_goods'
        ordering = ['-id']

    def __unicode__(self):
        return u'id:%s MainSKU:%s' % (self.id, self.MainSKU)
