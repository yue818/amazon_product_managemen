# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_fba_inbound_plan.py
 @time: 2018/12/10 13:50
"""  
from django.db import models


class t_amazon_fba_inbound_plan(models.Model):
    shop_name = models.CharField(u'店铺', max_length=32, blank=True, null=True)
    shop_site = models.CharField(u'站点', max_length=8, blank=True, null=True)
    seller_sku = models.CharField(u'店铺SKU', max_length=255, blank=True, null=True)
    quantity = models.IntegerField(u'入库数量', max_length=5, blank=True, null=True)
    insert_time = models.DateTimeField(u'添加时间', blank=True, null=True)
    insert_user = models.CharField(u'添加人', max_length=32, blank=True, null=True)
    status = models.CharField(u'状态', max_length=10, blank=True, null=True)
    update_time = models.DateTimeField(u'更新时间', blank=True, null=True)
    update_user = models.CharField(u'更新人', max_length=32, blank=True, null=True)

    class Meta:
        verbose_name = u'AMZ-FBA入库计划'
        verbose_name_plural = verbose_name
        db_table = 't_amazon_fba_inbound_plan'

    def __unicode__(self):
        return u'%s' % self.id
