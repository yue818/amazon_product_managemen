# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_sku_refund_status.py
 @time: 2018/10/24 14:29
"""  
from django.db import models


class t_amazon_sku_refund_status(models.Model):
    product_sku = models.CharField(u'商品SKU', max_length=255, blank=True, null=True)
    refund_order = models.IntegerField(u'退款订单量', max_length=10, blank=True, null=True)
    refresh_time = models.DateTimeField(u'更新时间', blank=True, null=True)

    class Meta:
        verbose_name = u'AMZ商品SKU退款情况'
        verbose_name_plural = verbose_name
        db_table = 't_amazon_sku_refund_status'

    def __unicode__(self):
        return u'%s' % self.id