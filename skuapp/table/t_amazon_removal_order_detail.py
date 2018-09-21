# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_removal_order_detail.py
 @time: 2018/8/23 10:49
"""  
from django.db import models


class t_amazon_removal_order_detail(models.Model):
    shop_name = models.CharField(u'店铺名', max_length=64, blank=True, null=True)
    sku = models.CharField(u'店铺SKU', max_length=255, blank=True, null=True)
    request_date = models.DateTimeField(u'日期', blank=True, null=True)
    order_id = models.CharField(u'订单编号', max_length=32, blank=True, null=True)
    order_type = models.CharField(u'订单类型', max_length=32, blank=True, null=True)
    order_status = models.CharField(u'订单状态', max_length=32, blank=True, null=True)
    requested_quantity = models.IntegerField(u'请求移除', max_length=10, blank=True, null=True)
    disposed_quantity = models.IntegerField(u'已完成', max_length=10, blank=True, null=True)
    shipped_quantity = models.IntegerField(u'已运输', max_length=10, blank=True, null=True)
    cancelled_quantity = models.IntegerField(u'取消移除', max_length=10, blank=True, null=True)
    in_process_quantity = models.IntegerField(u'处理中', max_length=10, blank=True, null=True)
    refresh_time = models.DateTimeField(u'更新时间', blank=True, null=True)

    class Meta:
        verbose_name = u'AMZ移除订单详情'
        verbose_name_plural = verbose_name
        db_table = 't_amazon_removal_order_detail'

    def __unicode__(self):
        return u'%s' % self.id
