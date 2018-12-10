# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_fba_inbound_address_cfg.py
 @time: 2018/12/10 10:05
"""  
from django.db import models


class t_amazon_fba_inbound_address_cfg(models.Model):
    shop_name = models.CharField(u'店铺', max_length=32, blank=True, null=True)
    country = models.CharField(u'国家', max_length=16, blank=True, null=True)
    province = models.CharField(u'省份', max_length=16, blank=True, null=True)
    city = models.CharField(u'城市', max_length=16, blank=True, null=True)
    name = models.CharField(u'地区', max_length=32, blank=True, null=True)
    postal_code = models.CharField(u'邮编', max_length=16, blank=True, null=True)
    address1 = models.CharField(u'详细地址1', max_length=255, blank=True, null=True)
    address2 = models.CharField(u'详细地址2', max_length=255, blank=True, null=True)
    insert_time = models.DateTimeField(u'添加时间', blank=True, null=True)
    insert_user = models.CharField(u'添加人', max_length=32, blank=True, null=True)
    update_time = models.DateTimeField(u'更新时间', blank=True, null=True)
    update_user = models.CharField(u'更新人', max_length=32, blank=True, null=True)

    class Meta:
        verbose_name = u'AMZ-FBA入库发货地址配置'
        verbose_name_plural = verbose_name
        db_table = 't_amazon_fba_inbound_address_cfg'

    def __unicode__(self):
        return u'%s' % self.id
