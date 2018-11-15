# coding=utf-8
from django.db import models
from .t_templet_ebay_base import *

class t_ebay_product_image_modify(t_templet_ebay_base):

    class Meta:
        verbose_name = u'eBay采集箱'
        verbose_name_plural = verbose_name
        db_table = 't_templet_ebay_collection_box'
        ordering = ['-id']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)