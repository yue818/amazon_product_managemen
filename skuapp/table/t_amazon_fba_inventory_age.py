# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_fba_inventory_age.py
 @time: 2018/11/21 16:48
"""  
from django.db import models


class t_amazon_fba_inventory_age(models.Model):
    shop_name = models.CharField(u'店铺', max_length=32, blank=True, null=True)
    sku = models.CharField(u'店铺SKU', max_length=255, blank=True, null=True)
    asin = models.CharField(u'ASIN', max_length=64, blank=True, null=True)
    snapshot_date = models.DateTimeField(u'报告时间', blank=True, null=True)
    qty_to_be_charged_ltsf_6_mo = models.CharField(u'库龄超6个月(数量)', max_length=64, blank=True, null=True)
    projected_ltsf_6_mo = models.CharField(u'仓储费(6个月)', max_length=32, blank=True, null=True)
    qty_to_be_charged_ltsf_12_mo = models.CharField(u'库龄超12个月(数量)', max_length=32, blank=True, null=True)
    projected_ltsf_12_mo = models.CharField(u'仓储费(12个月)', max_length=32, blank=True, null=True)
    seller = models.CharField(u'销售员', max_length=32, blank=True, null=True)
    refresh_time = models.DateTimeField(u'刷新时间', blank=True, null=True)

    class Meta:
        verbose_name = u'AMZ库龄'
        verbose_name_plural = verbose_name
        db_table = 't_amazon_fba_inventory_age'

    def __unicode__(self):
        return u'%s' % self.id