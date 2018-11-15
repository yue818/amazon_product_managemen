# -*- coding: utf-8 -*-
from django.db import models
from public import *


class t_report_sales_daily_byPlatform(models.Model):
    OrderDay        =   models.DateField(u'订单日期',blank = True,null = True)
    PlatformName    =   models.CharField(u'平台名称',max_length=16,blank = True,null = True)
    SalesVolume     =   models.PositiveSmallIntegerField(u'日销售量',max_length=11,blank = True,null = True)



    class Meta:
        verbose_name=u'平台日销量'
        verbose_name_plural=verbose_name
        db_table = 't_report_sales_daily_byPlatform'
        ordering = ['-OrderDay']
    def __unicode__(self):
        return u'id:%s'%(self.id)