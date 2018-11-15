# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 王芝杨
 @site: 
 @software: PyCharm
 @file: t_stocking_demand_fba.py
 @time: 2018-08-08

"""
from django.db import models
from .public import *


class t_stocking_demand_fba(models.Model):
    Stocking_plan_number  = models.CharField(u'备货计划号', max_length=32, blank=True, null=True)
    Stock_plan_date       = models.DateTimeField(u'备货计划时间', blank=True, null=True)
    Demand_people         = models.CharField(u'计划需求人', max_length=32, blank=True, null=True)
    ProductSKU            = models.CharField(u'商品SKU', max_length=32)
    ProductPrice = models.DecimalField(u'商品价格', max_digits=10, decimal_places=2, blank=True, null=True)
    ProductWeight = models.DecimalField(u'商品克重', max_digits=10, decimal_places=2, blank=True, null=True)
    ProductName           = models.CharField(u'商品名称', max_length=64, blank=True, null=True)
    ProductImage          = models.CharField(u'商品图片', max_length=200, blank=True, null=True)
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
    Status                = models.CharField(u'采购状态',choices=getChoices(ChoiceFBAPlanStatus),max_length=64,blank=True,null=True)
    UpdateTime            = models.DateTimeField(u'更新时间',auto_now=True,blank = True,null = True)
    importfile            = models.CharField(u'导入文件', max_length=64, blank=True, null=True)
    Product_nature = models.CharField(u'产品性质', choices=getChoices(ChoiceProductnature), max_length=32)
    ShopSKU = models.CharField(u'店铺SKU', max_length=32, blank=True, null=True)
    neworold              = models.CharField(u'补货/新品', choices=getChoices(ChoiceNewOld), max_length=8)
    OplogTime = models.DateTimeField(u'记录生成时间', blank=True, null=True)
    giveupMan = models.CharField(u'不需备货人', max_length=32, blank=True, null=True)
    giveupDate = models.DateTimeField(u'不需备货时间', blank=True, null=True)
    genPurchasePlanMan = models.CharField(u'生成采购计划人', max_length=32, blank=True, null=True)
    genPurchasePlanDate = models.DateTimeField(u'未生成采购计划-提交审核人', blank=True, null=True)
    recordPurchaseCodeDate = models.DateTimeField(u'录入采购编码时间', blank=True, null=True)
    recordPurchaseCodeMan = models.CharField(u'录入采购编码人', max_length=32, blank=True, null=True)
    completePurchaseDate = models.DateTimeField(u'完成采购时间', blank=True, null=True)
    completePurchaseMan = models.CharField(u'完成采购人', max_length=32, blank=True, null=True)
    completeStatus = models.CharField(u'完成采购状态', choices=getChoices(ChoiceFBAPlanStatus), max_length=64, blank=True, null=True)
    LogisticsNumber = models.CharField(u'物流单号', max_length=32, blank=True, null=True)
    Single_number = models.CharField(u'采购单号', max_length=32, blank=True, null=True)
    Ali_number = models.CharField(u'1688单号', max_length=32, blank=True, null=True)
    QTY = models.CharField(u'实际采购数量', max_length=32, blank=True, null=True)
    Arrival_date = models.DateTimeField(u'到货时间', blank=True, null=True)
    The_arrival_of_the_number = models.IntegerField(u'本次到货数量', max_length=10)
    sumbitCheckMan = models.CharField(u'提交质检人', max_length=32, blank=True, null=True)
    sumbitCheckDate = models.DateTimeField(u'提交质检时间', blank=True, null=True)
    CheckMan = models.CharField(u'质检人', max_length=32, blank=True, null=True)
    CheckTime = models.DateTimeField(u'质检时间', blank=True, null=True)
    checkStatus = models.CharField(u'质检状态', choices=getChoices(ChoiceFBAPlanStatus), max_length=64, blank=True,
                                      null=True)
    CheckNumber = models.IntegerField(u'抽检数量', max_length=10)
    CheckQualified = models.IntegerField(u'抽检合格数量', max_length=10)
    PercentOfPass = models.CharField(u'合格率', max_length=16, blank=True, null=True)
    isCheck = models.IntegerField(u'是否需要抽检', max_length=2, blank=True, null=True)
    genBatchMan = models.CharField(u'生成批次人', max_length=32, blank=True, null=True)
    genBatchDate = models.DateTimeField(u'生成批次时间', blank=True, null=True)
    genStatus = models.CharField(u'批次生成状态', choices=getChoices(ChoiceFBAPlanStatus), max_length=64, blank=True,
                                   null=True)
    Delivery_lot_number = models.CharField(u'发货批次号', max_length=32, blank=True, null=True)
    ExcelStatus = models.CharField(u'导出状态', choices=getChoices(ChoiceEStatus), max_length=16, blank=True, null=True)
    AmazonFactory = models.CharField(u'亚马逊服装', choices=getChoices(ChoiceAmazonFactory), max_length=16)
    Number = models.IntegerField(u'库存数量', max_length=10)
    TransFactory = models.CharField(u'转供应链', max_length=32, blank=True, null=True)
    checkCompleteNum = models.IntegerField(u'合格总量', max_length=10)
    checkInferiorNum = models.IntegerField(u'次品总量', max_length=10)
    tranReturnNum = models.IntegerField(u'转退数量', max_length=10)
    deliverNum = models.IntegerField(u'发货数量', max_length=10)
    tranReturnMan = models.CharField(u'转退人', max_length=32, blank=True, null=True)
    tranReturnDate = models.DateTimeField(u'转退时间', blank=True, null=True)
    pyRemark = models.TextField(u'普元备注', blank=True, null=True)
    checkConfirmMan = models.CharField(u'质检确认人', max_length=32, blank=True, null=True)
    checkConfirmDate = models.DateTimeField(u'质检确认时间', blank=True, null=True)
    checkConfirmFlag = models.CharField(u'质检确认标记', max_length=2, blank=True, null=True)

    class Meta:
        verbose_name = u'FBA备货需求'
        verbose_name_plural = verbose_name
        db_table = 't_stocking_demand_fba'

    def __unicode__(self):
        return u'%s' % (self.id)