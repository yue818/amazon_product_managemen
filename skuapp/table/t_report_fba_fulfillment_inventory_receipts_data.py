# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_report_fba_fulfillment_inventory_receipts_data.py
 @time: 2018-05-30 15:24
"""  

from django.db import models


class t_report_fba_fulfillment_inventory_receipts_data(models.Model):
    received_date = models.DateTimeField(u'接受日期', blank=True, null=True)
    fnsku = models.CharField(u'fnsku', max_length=128, blank=True, null=True)
    sku = models.CharField(u'sku', max_length=128, blank=True, null=True)
    product_name = models.CharField(u'product_name', max_length=512, blank=True, null=True)
    quantity = models.CharField(u'quantity', max_length=32, blank=True, null=True)
    fba_shipment_id = models.CharField(u'fba_shipment_id', max_length=32, blank=True, null=True)
    fulfillment_center_id = models.CharField(u'fulfillment_center_id', max_length=32, blank=True, null=True)
    refresh_date = models.DateTimeField(u'刷新日期', blank=True, null=True)
    shop_name = models.CharField(u'shop_name', max_length=64, blank=True, null=True)

    class Meta:
        verbose_name = u'AMAZON 已接受库存'
        verbose_name_plural = verbose_name
        db_table = 't_report_fba_fulfillment_inventory_receipts_data'

    def __unicode__(self):
        return u'%s' % self.id
