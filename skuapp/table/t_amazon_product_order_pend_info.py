# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_product_order_pend_info.py
 @time: 2018/9/6 14:15
"""  
from django.db import models


class t_amazon_product_order_pend_info(models.Model):
    shop_name = models.CharField(u'店铺名', max_length=64, blank=True, null=True)
    seller_sku = models.CharField(u'店铺SKU', max_length=255, blank=True, null=True)
    asin = models.CharField(u'asin', max_length=64, blank=True, null=True)
    amazon_order_id = models.CharField(u'亚马逊订单号', max_length=64, blank=True, null=True)
    seller_sku_each = models.CharField(u'店铺SKU拆分', max_length=128, blank=True, null=True)
    product_sku = models.CharField(u'商品SKU', max_length=128, blank=True, null=True)
    quantity_multiply = models.IntegerField(u'商品SKU组合量', max_length=10, blank=True, null=True)
    quantity_inventory = models.IntegerField(u'Pending商品量', max_length=10, blank=True, null=True)
    product_sku_zh = models.CharField(u'组合SKU', max_length=128, blank=True, null=True)
    product_sku_zh_multiply = models.IntegerField(u'组合SKU组合量', max_length=10, blank=True, null=True)
    sku_unit_price = models.FloatField(u'商品单价', max_length=10, blank=True, null=True)
    total_price = models.FloatField(u'成本价', max_length=10, blank=True, null=True)
    purchase_date = models.DateTimeField(u'下单时间', blank=True, null=True)
    order_refresh_time = models.DateTimeField(u'订单刷新时间', blank=True, null=True)
    refresh_time = models.DateTimeField(u'更新时间', blank=True, null=True)

    class Meta:
        verbose_name = u'AMZ Pending订单详情'
        verbose_name_plural = verbose_name
        db_table = 't_amazon_product_order_pend_info'

    def __unicode__(self):
        return u'%s' % self.id