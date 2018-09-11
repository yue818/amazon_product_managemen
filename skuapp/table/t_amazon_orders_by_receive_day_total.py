# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_orders_by_receive_day_total.py
 @time: 2018/9/10 16:55
"""

from django.db import models


class t_amazon_orders_by_receive_day_total(models.Model):
    seller = models.CharField(u'销售员', max_length=32, blank=True, null=True)
    site = models.CharField(u'站点', max_length=32, blank=True, null=True)
    has_order = models.IntegerField(u'出单', max_length=10, blank=True, null=True)
    no_order = models.IntegerField(u'出单', max_length=10, blank=True, null=True)
    time_span = models.CharField(u'到货时间范围', max_length=32, blank=True, null=True)
    refresh_time = models.DateTimeField(u'更新时间', blank=True, null=True)

    class Meta:
        verbose_name = u'AMZ按到货日期出单情况'
        verbose_name_plural = verbose_name
        db_table = 't_amazon_orders_by_receive_day_total'

    def __unicode__(self):
        return u'%s' % self.id