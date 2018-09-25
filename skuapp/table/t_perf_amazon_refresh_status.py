# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_perf_amazon_refresh_status.py
 @time: 2018/9/25 9:59
"""  
from django.db import models


class t_perf_amazon_refresh_status(models.Model):
    name = models.CharField(u'店铺全称', max_length=32, blank=True, null=True)
    shop_name = models.CharField(u'店铺', max_length=32, blank=True, null=True)
    shop_site = models.CharField(u'站点', max_length=32, blank=True, null=True)
    ip = models.CharField(u'IP', max_length=32, blank=True, null=True)

    product_refresh_status = models.CharField(u'商品刷新状态', max_length=32, blank=True, null=True)
    product_refresh_begin_time = models.DateTimeField(u'商品刷新开始时间', blank=True, null=True)
    product_refresh_end_time = models.DateTimeField(u'商品刷新结束时间', blank=True, null=True)
    product_refresh_remark = models.CharField(u'商品刷新备注', max_length=255, blank=True, null=True)

    fba_refresh_status = models.CharField(u'FBA库存刷新状态', max_length=32, blank=True, null=True)
    fba_refresh_begin_time = models.DateTimeField(u'FBA库存刷新开始时间', blank=True, null=True)
    fba_refresh_end_time = models.DateTimeField(u'FBA库存刷新结束时间', blank=True, null=True)
    fba_refresh_remark = models.CharField(u'FBA库存刷新备注', max_length=255, blank=True, null=True)

    order_refresh_status = models.CharField(u'订单刷新状态', max_length=32, blank=True, null=True)
    order_refresh_begin_time = models.DateTimeField(u'订单刷新开始时间', blank=True, null=True)
    order_refresh_end_time = models.DateTimeField(u'订单刷新结束时间', blank=True, null=True)
    order_refresh_remark = models.CharField(u'订单刷新备注', max_length=255, blank=True, null=True)

    receive_refresh_status = models.CharField(u'到货日期刷新状态', max_length=32, blank=True, null=True)
    receive_refresh_begin_time = models.DateTimeField(u'到货日期刷新开始时间', blank=True, null=True)
    receive_refresh_end_time = models.DateTimeField(u'到货日期刷新结束时间', blank=True, null=True)
    receive_refresh_remark = models.CharField(u'到货日期刷新备注', max_length=255, blank=True, null=True)

    fee_refresh_status = models.CharField(u'预览费用刷新状态', max_length=32, blank=True, null=True)
    fee_refresh_begin_time = models.DateTimeField(u'预览费用刷新开始时间', blank=True, null=True)
    fee_refresh_end_time = models.DateTimeField(u'预览费用刷新结束时间', blank=True, null=True)
    fee_refresh_remark = models.CharField(u'预览费用刷新备注', max_length=255, blank=True, null=True)

    remove_refresh_status = models.CharField(u'移除订单刷新状态', max_length=32, blank=True, null=True)
    remove_refresh_begin_time = models.DateTimeField(u'移除订单刷新开始时间', blank=True, null=True)
    remove_refresh_end_time = models.DateTimeField(u'移除订单刷新结束时间', blank=True, null=True)
    remove_refresh_remark = models.CharField(u'移除订单刷新备注', max_length=255, blank=True, null=True)

    finance_refresh_status = models.CharField(u'退款记录刷新状态', max_length=32, blank=True, null=True)
    finance_refresh_begin_time = models.DateTimeField(u'退款记录刷新开始时间', blank=True, null=True)
    finance_refresh_end_time = models.DateTimeField(u'退款记录刷新结束时间', blank=True, null=True)
    finance_refresh_remark = models.CharField(u'退款记录刷新备注', max_length=255, blank=True, null=True)

    is_valid = models.IntegerField(u'店铺状态', max_length=1, blank=True, null=True)

    class Meta:
        verbose_name = u'AMZ店铺刷新状态记录'
        verbose_name_plural = verbose_name
        db_table = 't_perf_amazon_refresh_status'
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % self.id