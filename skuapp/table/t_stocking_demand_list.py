# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_stocking_demand_list.py
 @time: 2017-12-19 14:08

"""
from django.db import models
from .public import *


class t_stocking_demand_list(models.Model):
    Stocking_plan_number  = models.CharField(u'备货计划号', max_length=32, blank=True, null=True)
    Stock_plan_date       = models.DateTimeField(u'备货计划时间', blank=True, null=True)
    Demand_people         = models.CharField(u'计划需求人', max_length=32, blank=True, null=True)
    Product_nature        = models.CharField(u'产品性质',choices=getChoices(ChoiceProductnature), max_length=32)
    ProductSKU            = models.CharField(u'商品SKU', max_length=32)
    ShopSKU               = models.CharField(u'店铺SKU', max_length=32, blank=True, null=True)
    ProductName           = models.CharField(u'商品名称', max_length=64, blank=True, null=True)
    ProductImage          = models.CharField(u'商品图片', max_length=200, blank=True, null=True)
    ProductPrice          = models.DecimalField(u'商品价格',max_digits=10,decimal_places=2,blank = True,null = True)
    ProductWeight         = models.DecimalField(u'商品克重',max_digits=10,decimal_places=2,blank = True,null = True)
    Supplier              = models.CharField(u'供应商', max_length=128, blank=True, null=True)
    Supplierlink          = models.CharField(u'采购连接', max_length=200, blank=True, null=True)
    Stocking_quantity     = models.IntegerField(u'计划采购数量', max_length=10)
    AccountNum            = models.CharField(u'账号',  max_length=32, blank=True, null=True)
    Site                  = models.CharField(u'站点', max_length=16, blank=True, null=True)
    Destination_warehouse = models.CharField(u'目的地仓库',choices=getChoices(ChoiceWarehouse), max_length=63)
    level                 = models.CharField(u'紧急程度',choices=getChoices(ChoiceLevel),max_length=16, blank=True, null=True)
    Auditor               = models.CharField(u'审核人',max_length=16,blank=True,null=True)
    AuditTime             = models.DateTimeField(u'审核时间', blank=True, null=True)
    Buyer                 = models.CharField(u'采购人',max_length=16,blank=True,null=True)
    Remarks               = models.TextField(u'备注',blank=True,null=True)
    Status                = models.CharField(u'采购状态',choices=getChoices(ChoicePlanStatus),max_length=64,blank=True,null=True)
    UpdateTime            = models.DateTimeField(u'更新时间',auto_now=True,blank = True,null = True)
    neworold              = models.CharField(u'补货/新品', choices=getChoices(ChoiceNewOld), max_length=8)
    OplogTime             = models.DateTimeField(u'记录生成时间',blank=True,null=True)
    submitAuditMan = models.CharField(u'未生成采购计划-提交审核人', max_length=32, blank=True, null=True)
    submitAuditDate = models.DateTimeField(u'未生成采购计划-提交审核时间', blank=True, null=True)
    genPurchasePlanMan = models.CharField(u'生成采购计划人', max_length=32, blank=True, null=True)
    genPurchasePlanDate = models.DateTimeField(u'未生成采购计划-提交审核人', blank=True, null=True)
    completePurchaseDate = models.DateTimeField(u'完成采购时间', blank=True, null=True)
    completePurchaseMan = models.CharField(u'完成采购人', max_length=32, blank=True, null=True)
    AmazonFactory       = models.CharField(u'亚马逊服装', choices=getChoices(ChoiceAmazonFactory),max_length=16)

    class Meta:
        verbose_name = u'备货需求表'
        verbose_name_plural = verbose_name
        db_table = 't_stocking_demand_list'

    def __unicode__(self):
        return u'%s' % (self.id)