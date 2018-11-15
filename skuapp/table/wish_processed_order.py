# encoding: utf-8
'''
@author: zhangyu
@contact: 292724306@qq.com
@software: pycharm
@file: wish_processed_order.py
@time: 2018-06-04 10:48
'''
from django.db import models


class wish_processed_order(models.Model):
    id = models.IntegerField(primary_key=True)
    shopName = models.CharField(u'店铺名称', max_length=255, blank=True, null=True)
    last_updated = models.CharField(u'日期', max_length=255, blank=True, null=True)
    expected_ship_date = models.CharField(max_length=255, blank=True, null=True)
    product_id = models.CharField(max_length=255, blank=True, null=True)
    buyer_id = models.CharField(max_length=255, blank=True, null=True)
    is_combined_order = models.CharField(max_length=255, blank=True, null=True)
    variant_id = models.CharField(max_length=255, blank=True, null=True)
    requires_delivery_confirmation = models.CharField(max_length=255, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    hours_to_fulfill = models.IntegerField(max_length=11, blank=True, null=True)
    order_size = models.CharField(u'变量', max_length=255, blank=True, null=True)
    sku = models.CharField(max_length=255, blank=True, null=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    days_to_fulfill = models.IntegerField(u'履行的天数', max_length=11, blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    order_time = models.CharField(max_length=255, blank=True, null=True)
    order_id = models.CharField(u'订单ID', max_length=255, blank=True, null=True)
    order_id = models.CharField(u'订单ID', max_length=255, blank=True, null=True)
    price = models.DecimalField(u'价格', max_digits=10, decimal_places=2, blank=True, null=True)
    released_to_merchant_time = models.CharField(max_length=255, blank=True, null=True)
    is_wish_express = models.CharField(max_length=255, blank=True, null=True)
    product_image_url = models.CharField(max_length=255, blank=True, null=True)
    tracking_confirmed = models.CharField(max_length=255, blank=True, null=True)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField(u'数量', max_length=11, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=255, blank=True, null=True)
    street_address1 = models.CharField(max_length=255, blank=True, null=True)
    street_address2 = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    updateTime = models.DateTimeField(u'同步时间', auto_now=True, blank=True, null=True)
    Operators = models.CharField(u'运营', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = u'Wish订单处理'
        verbose_name_plural = verbose_name
        db_table = 'wish_processed_order'
        ordering = ['days_to_fulfill']
