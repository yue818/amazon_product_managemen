# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 王芝杨
 @site: 
 @software: PyCharm
 @file: t_stocking_check_report.py
 @time: 2018-07-31 14:08

"""
from django.db import models

class t_stocking_check_report(models.Model):
    id                    = models.AutoField(u'业务流水号',primary_key=True)
    Stocking_plan_number  = models.CharField(u'备货计划号', max_length=32, blank=True, null=True)
    Purchase_Order_No     = models.CharField(u'采购单号', max_length=32, blank=True, null=True)
    Purchase_date         = models.DateTimeField(u'入库时间', blank=True, null=True)
    ProductSKU            = models.CharField(u'商品SKU', max_length=32)
    ProductName           = models.CharField(u'商品名称', max_length=255, blank=True, null=True)
    ProductImage          = models.CharField(u'商品图片', max_length=255, blank=True, null=True)
    ProductPrice          = models.DecimalField(u'商品价格',max_digits=10,decimal_places=2,blank = True,null = True)
    ProductWeight         = models.DecimalField(u'商品克重',max_digits=10,decimal_places=2,blank = True,null = True)
    Purchaser             = models.CharField(u'采购员', max_length=32, blank=True, null=True)
    SalerName             = models.CharField(u'业绩归属人1', max_length=32, blank=True, null=True)
    SalerName2            = models.CharField(u'业绩归属人2', max_length=32, blank=True, null=True)
    PurchaseNumber        = models.IntegerField(u'采购数量', max_length=10)
    ArrivalNumber         = models.IntegerField(u'到货数量', max_length=10)
    CheckNumber           = models.IntegerField(u'抽检数量', max_length=10)
    CheckQualified        = models.IntegerField(u'抽检合格数量', max_length=10)
    PercentOfPass         = models.CharField(u'合格率',  max_length=16, blank=True, null=True)
    CheckMan              = models.CharField(u'抽检人', max_length=32, blank=True, null=True)
    CheckTime             = models.DateTimeField(u'抽检时间', blank=True, null=True)
    Remark                = models.TextField(u'抽检备注',blank=True,null=True)
    isCheck               = models.IntegerField(u'是否需要抽检',max_length=2,blank=True,null=True)
    isFBA                 = models.CharField(u'是否属于FBA', max_length=32, blank=True, null=True)
    Demand_people         = models.CharField(u'计划需求人', max_length=32, blank=True, null=True)
    class Meta:
        verbose_name = u'质检报告'
        verbose_name_plural = verbose_name
        db_table = 't_stocking_check_report'

    def __unicode__(self):
        return u'%s' % (self.id)