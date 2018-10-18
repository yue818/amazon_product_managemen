# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_actionable_order_data.py
 @time: 2018/10/17 9:30
"""  
from django.db import models


class t_amazon_actionable_order_data(models.Model):
    order_id = models.CharField(u'订单编号', max_length=32, blank=True, null=True)
    order_item_id = models.CharField(u'订单商品编号', max_length=32, blank=True, null=True)
    purchase_date = models.DateTimeField(u'购买日期', blank=True, null=True)
    payments_date = models.DateTimeField(u'付款日期', blank=True, null=True)
    reporting_date = models.DateTimeField(u'报告日期', blank=True, null=True)
    promise_date = models.DateTimeField(u'承诺日期', blank=True, null=True)
    days_past_promise = models.IntegerField(u'超出承诺日期的天数', max_length=10, blank=True, null=True)
    buyer_email = models.CharField(u'买家电子邮件', max_length=128, blank=True, null=True)
    buyer_name = models.CharField(u'买家名称', max_length=64, blank=True, null=True)
    buyer_phone_number = models.CharField(u'买家电话号码', max_length=64, blank=True, null=True)
    sku = models.CharField(u'店铺SKU', max_length=255, blank=True, null=True)
    product_name = models.CharField(u'商品名称', max_length=255, blank=True, null=True)
    quantity_purchased = models.CharField(u'购买的数量', max_length=10, blank=True, null=True)
    quantity_shipped = models.CharField(u'已配送数量', max_length=10, blank=True, null=True)
    quantity_to_ship = models.CharField(u'待配送数量', max_length=10, blank=True, null=True)
    ship_service_level = models.CharField(u'运输方式', max_length=64, blank=True, null=True)
    recipient_name = models.CharField(u'收件人名称', max_length=64, blank=True, null=True)
    ship_address_1 = models.CharField(u'配送地址第 1 行', max_length=64, blank=True, null=True)
    ship_address_2 = models.CharField(u'配送地址第 2 行', max_length=64, blank=True, null=True)
    ship_address_3 = models.CharField(u'配送地址第 3 行', max_length=64, blank=True, null=True)
    ship_city = models.CharField(u'收货城市', max_length=64, blank=True, null=True)
    ship_state = models.CharField(u'收货省（州）', max_length=64, blank=True, null=True)
    ship_postal_code = models.CharField(u'邮编', max_length=64, blank=True, null=True)
    ship_country = models.CharField(u'国家', max_length=64, blank=True, null=True)
    shop_name = models.CharField(u'店铺', max_length=64, blank=True, null=True)
    refresh_time = models.DateTimeField(u'更新时间', blank=True, null=True)

    class Meta:
        verbose_name = u'亚马逊未发货订单'
        verbose_name_plural = verbose_name
        db_table = 't_amazon_actionable_order_data'

    def __unicode__(self):
        return u'%s' % self.id