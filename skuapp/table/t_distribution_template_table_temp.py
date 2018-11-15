# coding=utf-8
from django.db import models
from public import *

class t_distribution_template_table_temp(models.Model):
    NID             = models.IntegerField(u'铺货ID',max_length=11)
    ProductID       = models.CharField(u'产品ID', max_length=32, blank=True, null=True)
    ShopName        = models.CharField(u'目标店铺名称', max_length=32, blank=True, null=True)
    SKU             = models.CharField(u'商品SKU', max_length=32, blank=True, null=True)
    ShopSKU         = models.CharField(u'店铺SKU', max_length=32, blank=True, null=True)
    Status          = models.CharField(u'Status',choices=getChoices(ChoiceStatus_wish),max_length=32,blank = True,null = True)
    Price           = models.DecimalField(u'价格', max_digits=6, decimal_places=2, null=True)
    oldPrice        = models.DecimalField(u'原价格', max_digits=6, decimal_places=2, null=True)
    Quantity        = models.IntegerField(u'数量', max_length=11, blank=True, null=True)
    msrp            = models.DecimalField(u'标签价', max_digits=6, decimal_places=2, null=True)
    Color           = models.CharField(u'颜色', max_length=32, blank=True, null=True)
    Size            = models.CharField(u'尺寸', max_length=32, blank=True, null=True)
    Shipping        = models.DecimalField(u'运费', max_digits=6, decimal_places=2, null=True)
    ShippingTime    = models.CharField(u'运输时间', max_length=32, blank=True, null=True)
    ImageSKU        = models.CharField(u'子SKU图片', max_length=200, blank=True, null=True)
    ParentSKU       = models.CharField(u'父SKU', max_length=32, blank=True, null=True)
    VariationImage  = models.CharField(u'变种图', max_length=200, blank=True, null=True)
    DeleteFlag      =   models.CharField(u'待删除标识',max_length=5,blank=True,null=True)
    TemplateCreator   =  models.CharField(u'模版提交人', max_length=32, blank=True, null=True)
    TemplateCreatTime =  models.DateTimeField(u'模版提交时间', blank=True, null=True)
    TemplateModifier  =  models.CharField(u'模版修改人', max_length=32, blank=True, null=True)
    TemplateModifyTime=  models.DateTimeField(u'模版修改时间', blank=True, null=True)

    class Meta:
        verbose_name=u'模版TEMP'
        verbose_name_plural=verbose_name
        db_table = 't_distribution_template_table_temp'
        ordering =  ['-id']
    def __unicode__(self):
        return u'%s'%(self.id)