# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 王芝杨
 @site: 
 @software: PyCharm
 @file: t_stocking_demand_fbw.py
 @time: 2018-08-16

"""
from django.db import models
from .public import *


class t_stocking_demand_fbw(models.Model):
    Stocking_plan_number  = models.CharField(u'发货计划号', max_length=32, blank=True, null=True)
    Stock_plan_date       = models.DateTimeField(u'发货生成时间', blank=True, null=True)
    ProductImage = models.CharField(u'商品图片', max_length=200, blank=True, null=True)
    Destination_warehouse = models.CharField(u'目的地仓库', choices=getChoices(ChoiceWarehouse), max_length=63)
    AccountNum = models.CharField(u'账号', max_length=32)
    ProductID = models.CharField(u'ProductID', max_length=32)
    ProductSKU = models.CharField(u'商品SKU', max_length=32)
    ShopSKU = models.CharField(u'店铺SKU', max_length=128, blank=True, null=True)
    servenOrder = models.IntegerField(u'7天销量', max_length=10, blank=True, null=True)
    Stocking_quantity = models.IntegerField(u'发货数量', max_length=10, blank=True, null=True)
    QTY = models.IntegerField(u'实际发货数量', max_length=10, blank=True, null=True)
    ProductPrice = models.DecimalField(u'商品价格', max_digits=10, decimal_places=2, blank=True, null=True)
    ProductWeight = models.DecimalField(u'商品克重', max_digits=10, decimal_places=2, blank=True, null=True)
    DemandMoney = models.DecimalField(u'备货货值', max_digits=10, decimal_places=2, blank=True, null=True)
    DeliverMoney = models.DecimalField(u'发货货值', max_digits=10, decimal_places=2, blank=True, null=True)
    Remarks = models.TextField(u'备注', blank=True, null=True)
    Demand_people         = models.CharField(u'发货需求人', max_length=32, blank=True, null=True)
    FBW_US = models.CharField(u'FBW_US', choices=getChoices(ChoiceFBWPlanFBWUS),max_length=32) #有、无
    canSellCount = models.IntegerField(u'可卖数量', max_length=10, blank=True, null=True)
    Product_nature = models.CharField(u'产品性质', choices=getChoices(ChoiceProductnature), max_length=32)
    ProductName           = models.CharField(u'商品名称', max_length=64, blank=True, null=True)
    position = models.CharField(u'仓位', max_length=32, blank=True, null=True)
    packFormat = models.CharField(u'包装规格', max_length=128, blank=True, null=True)
    ListNumber = models.CharField(u'批次号', max_length=64, blank=True, null=True)
    importFileMan = models.CharField(u'导出文件人', max_length=32, blank=True, null=True)
    importFileTime = models.DateTimeField(u'导出文件时间', blank=True, null=True)
    genBatchMan = models.CharField(u'生成批次人', max_length=32, blank=True, null=True)
    genBatchTime = models.DateTimeField(u'生成批次时间', blank=True, null=True)
    addRecordMan = models.CharField(u'增加清单人', max_length=32, blank=True, null=True)
    addRecordTime = models.DateTimeField(u'增加清单时间', blank=True, null=True)
    deliverMan = models.CharField(u'发货人', max_length=32, blank=True, null=True)
    deliverTime = models.DateTimeField(u'发货时间', blank=True, null=True)
    genDemandMan = models.CharField(u'生成发货需求人', max_length=32, blank=True, null=True)
    genDemandTime = models.DateTimeField(u'生成发货需求时间', blank=True, null=True)
    OplogTime = models.DateTimeField(u'记录生成时间', blank=True, null=True)
    Status = models.CharField(u'状态', choices=getChoices(ChoiceFBWPlanStatus),max_length=32)
    deliver_way = models.CharField(u'发货方式', choices=getChoices(ChoiceFBWPlanDELIVER), max_length=32)
    newold = models.CharField(u'新老品', choices=getChoices(ChoiceFBWPlanNEWOLD), max_length=32)
    transdeliver = models.CharField(u'已完成采购->转发货人', max_length=32, blank=True, null=True)
    transTime = models.DateTimeField(u'已完成采购->转发货时间', blank=True, null=True)
    againgenBatchMan = models.CharField(u'重新生成批次人', max_length=32, blank=True, null=True)
    againgenBatchTime = models.DateTimeField(u'冲洗生成批次时间', blank=True, null=True)
    LogisticsNumber = models.CharField(u'物流单号', max_length=255, blank=True, null=True)
    class Meta:
        verbose_name = u'FBW发货列表'
        verbose_name_plural = verbose_name
        db_table = 't_stocking_demand_fbw'

    def __unicode__(self):
        return u'%s' % (self.id)