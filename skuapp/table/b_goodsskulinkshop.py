# -*- coding: utf-8 -*-
from django.db import models
from public import *
class b_goodsskulinkshop(models.Model):
    NID                 =   models.IntegerField(u'NID',blank = True,primary_key=True)
    SKU                 =   models.CharField(u'商品SKU',max_length=64,db_index = True,blank = True,null = True)
    ShopSKU             =   models.CharField(u'店铺SKU',max_length=64,db_index = True,blank = True,null = True)
    Memo                =   models.CharField(u'店铺名称',max_length=64,db_index = True,blank = True,null = True)
    PersonCode          =   models.CharField(u'店铺管理员',max_length=64,db_index = True,blank = True,null = True)
    class Meta:
        #app_label = 'pyapp'
        verbose_name=u'店铺SKU信息'
        verbose_name_plural=u'店铺SKU信息'
        db_table = 'b_goodsskulinkshop'
        ordering =  ['-NID']
    def __unicode__(self):
        return u'%s %s %s %s'%(self.SKU,self.ShopSKU,self.Memo,self.PersonCode)