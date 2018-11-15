# -*- coding: utf-8 -*-
"""
 @desc:
 @author: wangzhiyang
 @site:
 @software: PyCharm
 @file: t_saler_profit_config.py
 @time: 2018/8/29 8:53
"""
from django.db import models

class t_saler_profit_config(models.Model):
    id = models.AutoField(u'业务流水号', primary_key=True)
    Department = models.CharField(u'部门', max_length=64, blank=True, null=True)
    PlatformName = models.CharField(u'平台名称', max_length=128, blank=True, null=True)
    ShopName = models.CharField(u'店铺名称', max_length=256, blank=True, null=True)
    SalerName = models.CharField(u'业绩归属人', max_length=256, blank=True, null=True)
    StatisticsMonth = models.CharField(u'统计月份', max_length=20, blank=True, null=True)
    ImportMan = models.CharField(u'导入人', max_length=32, blank=True, null=True)
    ImportTime = models.DateTimeField(u'导入时间', blank=True, null=True)
    
    class Meta:
        verbose_name=u'月销售员信息表'
        verbose_name_plural=verbose_name
        db_table = 't_saler_profit_config'
        ordering =  ['-id']
    def __unicode__(self):
        return u'id:%s'%(self.id)