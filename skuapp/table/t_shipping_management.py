# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_shipping_management.py
 @time: 2017-12-19 16:29

"""   
from django.db import models
from .public import *


class t_shipping_management(models.Model):
    Stocking_plan_number                = models.CharField(u'备货计划号', max_length=32, blank=True, null=True)
    Delivery_lot_number                 = models.CharField(u'发货批次号', max_length=32, blank=True, null=True)
    Delivery_date                       = models.DateTimeField(u'发货日期', blank=True, null=True)
    Destination_warehouse               = models.CharField(u'目的地仓库',choices=getChoices(ChoiceWarehouse), max_length=32, blank=True, null=True)
    All_ProductSKU_Num                  = models.CharField(u'商品SKU*数量集合', max_length=200, blank=True, null=True)
    Sender                              = models.CharField(u'发货人', max_length=16, blank=True, null=True)
    The_first_Logistics_providers       = models.CharField(u'头程物流商', max_length=64, blank=True, null=True)
    The_first_Logistics_cost            = models.DecimalField(u'头程费用', max_digits=10,decimal_places=2,blank=True, null=True)
    LogisticsNumber                     = models.CharField(u'物流单号', max_length=128, blank=True, null=True)
    Cargo_infor                         = models.CharField(u'货物信息', max_length=10, blank=True, null=True)
    Invoice                             = models.CharField(u'发货清单（发票）', max_length=200, blank=True, null=True)
    BoxPaste                            = models.CharField(u'箱贴',max_length=200, blank=True, null=True)
    Warehouse_number                    = models.CharField(u'入库单号',max_length=200, blank=True, null=True)
    Status                              = models.CharField(u'本批次发货状态',choices=getChoices(Choicebatchstatus), max_length=64, blank=True, null=True)
    UpdateTime                          = models.DateTimeField(u'更新时间',auto_now=True,blank = True,null = True)
    Num                                 = models.IntegerField(u'实际发货数量',max_length=6,blank = True,null = True)
    BoxNum                              = models.IntegerField(u'发货箱数',max_length=4,blank = True,null = True)
    BoxWeight                           = models.DecimalField(u'发货重量',max_digits = 8 , decimal_places = 2,blank = True,null = True)
    BoxSize                             = models.DecimalField(u'发货尺寸',max_digits = 8 , decimal_places = 2,blank = True,null = True)
    LogisticsMode                       = models.CharField(u'物流方式', max_length=200, blank=True, null=True)
    GoodsCategory                       = models.CharField(u'货物品类', max_length=200, blank=True, null=True)
    OplogTime                           = models.DateTimeField(u'记录生成时间',blank=True,null=True)
    getDetailedList                     = models.CharField(u'获取发货清单和箱标人', max_length=32, blank=True, null=True)
    getDetailedTime                     = models.DateTimeField(u'获取发货清单和箱标时间', blank=True, null=True)

    class Meta:
        verbose_name = u'发货管理'
        verbose_name_plural = verbose_name
        db_table = 't_shipping_management'

    def __unicode__(self):
        return u'%s' % (self.id)