# -*- coding: utf-8 -*-

from django.db import models
from django.utils.safestring import mark_safe

class t_templet_ebay_pic_set(models.Model):
    assoc_pic_key = models.CharField(u'多属性依据名', max_length=32, blank=True, null=True)
    assoc_pic_url = models.CharField(u'图片', max_length=255, blank=True, null=True)
    assoc_pic_value = models.CharField(u'多属性依据值', max_length=64, blank=True, null=True)

    class Meta:
        verbose_name = u'eBay商品属性图片表'
        verbose_name_plural = verbose_name
        db_table = 't_templet_ebay_pic_set'
        ordering = ['-id']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)