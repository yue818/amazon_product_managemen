# -*- coding: utf-8 -*-
from django.db import models
from public import *


class t_all_plateform_code_shopname(models.Model):
    TypeNum   = models.CharField(u'类似',max_length=16,blank = True,null = True)
    Length    = models.CharField(u'Code长度',max_length=16,blank = True,null = True)
    Plateform  = models.CharField(u'平台',max_length=16,blank = True,null = True)
    ShopName   = models.CharField(u'卖家简称',max_length=64,blank = True,null = True)
    Code       = models.CharField(u'特殊码',max_length=32,blank = True,null = True)
    InitialNum  = models.IntegerField(u'原始值',max_length=32,blank = True,null = True)
    CurrentNum  = models.IntegerField(u'当前值',max_length=32,blank = True,null = True)

    class Meta:
        verbose_name=u'全平台店铺SKU编码'
        verbose_name_plural=verbose_name
        db_table = 't_all_plateform_code_shopname'
        ordering = ['-id']
        
    def __unicode__(self):
        return u'%s'%(self.id)