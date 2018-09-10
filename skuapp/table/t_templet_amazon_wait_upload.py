#-*-coding:utf-8-*-
from django.db import models
from .t_templet_amazon_base import *

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_templet_amazon_wait_upload.py
 @time: 2017/12/16 9:35
"""
class t_templet_amazon_wait_upload(t_templet_amazon_base):
    ShopSets = models.TextField(u'待铺货店铺', blank=True, null=True)

    class Meta:
        verbose_name = u'Amazon定时铺货'
        verbose_name_plural = verbose_name
        db_table = 't_templet_amazon_wait_upload'
        ordering = ['-id']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)