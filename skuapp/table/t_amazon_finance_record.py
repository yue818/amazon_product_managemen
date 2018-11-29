# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_finance_record.py
 @time: 2018/11/19 9:15
"""  
from django.db import models


class t_amazon_finance_record(models.Model):
    shop_name = models.CharField(u'店铺', max_length=32, blank=True, null=True)
    seller_sku = models.CharField(u'店铺SKU', max_length=255, blank=True, null=True)
    posted_date = models.DateTimeField(u'发布时间', blank=True, null=True)
    amazon_order_id = models.CharField(u'订单编号', max_length=64, blank=True, null=True)
    finance_type = models.CharField(u'交易类型', max_length=32, blank=True, null=True)
    marketplace_name = models.CharField(u'商城名称	', max_length=32, blank=True, null=True)
    quantity_shipped = models.CharField(u'数量', max_length=32, blank=True, null=True)
    order_adjustment_item_id = models.CharField(u'盘点商品编号', max_length=32, blank=True, null=True)
    order_item_id = models.CharField(u'订单商品编号', max_length=32, blank=True, null=True)
    fee_type = models.CharField(u'费用类型', max_length=32, blank=True, null=True)
    fee_currency = models.CharField(u'费用货币', max_length=32, blank=True, null=True)
    fee_amount = models.CharField(u'费用金额', max_length=32, blank=True, null=True)
    refresh_time = models.DateTimeField(u'刷新时间', blank=True, null=True)

    class Meta:
        verbose_name = u'AMZ交易信息'
        verbose_name_plural = verbose_name
        db_table = 't_amazon_finance_record'

    def __unicode__(self):
        return u'%s' % self.id
