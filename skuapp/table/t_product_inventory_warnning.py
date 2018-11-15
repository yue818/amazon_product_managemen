# -*- coding: utf-8 -*-
from django.db import models
from public import *

class t_product_inventory_warnning(models.Model):
    image_url           =   models.URLField(u'image_url',max_length=128,blank = True,null = True)
    MainSKU                 =   models.CharField(u'主sku',max_length=16,blank = True,null = True)
    Status                      =   models.CharField(u'商品状态',max_length=32,blank = True,null = True)
    ProductName         =   models.CharField(u'商品名称',max_length=64,blank = True,null = True)
    SalerName           =   models.CharField(u'业绩归属人2',max_length=32,blank = True,null = True)
    SalerName1          =   models.CharField(u'业绩归属人1',max_length=32,blank = True,null = True)
    Purchaser           =   models.CharField(u'采购员',max_length=255,blank = True,null = True)
    order7daysAll       =   models.CharField(u'7天销量',max_length=16,blank = True,null = True)
    order15daysAll      =   models.CharField(u'15天销量',max_length=16,blank = True,null = True)
    order30daysAll      =   models.CharField(u'30天销量',max_length=16,blank = True,null = True)
    AllAvailableNumber  =   models.CharField(u'可用数量',max_length=16,blank = True,null = True)
    CreateTime          =   models.DateTimeField(u'商品创建时间',blank = True,null = True)
    ItemUrl             =   models.URLField(u'网址6',max_length=16,blank = True,null = True)
    UnitPrice           =   models.CharField(u'商品成本单价',max_length=16,blank = True,null = True)
    Weight              =   models.CharField(u'商品重量',max_length=16,blank = True,null = True)
    Money               =   models.DecimalField(u'库存金额',max_digits = 10, decimal_places = 2,blank = True,null = True)
    radio               =   models.DecimalField(u'突变系数',max_digits = 10, decimal_places = 4,blank = True,null = True)
    HandleTime          =   models.DateTimeField(u'处理时间',blank = True,null = True,auto_now=True)
    HandleResults       =   models.CharField(u'处理状态',choices=getChoices(ChoiceHandleStatus),max_length=16,blank = True,null = True)
    tortinfo            =   models.CharField(u'侵权站点',max_length=16,blank = True,null = True)
    Remark1             =   models.TextField(u'处理结果1',max_length=255,blank = True,null = True)
    Remark2             =   models.TextField(u'处理结果2',max_length=255,blank = True,null = True)
    firstWarnningTime   =   models.DateTimeField(u'首次预警',blank = True,null = True,auto_now=True)
    CategoryCode        =   models.CharField(u'商品类型',choices=getChoices(ChoiceLargeCategory),max_length=16,blank = True,null = True)
    AllMoney            =   models.DecimalField(u'销售总金额',max_digits = 10, decimal_places = 2,blank = True,null = True)
    Number              =   models.IntegerField(u'库存数量',max_length=8,blank = True,null = True)
    SaleDate            =   models.DecimalField(u'可售天数',max_digits = 10, decimal_places = 1,blank = True,null = True)
    SupperName          =   models.CharField(u'供应商名称',max_length=16,blank = True,null = True)
    storeName           =   models.CharField(u'仓库',max_length=16,blank = True,null = True)
    insertTime          =   models.DateTimeField(u'数据同步时间',blank = True,null = True)
    HandleMan           =   models.CharField(u'处理人',max_length=16,blank = True,null = True)
    CostPrice           =   models.DecimalField(u'商品成本金额',max_digits = 10, decimal_places = 1,blank = True,null = True)
    class Meta:
        verbose_name=u'库存预警'
        verbose_name_plural=u'库存预警'
        db_table = 't_product_inventory_warnning_mainsku'
        ordering =  ['-order7daysAll']
    def __unicode__(self):
        return u'%s'%(self.id)