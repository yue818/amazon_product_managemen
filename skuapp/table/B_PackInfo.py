# -*- coding: utf-8 -*-
from django.db import models
from public import *

#普源的包装表
class B_PackInfo(models.Model):
    #NID           =   models.IntegerField(u'NID',blank = True,primary_key=True)
    PackCode      =  models.CharField(u'包装代码',max_length=50,null = True)
    PackName      =  models.CharField(u'包装规格',max_length=50,null = True)
    CostPrice     =  models.DecimalField(u'价格(¥元)',max_digits=10,decimal_places=5,null = True)
    Used          =  models.PositiveSmallIntegerField(u'Used',blank = True,null = True)
    Remark        =  models.CharField(u'备注',max_length=200,null = True)
    Weight        =  models.DecimalField(u'重量(g)',max_digits=10,decimal_places=4,null = True)
    BarCode       =  models.CharField(u'BarCode',max_length=32,null = True)
    class Meta:
        verbose_name=u'普源包装规格配置表'
        verbose_name_plural=u'普源包装规格配置表'
        db_table = 'B_PackInfo'
        ordering =  ['PackName',]
    def __unicode__(self):
        return u'NID=%s 规格=%s 价格(¥元)=%s 重量(g)=%s'%(self.id,self.PackName,self.CostPrice,self.Weight)