#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: v_product_customization_show.py
 @time: 2018/8/10 10:00
"""
from django.db import models
from public import *

class v_product_customization_show(models.Model):
    MainSKU = models.CharField(u'主sku', max_length=16, blank=True, null=True)
    BmpUrl = models.URLField(u'BmpUrl', max_length=16, blank=True, null=True)
    SKU = models.CharField(u'商品SKU', max_length=16, blank=True, null=True)
    GoodsStatus = models.CharField(u'商品状态', max_length=32, blank=True, null=True)
    GoodsName = models.CharField(u'商品名称', max_length=64, blank=True, null=True)
    SalerName = models.CharField(u'业绩归属人1', max_length=32, blank=True, null=True)
    SalerName2 = models.CharField(u'业绩归属人2', max_length=32, blank=True, null=True)
    Purchaser = models.CharField(u'采购员', max_length=32, blank=True, null=True)
    SellCount1 = models.IntegerField(u'7天销量', blank=True, null=True)
    SellCount2 = models.IntegerField(u'15天销量', blank=True, null=True)
    SellCount3 = models.IntegerField(u'30天销量', blank=True, null=True)
    Number = models.IntegerField(u'库存数量', blank=True, null=True)
    UseNumber = models.IntegerField(u'可用数量', blank=True, null=True)
    ReservationNum = models.IntegerField(u'占用数量', blank=True, null=True)
    AverageNumber = models.IntegerField(u'日平均数量', blank=True, null=True)
    CreateDate = models.DateTimeField(u'商品创建时间', blank=True, null=True)
    Weight = models.CharField(u'商品重量', max_length=16, blank=True, null=True)
    Money = models.DecimalField(u'库存金额', max_digits=10, decimal_places=2, blank=True, null=True)
    Price = models.DecimalField(u'平均单价', max_digits=10, decimal_places=2, blank=True, null=True)
    SaleDay = models.DecimalField(u'预计可售天数', max_digits=10, decimal_places=1, blank=True, null=True)
    SupplierName = models.CharField(u'供应商名称', max_length=16, blank=True, null=True)
    OSCode = models.CharField(u'商品采购码', max_length=5, blank=True, null=True)
    storeID = models.IntegerField(u'仓库', choices=getChoices(ChoiceStoreID), blank=True, null=True)
    storeName = models.IntegerField(u'默认发货仓库 ', choices=getChoices(ChoiceStoreID), blank=True, null=True)
    CostPrice = models.DecimalField(u'商品成本单价', max_digits=10, decimal_places=1, blank=True, null=True)
    LinkUrl = models.URLField(u'网址', max_length=16, blank=True, null=True)
    LinkUrl2 = models.URLField(u'网址2', max_length=16, blank=True, null=True)
    LinkUrl3 = models.URLField(u'网址3', max_length=16, blank=True, null=True)
    LinkUrl4 = models.URLField(u'网址4', max_length=16, blank=True, null=True)
    LinkUrl5 = models.URLField(u'网址5', max_length=16, blank=True, null=True)
    LinkUrl6 = models.URLField(u'网址6', max_length=16, blank=True, null=True)
    Model = models.CharField(u'型号', max_length=16, db_index=True, blank=True, null=True)
    KcMaxNum = models.IntegerField(u'库存上限', blank=True, null=True)
    KcMinNum = models.IntegerField(u'库存下限', blank=True, null=True)
    Style = models.CharField(u'款式', max_length=16, db_index=True, blank=True, null=True)
    MinPrice = models.DecimalField(u'最低采购单价', max_digits=10, decimal_places=2, null=True)
    CategoryCode = models.CharField(u'产品类别', max_length=32, db_index=True, blank=True, null=True)
    Used = models.PositiveSmallIntegerField(u'是否停用', blank=True, null=True)
    AllCostPrice = models.DecimalField(u'商品成本金额', max_digits=10, decimal_places=1, blank=True, null=True)
    possessMan1 = models.CharField(u'责任归属人1', max_length=16, blank=True, null=True)
    possessMan2 = models.CharField(u'责任归属人2', max_length=16, blank=True, null=True)
    MoreStyleUrl = models.URLField(u'多款式网址', max_length=16, blank=True, null=True)
    UpdateTime = models.DateTimeField(u'数据更新时间', blank=True, null=True, auto_now=True)
    IsCg = models.CharField(u'建议采购', choices=getChoices(ChoiceIsCg), max_length=4, blank=True, null=True)
    radio = models.DecimalField(u'突变系数', max_digits=10, decimal_places=2, blank=True, null=True)
    NotInStore = models.IntegerField(u'采购未入库', blank=True, null=True)
    hopeUseNum = models.DecimalField(u'预计可用库存', max_digits=10, decimal_places=2, blank=True, null=True)
    UnPaiDNum = models.DecimalField(u'缺货及未派单', max_digits=10, decimal_places=2, blank=True, null=True)
    LocationName = models.CharField(u'库位', max_length=32, blank=True, null=True)
    SuggestNum = models.DecimalField(u'建议采购数量', max_digits=10, decimal_places=2, blank=True, null=True)
    MaxDelayDays = models.IntegerField(u'最长采购缺货天数', blank=True, null=True)
    SaleReNum = models.IntegerField(u'缺货占用数量', blank=True, null=True)
    StockDiff15 = models.DecimalField(u'预计可用库存-15天销量', max_digits=10, decimal_places=2, blank=True, null=True)
    # HandleTime          =   models.DateTimeField(u'处理时间',blank = True,null = True,auto_now=True)
    # HandleResults       =   models.CharField(u'处理状态',choices=getChoices(ChoiceHandleStatus),max_length=16,blank = True,null = True)
    tortinfo = models.CharField(u'侵权站点', max_length=16, blank=True, null=True)
    CgCategory = models.CharField(u'供应链商品类别', choices=getChoices(ChoiceSelectCategory), max_length=32, blank=True,
                                  null=True)
    Remark3 = models.TextField(u'采购意见', max_length=255, blank=True, null=True)
    SourceOSCode = models.CharField(u'采购等级码', max_length=16, blank=True, null=True)
    GoodsID = models.IntegerField(u'GoodsID', blank=True, null=True)
    # Remark2             =   models.TextField(u'',max_length=255,blank = True,null = True)
    # firstWarnningTime   =   models.DateTimeField(u'首次预警',blank = True,null = True,auto_now=True)
    PurchaseNum = models.IntegerField(u'采购数量', blank=True, null=True)
    FromClothes = models.SmallIntegerField(u'是否服装', blank=True, null=True)

    class Meta:
        verbose_name = u'产品定做落地库存查询'
        verbose_name_plural = verbose_name
        db_table = 'v_product_customization_show'
        ordering = ['-SellCount1']

    def __unicode__(self):
        return u'%s'%(self.id)