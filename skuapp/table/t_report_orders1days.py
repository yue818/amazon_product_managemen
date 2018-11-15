# -*- coding: utf-8 -*-
from django.db import models
from public import *


class t_report_orders1days(models.Model):
    YYYYMMDD                =   models.CharField(u'年月日(UTC)',max_length=32,blank = True,null = True)
    PlatformName            =   models.CharField(u'平台名称',max_length=32,blank = True,null = True)
    ShopName                =   models.CharField(u'店铺名称',max_length=32,blank = True,null = True)
    ProductID               =   models.CharField(u'ProductID',max_length=32,blank = True,null = True)
    OrdersLast1Days         =   models.PositiveSmallIntegerField(u'日order数',blank = True,null = True)
    OrdersLast7Days         =   models.PositiveSmallIntegerField(u'7天order数',blank = True,null = True)
    UpdateTime              =   models.DateTimeField(u'更新时间',auto_now=True,blank = True,null = True)
    
    class Meta:
        verbose_name=u'日销量统计表'
        verbose_name_plural=verbose_name
        db_table = 't_report_orders1days'
        ordering = ['-YYYYMMDD']

    def __unicode__(self):
        return u'%s'%(self.id)


class t_report_orders1days_wish_overseas_warehouse(models.Model):
    YYYYMMDD = models.CharField(u'年月日(UTC)', max_length=32, blank=True, null=True)
    PlatformName = models.CharField(u'平台名称', max_length=32, blank=True, null=True)
    ShopName = models.CharField(u'店铺名称', max_length=32, blank=True, null=True)
    ProductID = models.CharField(u'ProductID', max_length=32, blank=True, null=True)
    OrdersLast1Days = models.PositiveSmallIntegerField(u'日order数', blank=True, null=True)
    OrdersLast7Days = models.PositiveSmallIntegerField(u'7天order数', blank=True, null=True)
    UpdateTime = models.DateTimeField(u'更新时间', auto_now=True, blank=True, null=True)
    WarehouseName = models.CharField(u'海外仓名称', max_length=64, blank=True, null=True)

    class Meta:
        verbose_name = u'日销量统计表(海外仓)'
        verbose_name_plural = verbose_name
        db_table = 't_report_orders1days_wish_overseas_warehouse'
        ordering = ['-YYYYMMDD']

    def __unicode__(self):
        return u'%s' % (self.id)