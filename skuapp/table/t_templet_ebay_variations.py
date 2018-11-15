# -*- coding: utf-8 -*-

from django.db import models
from django.utils.safestring import mark_safe


class t_templet_ebay_variations(models.Model):
    variationSku = models.CharField(u'多属性SKU', max_length=64, blank=True, null=True)
    startPrice = models.FloatField(u'起始价格',blank = True,null = True)
    quantity = models.PositiveSmallIntegerField(u'数量',blank = True,null = True)
    variationSpecifics = models.TextField(u'variationSpecifics', blank=True, null=True)
    templetID = models.PositiveSmallIntegerField(u'templetID',blank = True,null = True)

    class Meta:
        verbose_name = u'eBay商品属性表'
        verbose_name_plural = verbose_name
        db_table = 't_templet_ebay_variations'
        ordering = ['-id']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)