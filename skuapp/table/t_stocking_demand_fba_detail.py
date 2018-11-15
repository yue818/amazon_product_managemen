# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 王芝杨
 @site: 
 @software: PyCharm
 @file: t_stocking_demand_fba_detail.py
 @time: 2018-08-21

"""
from django.db import models
from .public import *

class t_stocking_demand_fba_detail(models.Model):
    ProductSKU = models.CharField(u'商品SKU', max_length=32)
    Stocking_plan_number = models.CharField(u'备货计划号', max_length=32)
    Status = models.CharField(u'状态', choices=getChoices(ChoiceFBAPlanStatus), max_length=16, blank=True, null=True)
    CreateDate = models.DateTimeField(u'生成SKU时间', blank=True, null=True)
    AuditFlag = models.IntegerField(u'核实标记', max_length=1)
    AuditMan = models.CharField(u'已核查人', max_length=32, blank=True, null=True)
    AuditDate = models.DateTimeField(u'已核查时间', blank=True, null=True)
    Remarks = models.TextField(u'备注', blank=True, null=True)
    class Meta:
        verbose_name = u'FBA明细一览'
        verbose_name_plural = verbose_name
        db_table = 't_stocking_demand_fba_detail'
    def __unicode__(self):
        return u'%s' % (self.id)