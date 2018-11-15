# -*- coding: utf-8 -*-
from django.db import models
from public import *


class t_online_info_ebay_subsku(models.Model):
    itemid              =   models.CharField(u'产品标识ID',max_length=32,blank = True,null = True)
    subSKU              =   models.CharField(u'子SKU',max_length = 32,blank = True,null = True)
    title               =   models.TextField(u'标题',blank = True,null = True)
    startprice          =   models.FloatField(u'现在价格',max_length=12)
    total               =   models.IntegerField(u'产品总量',blank = True,null = True)
    sold                =   models.CharField(u'总销量',max_length=10,blank = True,null = True)
    title               =   models.CharField(u'子标题',max_length=150,blank = True,null = True)
    VariationSpecifics  =   models.TextField(u'变体属性',blank = True,null = True)
    picCodType          =   models.CharField(u'图片依据类型',max_length=32,blank = True,null = True)
    picType             =   models.CharField(u'变体图片类型',max_length=100,blank = True,null = True)
    VariationPictures   =   models.TextField(u'变体图',blank = True,null = True)
    productsku          =   models.CharField(u'商品SKU',max_length=256,blank = True,null = True)
    productstatus       =   models.CharField(u'商品状态',max_length=6,blank = True,null = True)
    UseNumber           =   models.IntegerField(u'可用数量',max_length=11,blank = True,null = True)
    SaleDay             =   models.DecimalField(u'可售天数', max_digits = 18, decimal_places = 2,blank = True,null = True)
    realavailable = models.IntegerField(u'库存', max_length=11, blank=True, null=True)
    profitrate = models.CharField(u'利润率', max_length=20, blank=True, null=True)


    class Meta:
        verbose_name=u'ebay子sku'
        verbose_name_plural=verbose_name
        db_table = 't_online_info_ebay_subsku'
    def __unicode__(self):
        return u'id:%s'%(self.id)