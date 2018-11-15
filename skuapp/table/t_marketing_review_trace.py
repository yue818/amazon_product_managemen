# -*- coding: utf-8 -*-
"""
 @desc:joom营销留评效果跟踪，填写的店铺和sku以及产品id，刊登时间、营销时间、留评时间，几个要素，读出自刊登日后的日销量情况，并标注营销时间和留评时间
 @author: wangzhiyang
 @site:
 @software: PyCharm
 @file: t_marketing_revied_trace.py
 @time: 2018/5/29 8:53
"""
from django.db import models
from public import *
from skuapp.table.t_store_configuration_file import t_store_configuration_file

def getShopName():
    objs = t_store_configuration_file.objects.filter(ShopName__startswith='JOOM-').values_list('ShopName',flat=True)
    sArray = []
    for obj in objs:
        stmp = (obj, obj)
        sArray.append(stmp)
        del stmp
    return tuple(sArray)

class t_marketing_review_trace(models.Model):
    Id              = models.AutoField(u'业务流水号',primary_key=True)
    SKU             = models.CharField(u'SKU',max_length=32,blank = False,null = False)
    ProductID       = models.CharField(u'产品ID',max_length=128,blank = False,null = False)
    ShopName        = models.CharField(u'普源店铺名称',max_length=255,blank = False,null = False)
    DYDate          = models.DateField(u'调研日期',blank = False,null = False)
    PublishDate     = models.DateField(u'刊登日期',blank = False,null = False)
    EnKeys          = models.CharField(u'英文关键词', max_length=255, blank=True, null=True)
    ZeroProfitPrice = models.DecimalField(u'零利润价格',max_digits=6,decimal_places=2,blank = True,null = True)
    PrePrice        = models.DecimalField(u'初步定价',max_digits=6,decimal_places=2,blank = False,null = False)
    MaxPrePrice     = models.DecimalField(u'初步定价最大值', max_digits=6, decimal_places=2, blank=False, null=False)
    CurrentPrice    = models.DecimalField(u'当前售价', max_digits=6, decimal_places=2, blank=True, null=True)
    ProfitPrice     = models.CharField(u'利润率',max_length=64,blank=True,null = True)
    ReverseLink     = models.URLField(u'反向链接',blank = True,null = True)
    OpPrice         = models.CharField(u'对手价格',max_length=64, blank=True, null=True)
    OpProfitPrice    = models.CharField(u'对手利润率',max_length=64, blank=True, null=True)
    GroundTime      = models.DateTimeField(u'对手上架时间',blank = True,null = True)
    MarketingTime   = models.DateField(u'营销时间',blank = True,null = True)
    ReviewTime      = models.DateField(u'留评时间',blank = True,null = True)
    LRStaff         = models.CharField(u'录入人员', max_length=64, blank=True, null=True)
    LRTime          = models.DateTimeField(u'录入时间',blank = True,null = True)
    SKUType         = models.CharField(u'SKU类型',max_length=16,choices=getChoices(ChoiceApplyType),default='mainsku',blank = False,null = False)


    class Meta:
        verbose_name=u'营销留评跟踪'
        verbose_name_plural=verbose_name
        db_table = 't_marketing_review_trace'
        ordering = ['-LRTime']
    def __unicode__(self):
        return u'Id:%s'%(self.Id)