# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_shop_refund_status.py
 @time: 2018/10/24 14:23
"""  
from django.db import models


class t_amazon_shop_refund_status(models.Model):
    shop_name = models.CharField(u'店铺', max_length=32, blank=True, null=True)
    all_order = models.IntegerField(u'总订单量', max_length=10, blank=True, null=True)
    refund_order = models.IntegerField(u'退款订单量', max_length=10, blank=True, null=True)
    refund_rate = models.FloatField(u'退款率', max_length=5, blank=True, null=True)
    refresh_time = models.DateTimeField(u'更新时间', blank=True, null=True)

    class Meta:
        verbose_name = u'AMZ店铺退款情况'
        verbose_name_plural = verbose_name
        db_table = 't_amazon_shop_refund_status'

    def __unicode__(self):
        return u'%s' % self.id