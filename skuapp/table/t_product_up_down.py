# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models
from public import *
from django.utils.safestring import mark_safe
#12)    部门领用记录 t_product_depart_get
class t_product_up_down(models.Model):
    SKU             =   models.CharField(u'SKU',max_length=100,blank = True,null = True)
    Goods_Name      =   models.CharField(u'商品名称',max_length=32,blank = True,null = True)
    Goods_Status    =   models.CharField(u'商品状态',choices=getChoices(ChoiceGoodStatus),max_length=11)
    
    Request_man     =   models.CharField(u'申请人', max_length=30, blank=True, null=True)
    Request_date    =   models.DateField(u'申请时间', blank=True, null=True)
    
    Purchase_man    =   models.CharField(u'采购人员', max_length=30, blank=True, null=True)
    Producer        =   models.CharField(u'产品专员',max_length=30, blank=True, null=True)
    SupplierID      =   models.IntegerField(u'供应商ID',)
    Supplier        =   models.CharField(u'供应商',max_length=30, blank=True, null=True)
    Supplier_url    =   models.CharField(u'供应商采购链接',max_length=200, blank=True, null=True)
    Goodsbirth      =   models.CharField(u'产品创建时间',max_length=32,blank=True, null=True,)
    sum             =   models.IntegerField(u'累计临下次数',default=0,blank=True, null=True)
    #DealRecord      =   models.CharField(u'商品处理',choices=getChoices(PR),max_length=30, blank=True, null=True)
    Remark          =   models.TextField(u'备注',max_length=120,blank=True, null=True)
    Add_Date        =   models.DateField(u'截止日期',max_length=16)
    day_obj         =   models.IntegerField(u'天数',blank=True,null=True)
  
    MainSKU         =   models.CharField(u'MainSKU', max_length=30, blank=True, null=True)


    class Meta:
        verbose_name=u'临时上下架状态跟踪处理单'
        verbose_name_plural=u'临时上下架状态跟踪处理单'
        db_table = 't_product_up_down'
        ordering =  ['-id']
    def __unicode__(self):
        return u'id:%s'%(self.id)
