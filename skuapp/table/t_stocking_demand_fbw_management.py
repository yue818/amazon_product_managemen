# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: wangzhiyang
 @site: 
 @software: PyCharm
 @file: t_stocking_demand_fbw_management.py
 @time: 2018-10-18

"""   
from django.db import models
from .public import *


class t_stocking_demand_fbw_management(models.Model):
    Stocking_plan_number                = models.TextField(u'发货计划号', blank=True, null=True)
    Delivery_lot_number                 = models.CharField(u'发货批次号', max_length=64, blank=True, null=True)
    Delivery_date                       = models.DateTimeField(u'发货日期', blank=True, null=True)
    Destination_warehouse               = models.CharField(u'目的地仓库',choices=getChoices(ChoiceWarehouse), max_length=32, blank=True, null=True)
    All_ProductSKU_Num                  = models.TextField(u'商品SKU*数量集合', blank=True, null=True)
    Sender                              = models.CharField(u'发货人', max_length=16, blank=True, null=True)
    LogisticsNumber                     = models.CharField(u'物流单号', max_length=128, blank=True, null=True)
    Status                              = models.CharField(u'本批次发货状态',choices=getChoices(Choicedeliverstatus), max_length=64, blank=True, null=True)
    UpdateTime                          = models.DateTimeField(u'更新时间',auto_now=True,blank = True,null = True)
    OplogTime                           = models.DateTimeField(u'记录生成时间',blank=True,null=True)
    All_deman_people                     = models.TextField(u'发货计划人', blank=True, null=True)
    remarks = models.TextField(u'备注', blank=True, null=True)

    class Meta:
        verbose_name = u'FBW发货物流信息'
        verbose_name_plural = verbose_name
        db_table = 't_stocking_demand_fbw_management'

    def __unicode__(self):
        return u'%s' % (self.id)