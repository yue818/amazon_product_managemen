# coding=utf-8
from django.db import models
from .t_templet_ebay_base import *

class t_templet_public_ebay(t_templet_ebay_base):
    UsedNum = models.IntegerField(u'使用次数', max_length=8, blank=True, null=True)

    class Meta:
        verbose_name = u'eBay公共模板'
        verbose_name_plural = verbose_name
        db_table = 't_templet_public_ebay'
        ordering = ['-id']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)