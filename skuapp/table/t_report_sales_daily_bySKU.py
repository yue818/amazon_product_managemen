# -*- coding: utf-8 -*-
from django.db import models
from public import *


class t_report_sales_daily_bySKU(models.Model):
    OrderDay        =   models.DateField(u'订单日期',blank = True,null = True)
    SKU             =   models.CharField(u'商品SKU',max_length=100,blank = True,null = True)
    SalesVolume     =   models.PositiveSmallIntegerField(u'日销售量',max_length=11,blank = True,null = True)



    class Meta:
        verbose_name=u'SKU日销量'
        verbose_name_plural=verbose_name
        db_table = 't_report_sales_daily_bySKU'
        ordering = ['-OrderDay']
    def __unicode__(self):
        return u'id:%s'%(self.id)