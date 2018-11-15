# encoding: utf-8
"""
@author: ZhangYu
@contact: 292724306@qq.com
@site: 
@software: PyCharm
@file: t_product_b_goods_all_productsku.py
@time: 2017-12-23 10:56
"""
from django.db import models
from b_goods import b_goods
from public import *

class t_product_b_goods_all_productsku(models.Model):
    MainSKU = models.CharField(u'主SKU', max_length=32, db_index=True, blank=True, null=True)
    NID = models.IntegerField(u'NID', blank=True, primary_key=True)
    GoodsCategoryID = models.IntegerField(u'分类id', blank=True, null=True)
    CategoryCode = models.CharField(u'分类code', max_length=50, blank=True, null=True)
    GoodsCode = models.CharField(u'商品编码', max_length=16, db_index=True, blank=True, null=True)
    GoodsName = models.CharField(u'商品名称', max_length=16, db_index=True, blank=True, null=True)
    ShopTitle = models.CharField(u'店铺名称', max_length=16, db_index=True, blank=True, null=True)
    SKU = models.CharField(u'SKU', max_length=16, db_index=True, blank=True, null=True)
    BarCode = models.CharField(u'采购渠道', max_length=16, blank=True, null=True)
    FitCode = models.CharField(u'FitCode', max_length=16, db_index=True, blank=True, null=True)
    MultiStyle = models.CharField(u'多款式', max_length=16, db_index=True, blank=True, null=True)
    Material = models.CharField(u'材质', max_length=16, db_index=True, blank=True, null=True)
    Class = models.CharField(u'规格', max_length=16, db_index=True, blank=True, null=True)
    Model = models.CharField(u'型号', max_length=16, db_index=True, blank=True, null=True)
    Unit = models.CharField(u'单位', choices=getChoices(ChoiceUnit), max_length=4, null=True)
    Style = models.CharField(u'款式', max_length=16, db_index=True, blank=True, null=True)
    Brand = models.CharField(u'品牌', max_length=16, db_index=True, blank=True, null=True)
    LocationID = models.IntegerField(u'LocationID', blank=True, null=True)
    Quantity = models.DecimalField(u'数量(个)', max_digits=10, decimal_places=2, null=True)
    SalePrice = models.DecimalField(u'最低售价($)', max_digits=10, decimal_places=2, null=True)
    CostPrice = models.DecimalField(u'成本价(RMB)', max_digits=10, decimal_places=2, null=True)
    AliasCnName = models.CharField(u'报关中文名', max_length=16, blank=True, null=True)
    AliasEnName = models.CharField(u'报关英文名', max_length=16, blank=True, null=True)
    Weight = models.DecimalField(u'重量(克)', max_digits=10, decimal_places=2, null=True)
    DeclaredValue = models.DecimalField(u'申报价值(美元)', max_digits=10, decimal_places=2, null=True)
    OriginCountry = models.CharField(u'出口国家', max_length=16, blank=True, null=True)
    OriginCountryCode = models.CharField(u'出口国家代码', max_length=16, blank=True, null=True)
    ExpressID = models.IntegerField(u'ExpressID', blank=True, null=True)
    Used = models.PositiveSmallIntegerField(u'Used', blank=True, null=True)
    BmpFileName = models.CharField(u'图片文件名称', max_length=16, blank=True, null=True)
    BmpUrl = models.URLField(u'图片路径', null=True)
    MaxNum = models.IntegerField(u'库存上限', blank=True, null=True)
    MinNum = models.IntegerField(u'库存下限', blank=True, null=True)
    GoodsCount = models.IntegerField(u'商品数量', blank=True, null=True)
    SupplierID = models.IntegerField(u'供应商ID', blank=True, null=True)
    Notes = models.TextField(u'备注', blank=True, null=True)
    SampleFlag = models.IntegerField(u'SampleFlag', blank=True, null=True)
    SampleCount = models.IntegerField(u'样品数量', blank=True, null=True)
    SampleMemo = models.CharField(u'SampleMemo', max_length=16, blank=True, null=True)
    CreateDate = models.DateTimeField(u'创建时间', auto_now_add=True, blank=True, null=True)
    GroupFlag = models.IntegerField(u'GroupFlag', blank=True, null=True)
    SalerName = models.CharField(u'业绩归属人1', max_length=16, blank=True, null=True)
    SellCount = models.IntegerField(u'SellCount', blank=True, null=True)
    SellDays = models.IntegerField(u'库存预警销售周期', blank=True, null=True)
    PackFee = models.DecimalField(u'包装成本', max_digits=10, decimal_places=2, null=True)
    PackName = models.CharField(u'包装规格', max_length=16, blank=True, null=True)
    GoodsStatus = models.CharField(u'商品状态', choices=getChoices(ChoiceGoodsStatus), max_length=16, null=True)
    DevDate = models.DateTimeField(u'开发日期', auto_now_add=True, blank=True, null=True)
    SalerName2 = models.CharField(u'业绩归属人2', max_length=16, blank=True, null=True)
    BatchPrice = models.DecimalField(u'批发价格', max_digits=10, decimal_places=2, null=True)
    MaxSalePrice = models.DecimalField(u'最高售价', max_digits=10, decimal_places=2, null=True)
    RetailPrice = models.DecimalField(u'零售价格', max_digits=10, decimal_places=2, null=True)
    MarketPrice = models.DecimalField(u'市场参考价', max_digits=10, decimal_places=2, null=True)
    PackageCount = models.IntegerField(u'最小包装数', blank=True, null=True)
    ChangeStatusTime = models.DateTimeField(u'ChangeStatusTime', auto_now=True, blank=True, null=True)
    StockDays = models.IntegerField(u'采购到货天数', blank=True, null=True)
    StoreID = models.IntegerField(u'仓库id', blank=True, null=True)
    Purchaser = models.CharField(u'采购员', max_length=16, blank=True, null=True)
    LinkUrl = models.URLField(u'LinkUrl', null=True)
    LinkUrl2 = models.URLField(u'LinkUrl2', null=True)
    LinkUrl3 = models.URLField(u'LinkUrl3', null=True)
    StockMinAmount = models.IntegerField(u'采购最小订货量', blank=True, null=True)
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
    # 二级分类
    IsCharged = models.CharField(u'是否带电', choices=getChoices(ChoiceIF), max_length=16, null=True)
    DelInFile = models.CharField(u'DelInFile', max_length=16, db_index=True, blank=True, null=True)
    Season = models.CharField(u'季节', choices=getChoices(ChoiceSeason), max_length=16, null=True)
    IsPowder = models.CharField(u'是否粉末', choices=getChoices(ChoiceIF), max_length=16, null=True)
    IsLiquid = models.CharField(u'是否液体', choices=getChoices(ChoiceIF), max_length=16, null=True)

    possessMan1 = models.CharField(u'责任归属人1', max_length=16, blank=True, null=True)
    possessMan2 = models.CharField(u'责任归属人2', max_length=16, blank=True, null=True)
    LinkUrl4 = models.URLField(u'LinkUrl4', null=True)
    LinkUrl5 = models.URLField(u'LinkUrl5', null=True)
    LinkUrl6 = models.URLField(u'LinkUrl6', null=True)
    # 二级分类
    isMagnetism = models.CharField(u'是否带磁', choices=getChoices(ChoiceIF), max_length=16, null=True)
    NoSalesDate = models.CharField(u'NoSalesDate', choices=getChoices(ChoiceIF), max_length=16, null=True)

    class Meta:
        verbose_name = u'普源商品信息'
        verbose_name_plural = verbose_name
        db_table = 't_product_b_goods_all_productsku'


    def __unicode__(self):
        return u'%s %s %s ' % (self.NID, self.SKU, self.GoodsName)
