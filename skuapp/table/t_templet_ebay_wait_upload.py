# coding=utf-8

from django.db import models
from .t_templet_ebay_base import t_templet_ebay_base


class t_templet_ebay_wait_upload(t_templet_ebay_base):
    ShopSets = models.TextField(u'待铺货店铺', blank=True, null=True)
    TimePlan = models.TextField(u'时间计划JSON', blank=True, null=True)
    ShippingTempID = models.IntegerField(u'运费模板ID', blank=True, null=True)

    class Meta:
        verbose_name = u'eBay待铺货'
        verbose_name_plural = verbose_name
        db_table = 't_templet_ebay_wait_upload'
        ordering = ['-id']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)
