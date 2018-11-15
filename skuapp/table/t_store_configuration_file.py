# -*- coding: utf-8 -*-
from django.db import models
from skuapp.table.public import *
        
        
class t_store_configuration_file(models.Model):
    ShopName            =   models.CharField(u'卖家简称',max_length=32,blank = True,null = True)
    Seller              =   models.CharField(u'店长/销售员',max_length=32,blank = True,null = True)
    Published           =   models.CharField(u'刊登员',max_length=32,blank = True,null = True)
    Operators           =   models.CharField(u'运营人员',max_length=32,blank = True,null = True)
    ShopType            =   models.CharField(u'店铺类型',max_length=10,blank = True,null = True)
    Submitter           =   models.CharField(u'提交人',max_length=32,blank = True,null = True)
    Department          =   models.CharField(u'部门',choices=getChoices(ChoiceDep),max_length=5,blank = True,null = True)
    RealName            =   models.CharField(u'店铺名',max_length=63,blank = True,null = True)
    ShopName_temp       =   models.CharField(u'ShopCode',max_length=63,blank = True,null = True)
    Status              =   models.CharField(u'店铺状态',choices=getChoices(ChoiceShopStatus),max_length=32,blank = True,null = True)
    PlatformID          =   models.CharField(u'平台名',max_length=32,blank = True,null = True)
    UpdateTime          =   models.DateTimeField(u'更新时间', auto_now=True, blank=True, null=True)

    
    class Meta:
        verbose_name=u'配置文件'
        verbose_name_plural=verbose_name
        db_table = 't_store_configuration_file'

    def __unicode__(self):
        return u'%s'%(self.id)
        
        
        