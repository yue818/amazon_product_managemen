# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_config_amazon_ad_shop_status.py
 @time: 2018-05-17 16:36
"""  
from django.db import models


class t_config_amazon_ad_shop_status(models.Model):
    name = models.CharField(u'店铺全称', max_length=64, blank=True, null=True)
    shop_name = models.CharField(u'店铺名', max_length=32, blank=True, null=True)
    shop_site = models.CharField(u'站点', max_length=32, blank=True, null=True)
    IP = models.CharField(u'店铺IP', max_length=32, blank=True, null=True)
    uuid = models.CharField(u'更新批次信息', max_length=64, blank=True, null=True)
    synType = models.CharField(u'更新类型', max_length=32, blank=True, null=True)
    status = models.CharField(u'更新状态', max_length=32, blank=True, null=True)
    updatetime = models.DateTimeField(u'更新时间', blank=True, null=True)

    class Meta:
        verbose_name = u'AMAZON CPC广告店铺刷新状态'
        verbose_name_plural = verbose_name
        db_table = 't_config_amazon_ad_shop_status'

    def __unicode__(self):
        return u'%s' % self.id
