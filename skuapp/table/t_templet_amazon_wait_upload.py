#-*-coding:utf-8-*-
from django.db import models
from .t_templet_amazon_base import *
from skuapp.table.t_config_shop_alias import *

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_templet_amazon_wait_upload.py
 @time: 2017/12/16 9:35
"""
def getSelect():
    return t_config_shop_alias.objects.values_list('ShopName','ShopName')

class t_templet_amazon_wait_upload(t_templet_amazon_base):
    ShopSets = models.CharField(u'待刊登店铺', max_length=200, choices=getSelect(), blank=True, null=True)
    class Meta:
        verbose_name = u'Amazon待刊登'
        verbose_name_plural = verbose_name
        db_table = 't_templet_amazon_wait_upload'
        ordering = ['-id']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)