# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_product_price_info.py
 @time: 2018/8/20 15:00
"""  
from django.db import models


class t_amazon_product_price_info(models.Model):
    shop_name = models.CharField(u'店铺名', max_length=64, blank=True, null=True)
    seller_sku = models.CharField(u'店铺SKU', max_length=255, blank=True, null=True)
    asin = models.CharField(u'asin', max_length=64, blank=True, null=True)
    seller_sku_each = models.CharField(u'店铺SKU拆分', max_length=128, blank=True, null=True)
    product_sku = models.CharField(u'商品SKU', max_length=128, blank=True, null=True)
    quantity_multiply = models.IntegerField(u'商品SKU组合量', max_length=10, blank=True, null=True)
    quantity_inventory = models.IntegerField(u'商品SKU库存量', max_length=10, blank=True, null=True)
    sku_unit_price = models.FloatField(u'商品单价', max_length=10, blank=True, null=True)
    total_price = models.FloatField(u'成本价', max_length=10, blank=True, null=True)
    status = models.FileField(u'状态', max_length=32, blank=True, null=True)
    is_fba = models.IntegerField(u'是否FBA', max_length=1, blank=True, null=True)
    UpdateTime = models.DateTimeField(u'更新时间', blank=True, null=True)

    class Meta:
        verbose_name = u'AMZ商品库存价格信息'
        verbose_name_plural = verbose_name
        db_table = 't_amazon_product_price_info'

    def __unicode__(self):
        return u'%s' % (self.id)