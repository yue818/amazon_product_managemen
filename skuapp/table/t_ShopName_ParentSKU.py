# -*- coding: utf-8 -*-
from django.db import models


class t_ShopName_ParentSKU(models.Model):
    ShopName       = models.CharField(u'店铺简称',max_length=31,blank = True,null = True)
    ParentSKU      = models.CharField(u'ParentSKU',max_length=31,blank = True,null = True)
    
    class Meta:
        verbose_name=u'店铺名称与ParentSKU关联表'
        verbose_name_plural=verbose_name
        db_table = 't_ShopName_ParentSKU'
        ordering =  ['ShopName']
    def __unicode__(self):
        return u'%s'%(self.id)