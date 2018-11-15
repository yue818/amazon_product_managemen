# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models

class t_cfg_standard_large_small(models.Model):
    standard_large_code        =   models.CharField(u'大规格code',max_length=32,blank = True,null = True)
    standard_small_code        =   models.CharField(u'小规格code',max_length=32,blank = True,null = True)
    standard_id                =   models.CharField(u'standard_id', max_length=32, blank = True,null = True)
    CURRENCYCODE               =   models.CharField(u'货币code',max_length=32,blank = True,null = True)
    getprice                   =   models.TextField(u'价格表达式',blank = True,null = True)
    getprice_desc              =   models.TextField(u'价格描述',blank = True,null = True)
    updatetime                 =   models.DateTimeField(u'更新时间',blank = True,null = True)

    class Meta:
        verbose_name=u'规格类型对应表'
        verbose_name_plural=u'规格类型对应表'
        db_table = 't_cfg_standard_large_small'
        ordering =  ['id']
    def __unicode__(self):
        return u'id:%s'%(self.id)
