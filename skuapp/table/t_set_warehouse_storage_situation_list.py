# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_set_warehouse_storage_situation_list.py
 @time: 2017-12-19 16:12

"""
from django.db import models
from .public import *

class t_set_warehouse_storage_situation_list(models.Model):
    Stocking_plan_number                = models.CharField(u'备货计划号', max_length=32, blank=True, null=True)
    Delivery_lot_number                 = models.CharField(u'发货批次号', max_length=32, blank=True, null=True)
    Product_nature                      = models.CharField(u'产品性质', choices=getChoices(ChoiceProductnature), max_length=32, blank=True,null=True)
    Purchase_Order_No                   = models.CharField(u'采购单号', max_length=32, blank=True, null=True)
    Destination_warehouse               = models.CharField(u'目的地仓库',choices=getChoices(ChoiceWarehouse), max_length=63, blank=True, null=True)
    ProductSKU                          = models.CharField(u'商品SKU', max_length=32, blank=True, null=True)
    ShopSKU                             = models.CharField(u'店铺SKU', max_length=32, blank=True, null=True)
    ProductName                         = models.CharField(u'商品名称', max_length=100, blank=True, null=True)
    ProductImage                        = models.CharField(u'商品图片', max_length=200, blank=True, null=True)
    Stock_plan_unfinished_quantity      = models.IntegerField(u'备货计划未完成数量', max_length=10, blank=True, null=True)
    The_arrival_of_the_number           = models.IntegerField(u'本次到货数量', max_length=10, blank=True, null=True)
    QTY                                 = models.IntegerField(u'采购数量', max_length=10, blank=True, null=True)
    Stocking_quantity                   = models.IntegerField(u'计划采购数量', max_length=10, blank=True, null=True)
    Price                               = models.DecimalField(u'成本价',max_digits=10,decimal_places=2,blank = True,null = True)
    Weight                              = models.DecimalField(u'克重',max_digits=10,decimal_places=2,blank = True,null = True)
    Arrival_date                        = models.DateTimeField(u'到货日期', blank=True, null=True)
    Arrival_status                      = models.CharField(u'到货状态',choices=getChoices(ChoiceArrivalStatus), max_length=64, blank=True, null=True)
    Delivery_status                     = models.CharField(u'批次状态',choices=getChoices(ChoiceDeliveryStatus), max_length=64, blank=True, null=True)
    Remarks                             = models.TextField(u'备注', blank=True, null=True)
    Storage_status                      = models.CharField(u'入库状态', choices=getChoices(ChoiceStorageStatus), max_length=64, blank=True,null=True)
    StorageDate                         = models.DateTimeField(u'入库日期', blank=True, null=True)
    UpdateTime                          = models.DateTimeField(u'更新时间',auto_now=True,blank = True,null = True)
    LogisticsNumber                     = models.CharField(u'物流单号', max_length=128, blank=True, null=True)
    level                               = models.CharField(u'紧急程度', choices=getChoices(ChoiceLevel), max_length=16, blank=True, null=True)
    Demand_people                       = models.CharField(u'计划需求人', max_length=32, blank=True, null=True)
    Site                                = models.CharField(u'站点', max_length=16, blank=True, null=True)
    AccountNum                          = models.CharField(u'账号', max_length=32, blank=True, null=True)
    OplogTime                           = models.DateTimeField(u'记录生成时间',blank=True,null=True)
    checkMan                            = models.CharField(u'质检人', max_length=32, blank=True, null=True)
    checkTime                           = models.DateTimeField(u'质检时间', blank=True, null=True)
    checkStatus                         = models.CharField(u'质检状态', max_length=64, blank=True,null=True)
    checkRemark                         = models.TextField(u'质检备注', blank=True, null=True)
    genBatchMan                         = models.CharField(u'质检人', max_length=32, blank=True, null=True)
    genBatchTime                        = models.DateTimeField(u'质检时间', blank=True, null=True)

    class Meta:
        verbose_name = u'集货仓入库情况一览'
        verbose_name_plural = verbose_name
        db_table = 't_set_warehouse_storage_situation_list'

    def __unicode__(self):
        return u'%s' % (self.id)
