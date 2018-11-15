# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models
from public import *
from django.utils.safestring import mark_safe

class t_sensitive_sku_info(models.Model):
    sensitive_sku           =   models.CharField(u'敏感SKU',max_length=100,blank = True,null = True)
    Input_man               =   models.CharField(u'信息录入员',max_length=100,blank = True,null = True)
    Input_time              =   models.DateTimeField(u'录入时间',blank = True,null = True)

    class Meta:
        verbose_name=u'敏感SKU信息录入表'
        verbose_name_plural=u'敏感SKU信息录入表'
        db_table = 't_sensitive_sku_info'
        ordering =  ['-id']
    def __unicode__(self):
        return u'id:%s'%(self.id)
