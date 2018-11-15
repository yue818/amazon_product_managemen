# -*- coding: utf-8 -*-
from django.db import models
from public import *


class t_shopsku_information_binding(models.Model):
    SKU                 =   models.CharField(u'商品SKU',max_length=64,db_index = True,blank = True,null = True)
    ShopSKU             =   models.CharField(u'店铺SKU',max_length=64,blank = True,null = True)
    Memo                =   models.CharField(u'店铺名称',max_length=64,blank = True,null = True)
    PersonCode          =   models.CharField(u'店铺管理员',max_length=64,blank = True,null = True)
    Filename            =   models.FileField(u'文件名',blank = True,null = True)
    Submitter           =   models.CharField(u'提交人',max_length=31,blank = True,null = True)
    SubmitTime          =   models.DateTimeField(u'提交时间',blank = True,null = True)
    BindingStatus       =   models.CharField(u'状态',max_length=100,choices = getChoices(ChoiceBindingStatus),blank = True,null = True)

    class Meta:

        verbose_name=u'店铺SKU信息绑定'
        verbose_name_plural=verbose_name
        db_table = 't_shopsku_information_binding'

    def __unicode__(self):
        return u'%s'%(self.id)