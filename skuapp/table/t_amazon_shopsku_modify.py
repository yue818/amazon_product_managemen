# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_shopsku_modify.py
 @time: 2018/8/23 17:21
"""  
from django.db import models


class t_amazon_shopsku_modify(models.Model):
    shop_name = models.CharField(u'店铺', max_length=32, blank=False, null=False)
    seller_sku = models.CharField(u'店铺SKU', max_length=255, blank=False, null=False)
    sku_modify = models.CharField(u'店铺SKU修正', max_length=255, blank=False, null=False)
    modify_reason = models.CharField(u'修正原因', max_length=255, blank=False, null=False)
    modify_user = models.CharField(u'修正人', max_length=32, blank=True, null=True)
    modify_time = models.DateTimeField(u'修正时间', blank=True, null=True)
    update_user = models.CharField(u'更新人', max_length=32, blank=True, null=True)
    update_time = models.DateTimeField(u'更新时间', blank=True, null=True)

    class Meta:
        verbose_name = u'AMZ店铺SKU关系修正'
        verbose_name_plural = verbose_name
        db_table = 't_amazon_shopsku_modify'

    def __unicode__(self):
        return u'%s' % self.id