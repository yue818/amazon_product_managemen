# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_conversion_info.py
 @time: 2018/12/6 15:47
"""  
from django.db import models


class t_amazon_conversion_info(models.Model):
    shop_name = models.CharField(u'店铺', max_length=32, blank=True, null=True)
    seller = models.CharField(u'销售员', max_length=32, blank=True, null=True)
    seller_sku = models.CharField(u'店铺SKU', max_length=255, blank=True, null=True)
    product_sku = models.CharField(u'商品SKU', max_length=255, blank=True, null=True)
    com_pro_sku = models.CharField(u'组合SKU', max_length=2000, blank=True, null=True)
    begin_time = models.DateTimeField(u'库存起始时间', blank=True, null=True)
    begin_quantity = models.IntegerField(u'起始库存量', max_length=10, blank=True, null=True)
    end_time = models.DateTimeField(u'库存终止时间', blank=True, null=True)
    end_quantity = models.IntegerField(u'终止库存量', max_length=10, blank=True, null=True)
    orders = models.IntegerField(u'订单量', max_length=10, blank=True, null=True)
    order_quantity = models.IntegerField(u'订单商品量', max_length=10, blank=True, null=True)
    time_span = models.CharField(u'时间范围', max_length=32, blank=True, null=True)
    refresh_time = models.DateTimeField(u'刷新时间', blank=True, null=True)

    class Meta:
        verbose_name = u'AMZ周转率-详单-店铺SKU级'
        verbose_name_plural = verbose_name
        db_table = 't_amazon_conversion_info'

    def __unicode__(self):
        return u'%s' % self.id
