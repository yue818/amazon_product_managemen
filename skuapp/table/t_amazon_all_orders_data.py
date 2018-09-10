# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_all_orders_data.py
 @time: 2018-06-20 17:15
"""  


from django.db import models


class t_amazon_all_orders_data(models.Model):
    amazon_order_id = models.CharField(u'订单号', max_length=32, blank=True, null=True)
    purchase_date = models.DateTimeField(u'下单日期', blank=True, null=True)
    last_updated_date = models.DateTimeField(u'订单更新日期', blank=True, null=True)
    order_status = models.CharField(u'订单状态', max_length=32, blank=True, null=True)
    fulfillment_channel = models.CharField(u'配送方式', max_length=32, blank=True, null=True)
    sales_channel = models.CharField(u'订单渠道', max_length=32, blank=True, null=True)
    shop_name = models.CharField(u'店铺', max_length=50, blank=True, null=True)
    sku = models.CharField(u'店铺SKU', max_length=128, blank=True, null=True)
    asin = models.CharField(u'ASIN', max_length=32, blank=True, null=True)
    item_status = models.CharField(u'订单商品状态', max_length=32, blank=True, null=True)
    quantity = models.CharField(u'商品数量', max_length=10, blank=True, null=True)
    currency = models.CharField(u'货币', max_length=32, blank=True, null=True)
    item_price = models.CharField(u'总金额', max_length=32, blank=True, null=True)
    item_tax = models.CharField(u'税', max_length=32, blank=True, null=True)
    shipping_price = models.CharField(u'运费', max_length=32, blank=True, null=True)
    shipping_tax = models.CharField(u'运费税', max_length=32, blank=True, null=True)
    ship_country = models.CharField(u'国家', max_length=32, blank=True, null=True)
    ship_city = models.CharField(u'城市', max_length=32, blank=True, null=True)
    ship_state = models.CharField(u'地区', max_length=32, blank=True, null=True)
    ship_postal_code = models.CharField(u'邮编', max_length=32, blank=True, null=True)
    refresh_time = models.DateTimeField(u'更新时间', blank=True, null=True)

    class Meta:
        verbose_name = u'亚马逊订单数据'
        verbose_name_plural = verbose_name
        db_table = 't_amazon_all_orders_data'

    def __unicode__(self):
        return u'%s' % self.id