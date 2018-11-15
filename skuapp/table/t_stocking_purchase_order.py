# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_stocking_purchase_order.py
 @time: 2017-12-19 15:00

"""   
from django.db import models
from .public import *


class t_stocking_purchase_order(models.Model):
    Stocking_plan_number  = models.CharField(u'备货计划号', max_length=32, blank=True, null=True)
    Stock_plan_date       = models.DateTimeField(u'备货计划时间', blank=True, null=True)
    Single_number         = models.CharField(u'采购订单号/调拨单号', max_length=32, blank=True, null=True)
    ProductSKU            = models.CharField(u'商品SKU', max_length=32, blank=True, null=True)
    ShopSKU               = models.CharField(u'店铺SKU', max_length=32, blank=True, null=True)
    Product_nature        = models.CharField(u'产品性质', choices=getChoices(ChoiceProductnature), max_length=32, blank=True,null=True)
    ProductName           = models.CharField(u'商品名称', max_length=100, blank=True, null=True)
    ProductImage          = models.CharField(u'商品图片', max_length=200, blank=True, null=True)
    Stocking_quantity     = models.IntegerField(u'计划采购数量', max_length=10, blank=True, null=True)
    QTY                   = models.IntegerField(u'采购数量', max_length=10, blank=True, null=True)
    Price                 = models.DecimalField(u'含税单价',max_digits=10,decimal_places=2,blank = True,null = True)
    Weight                = models.DecimalField(u'商品克重',max_digits=10,decimal_places=2,blank = True,null = True)
    Remarks               = models.TextField(u'备注', blank=True, null=True)
    Supplier              = models.CharField(u'供应商', max_length=128, blank=True, null=True)
    Supplierlink          = models.CharField(u'采购连接', max_length=200, blank=True, null=True)
    Ali_number            = models.CharField(u'1688单号', max_length=63, blank=True, null=True)
    Arrival_date          = models.DateField(u'预计到货日期', blank=True, null=False)
    Contract_No           = models.CharField(u'合同号',max_length=16,blank=True,null=True)
    Buyer                 = models.CharField(u'采购人', max_length=16, blank=True, null=True)
    Logistics_costs       = models.DecimalField(u'物流费',max_digits=10,decimal_places=2,blank = True,null = True)
    pay_method            = models.CharField(u'付款方式', max_length=16, blank=True, null=True)
    ThePeople             = models.CharField(u'制单人', max_length=16, blank=True, null=True)
    TheTime               = models.DateTimeField(u'制单时间',blank=True, null=True)
    Warehouse             = models.CharField(u'仓库', choices=getChoices(ChoiceWarehouse),max_length=64, blank=True, null=True)
    Prepayments           = models.DecimalField(u'预付款',max_digits=10,decimal_places=2,blank = True,null = True)
    Status                = models.CharField(u'采购进行状态',choices=getChoices(ChoicePurchStatus),max_length=16, blank=True, null=True)
    ExcelStatus           = models.CharField(u'导出状态',choices=getChoices(ChoiceEStatus),max_length=16, blank=True, null=True)
    UpdateTime            = models.DateTimeField(u'更新时间',auto_now=True,blank = True,null = True)
    Demand_people         = models.CharField(u'计划需求人', max_length=32, blank=True, null=True)
    LogisticsNumber       = models.CharField(u'物流单号', max_length=128, blank=True, null=True)
    level                 = models.CharField(u'紧急程度', choices=getChoices(ChoiceLevel), max_length=16, blank=True, null=True)
    Site                  = models.CharField(u'站点', max_length=16, blank=True, null=True)
    AccountNum            = models.CharField(u'账号', max_length=32, blank=True, null=True)
    OplogTime             = models.DateTimeField(u'记录生成时间',blank=True,null=True)
    Arrival_date1         = models.DateTimeField(u'到货日期', blank=True, null=True)
    Arrival_status        = models.CharField(u'到货状态', choices=getChoices(ChoiceArrivalStatus), max_length=64, blank=True,null=True)
    Storage_status        = models.CharField(u'入库状态', choices=getChoices(ChoiceStorageStatus), max_length=64, blank=True,null=True)
    StorageDate           = models.DateTimeField(u'入库日期', blank=True, null=True)
    The_arrival_of_the_number = models.IntegerField(u'本次到货数量', max_length=10, blank=True, null=True)
    completeInstoreMan    = models.CharField(u'完成入库人', max_length=32, blank=True, null=True)
    completeInstoreDate   = models.DateTimeField(u'完成入库时间', blank=True, null=True)
    splitMan              = models.CharField(u'拆分订单人', max_length=32, blank=True, null=True)
    splitTime             = models.DateTimeField(u'拆分订单时间', blank=True, null=True)
    splitRemark           = models.CharField(u'拆分备注', max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = u'采购计划表'
        verbose_name_plural = verbose_name
        db_table = 't_stocking_purchase_order'

    def __unicode__(self):
        return u'%s' % (self.id)