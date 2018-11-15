# -*- coding: utf-8 -*-
"""
 @desc:
 @author: wangzhiyang
 @site:
 @software: PyCharm
 @file: t_saler_profit_reportform.py
 @time: 2018/8/29 8:53
"""
from django.db import models

class t_saler_profit_reportform(models.Model):
    id = models.AutoField(u'业务流水号', primary_key=True)
    SalerName = models.CharField(u'业绩归属人', max_length=256, blank=True, null=True)
    StatisticsMonth = models.CharField(u'统计月份', max_length=20, blank=True, null=True)
    ShopSKU = models.CharField(u'店铺SKU', max_length=128, blank=True, null=True)
    ProductSKU = models.CharField(u'商品SKU', max_length=64, blank=True, null=True)
    StockAveragePrice = models.DecimalField(u'库存平均价', max_digits=10, decimal_places=4, blank=True, null=True)
    GoodsCode = models.CharField(u'商品编码', max_length=64, blank=True, null=True)
    ProductName = models.CharField(u'商品名称', max_length=255, blank=True, null=True)
    Model = models.CharField(u'型号', max_length=128, blank=True, null=True)
    Specifications = models.CharField(u'规格', max_length=128, blank=True, null=True)
    Style1 = models.CharField(u'款式1', max_length=64, blank=True, null=True)
    Style2 = models.CharField(u'款式2', max_length=64, blank=True, null=True)
    Category = models.CharField(u'商品类别', max_length=64, blank=True, null=True)
    Supplier = models.CharField(u'供应商', max_length=255, blank=True, null=True)
    SalerName1 = models.CharField(u'业绩归属人1', max_length=32, blank=True, null=True)
    SalerName2 = models.CharField(u'业绩归属人2', max_length=32, blank=True, null=True)
    Purchaser = models.CharField(u'采购员', max_length=32, blank=True, null=True)
    CreateDate = models.DateField(u'商品创建时间', blank=True, null=True)

    SaleNum = models.PositiveSmallIntegerField(u'销售数量', max_length=11,blank=True, null=True)
    SaleVolume = models.DecimalField(u'销售额', max_digits=10, decimal_places=4, blank=True, null=True)
    BuyerPayFreight = models.DecimalField(u'买家付运费', max_digits=10, decimal_places=4, blank=True, null=True)
    SaleCost = models.DecimalField(u'销售成本', max_digits=10, decimal_places=4, blank=True, null=True)
    Profit = models.DecimalField(u'实收利润', max_digits=10, decimal_places=4, blank=True, null=True)
    EbayTransFee = models.DecimalField(u'ebay成交费', max_digits=10, decimal_places=4, blank=True, null=True)
    PPCharge = models.DecimalField(u'PP手续费', max_digits=10, decimal_places=4, blank=True, null=True)
    ActualAmount = models.DecimalField(u'实得金额', max_digits=10, decimal_places=4, blank=True, null=True)
    FreightCost = models.DecimalField(u'运费成本', max_digits=10, decimal_places=4, blank=True, null=True)
    PackCost = models.DecimalField(u'包装成本', max_digits=10, decimal_places=4, blank=True, null=True)
    RefundAmount = models.DecimalField(u'退款金额', max_digits=10, decimal_places=4, blank=True, null=True)
    Salers = models.CharField(u'销售员', max_length=32, blank=True, null=True)
    effdate = models.DateTimeField(u'生效时间', blank=True, null=True)
    expdate = models.DateTimeField(u'失效时间', blank=True, null=True)
    platform = models.CharField(u'平台', max_length=32, blank=True, null=True)
    allShopName = models.TextField(u'店铺名称', blank=True, null=True)

    class Meta:
        verbose_name=u'月业绩销售明细表'
        verbose_name_plural=verbose_name
        db_table = 't_saler_profit_reportform'
        ordering =  ['-id']
    def __unicode__(self):
        return u'id:%s'%(self.id)