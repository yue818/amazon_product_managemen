# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_conversion_detail.py
 @time: 2018/12/6 15:55
"""  
from django.db import models


class t_amazon_conversion_detail(models.Model):
    shop_name = models.CharField(u'店铺', max_length=32, blank=True, null=True)
    seller = models.CharField(u'销售员', max_length=32, blank=True, null=True)
    seller_sku = models.CharField(u'店铺SKU', max_length=255, blank=True, null=True)
    product_sku = models.CharField(u'商品SKU', max_length=255, blank=True, null=True)
    product_sku_zh = models.CharField(u'组合SKU', max_length=2000, blank=True, null=True)
    product_sku_zh_multiply = models.IntegerField(u'组合SKU组合量', max_length=10, blank=True, null=True)
    quantity_multiply = models.IntegerField(u'商品组合量', max_length=10, blank=True, null=True)
    order_quantity = models.IntegerField(u'订单商品量', max_length=10, blank=True, null=True)
    afn_quantity = models.IntegerField(u'FBA库存', max_length=10, blank=True, null=True)
    warehouse_quantity = models.IntegerField(u'集合仓库存', max_length=10, blank=True, null=True)
    product_price = models.DecimalField(u'商品成本', max_digits=10, decimal_places=2, blank=True, null=True)
    time_span = models.CharField(u'时间范围', max_length=32, blank=True, null=True)
    refresh_time = models.DateTimeField(u'刷新时间', blank=True, null=True)

    class Meta:
        verbose_name = u'AMZ周转率-详单-商品SKU级'
        verbose_name_plural = verbose_name
        db_table = 't_amazon_conversion_detail'

    def __unicode__(self):
        return u'%s' % self.id
