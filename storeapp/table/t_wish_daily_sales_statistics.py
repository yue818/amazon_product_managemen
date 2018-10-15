#-*-coding:utf-8-*-
u"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_wish_daily_sales_statistics.py
 @time: 2018/9/5 9:47
"""
from django.db import models

class t_wish_daily_sales_statistics(models.Model):
    OrderDate   = models.DateField(u'订单日期',  blank=True, null=True)
    OfSales     = models.DecimalField(u'日总销售额', max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name=u'Wish日总销售额统计'
        verbose_name_plural=verbose_name
        db_table = 't_wish_daily_sales_statistics'

    def __unicode__(self):
        return u'OrderDate:%s;OfSales:%s'%(self.OrderDate,self.OfSales)












