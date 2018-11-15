# -*- coding: utf-8 -*-
from django.db import models
from public import *
from t_store_configuration_file import *

class t_use_productsku_apply_for_shopsku(models.Model):
    ShopName   = models.CharField(u'卖家简称',max_length=64,blank = True,null = True)
    ApplyType  = models.CharField(u'申请类型',choices=getChoices(ChoiceApplyType),max_length=16,blank = True,null = True)
    InputText  = models.TextField(u'输入框',blank = True,null = True)
    ProductSKU = models.CharField(u'商品SKU',max_length=16,blank = True,null = True)
    ShopSKU    = models.CharField(u'店铺SKU',max_length=32,blank = True,null = True)
    Applicant  = models.CharField(u'申请人',max_length=32,blank = True,null = True)
    ApplyTime  = models.DateTimeField(u'申请时间',blank = True,null = True)
    BStatus    = models.CharField(u'确认绑定状态',choices=getChoices(ChoiceBStatus),max_length=32,blank = True,null = True)
    EStatus    = models.CharField(u'导出状态',choices=getChoices(ChoiceEStatus),max_length=32,blank = True,null = True)
    MainSKU    = models.CharField(u'主SKU',max_length=32,blank = True,null = True)

    class Meta:
        verbose_name=u'店铺SKU申请'
        verbose_name_plural=verbose_name
        db_table = 't_use_productsku_apply_for_shopsku'
        ordering = ['-id']
        
    def __unicode__(self):
        return u'%s'%(self.id)