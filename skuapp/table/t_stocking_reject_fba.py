# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 王芝杨
 @site: 
 @software: PyCharm
 @file: t_stocking_reject_fba.py
 @time: 2018-08-08

"""
from django.db import models
from .public import *


class t_stocking_reject_fba(models.Model):
    RejectNumber        = models.CharField(u'转退计划号', max_length=32, blank=True, null=True)
    RejectDate          = models.DateTimeField(u'转退时间', blank=True, null=True)
    RejectMan           = models.CharField(u'转退申请人', max_length=32, blank=True, null=True)
    PurchaseOrderNum    = models.CharField(u'采购单号', max_length=32)
    ProductSKU          = models.CharField(u'商品SKU', max_length=32)
    ProductName         = models.CharField(u'商品名称', max_length=64, blank=True, null=True)
    ProductImage        = models.CharField(u'商品图片', max_length=255, blank=True, null=True)
    RejectNum           = models.IntegerField(u'转退数量', max_length=10)
    Status              = models.CharField(u'转退状态', choices=getChoices(ChoiceRejectFBAStatus), max_length=16, blank=True, null=True)
    RejectStatus        = models.CharField(u'转退状态', choices=getChoices(ChoiceRejectFBAStatus), max_length=16)
    SummbitRejectMan = models.CharField(u'转退提交人', max_length=32, blank=True, null=True)
    SummbitRejectDate = models.DateTimeField(u'转退提交时间', blank=True, null=True)
    GiveupMan = models.CharField(u'转退废弃人', max_length=32, blank=True, null=True)
    GiveupDate = models.DateTimeField(u'转退废弃时间', blank=True, null=True)
    Remarks             = models.CharField(u'备注', max_length=16, blank=True, null=True)
    ReturnNumber = models.CharField(u'转退订单号', max_length=32, blank=True, null=True)
    isCheckTranReturn = models.IntegerField(u'质检退货标志', max_length=2)
    ActualRejectNum = models.IntegerField(u'实际退货数量', max_length=10)

    class Meta:
        verbose_name = u'FBA转退'
        verbose_name_plural = verbose_name
        db_table = 't_stocking_reject_fba'

    def __unicode__(self):
        return u'%s' % (self.id)