# -*- coding: utf-8 -*-
from django.db import models
from public import *


class t_config_apiurl_asin_operation(models.Model):
    OperationMan    = models.CharField(u'操作人', max_length=20, blank=True, null=False)
    Developed       = models.IntegerField(u'已开发', max_length=20, blank=True, null=True)
    Repeation       = models.IntegerField(u'重复', max_length=20, blank=True, null=True)
    Handled         = models.IntegerField(u'已处理', max_length=20, blank=True, null=True)
    OperationWeek   = models.CharField(u'处理周数', max_length=20, blank=True, null=True)


    class Meta:
        verbose_name=u'Amazon榜单操作记录'
        verbose_name_plural=u'Amazon榜单操作记录'
        db_table = 't_config_apiurl_asin_operation'
        ordering =  ['-OperationWeek',]
    def __unicode__(self):
        return u'id:%s'%(self.id)