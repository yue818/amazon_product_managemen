# -*-coding:utf-8-*-

"""
 @desc:
 @author: sunjian
 @site:
 @software: Sublime
 @file: t_templet_config_amazon_item_type_name.py
 @time: 2018/07/19 9:35
"""

from django.db import models


class t_templet_config_amazon_item_type_name(models.Model):
    site = models.CharField(u'站点', max_length=32, blank=True, null=True)
    product_type = models.CharField(u'刊登种类', max_length=255, blank=True, null=True)
    feed_product_type = models.CharField(u'商品种类', max_length=255, blank=True, null=True)
    item_type_name = models.TextField(u'item_type_name', blank=True, null=True)

    class Meta:
        app_label = 'skuapp'
        verbose_name = u't_templet_config_amazon_item_type_name'
        db_table = 't_templet_config_amazon_item_type_name'

    def __unicode__(self):
        return u'%s' % (self.id)
