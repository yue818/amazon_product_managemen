# -*- coding: utf-8 -*-
from django.db import models
from django.utils.safestring import mark_safe
from skuapp.table.public import *

class t_product_mainsku_sku(models.Model):
    MainSKU    =   models.CharField(u'主SKU',db_index = True,max_length=32,blank = True,null = True)
    SKU        =   models.CharField(u'子SKU',db_index = True,max_length=32,blank = True,null = True)
    SKUATTRS   =   models.CharField(u'商品SKU属性',max_length=200,blank = True,null = True)
    UnitPrice  =   models.DecimalField(u'产品价(¥元)',max_digits=7,decimal_places=2,blank = True,null = True)
    Weight     =   models.PositiveSmallIntegerField(u'产品重量(g)',blank = True,null = True)
    PackNID    =   models.CharField(u'包装NID',max_length=50,null = True)
    MinPackNum =   models.PositiveSmallIntegerField(mark_safe(u'最小包<br>装数量'),default = 1,blank = True,null = True)
    DressInfo  =   models.CharField(u'服装类信息',max_length=200,blank = True,null = True)
    pid        =   models.IntegerField(u'业务流水号',blank = True,null = True)
    ProductSKU =   models.CharField(u'商品SKU',max_length=63,blank = True,null = True)
    SupplierLink =   models.CharField(u'供应商链接',max_length=255,blank = True,null = True)
    SupplierNum  =   models.CharField(u'供应商货号',max_length=128,blank = True,null = True)
    HasOssImage = models.IntegerField(u'是否有图', blank=True, null=True)
 
    class Meta:
        verbose_name=u'主SKU子SKU对应表'
        verbose_name_plural=u'主SKU子SKU对应表'
        db_table = 't_product_mainsku_sku'
        ordering =  ['MainSKU','SKU',]
    def __unicode__(self):
        return u'%s MainSKU=%s SKU=%s SKUATTRS=%s UnitPrice=%s Weight=%s pid=%s'%(self.id,self.MainSKU,self.SKU,self.SKUATTRS,self.UnitPrice,self.Weight,self.pid)