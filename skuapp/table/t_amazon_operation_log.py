# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_operation_log.py
 @time: 2018/8/22 9:48
"""  
from django.db import models


class t_amazon_operation_log(models.Model):
    batch_id = models.CharField(u'操作序列号', max_length=64, blank=True, null=True)
    shop_name = models.CharField(u'店铺', max_length=32, blank=True, null=True)
    seller_sku = models.CharField(u'店铺SKU', max_length=255, blank=True, null=True)
    action = models.CharField(u'操作类型', max_length=64, blank=True, null=True)
    price_before = models.FloatField(u'调整前价格', max_length=10, blank=True, null=True)
    price_after = models.FloatField(u'调整后价格', max_length=10, blank=True, null=True)
    deal_action = models.FileField(u'操作类型', max_length=64, blank=True, null=True)
    begin_time = models.DateTimeField(u'操作开始时间', blank=True, null=True)
    end_time = models.DateTimeField(u'操作结束时间', blank=True, null=True)
    deal_result = models.IntegerField(u'操作结果', max_length=1, blank=True, null=True)
    deal_result_info = models.FileField(u'结果详情', max_length=255, blank=True, null=True)
    remark = models.FileField(u'备注', max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = u'AMZ操作日志'
        verbose_name_plural = verbose_name
        db_table = 't_amazon_operation_log'

    def __unicode__(self):
        return u'%s' % self.id