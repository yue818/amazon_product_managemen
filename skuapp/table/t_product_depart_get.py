# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models
#12)    部门领用记录 t_product_depart_get
class t_product_depart_get(t_base):
    StaffName      =   models.CharField(u'领用人名称',max_length=16,blank = True,null = True)
    SalesAttr      =   models.CharField(u'销售归属人',max_length=16,blank = True,null = True)
    LYTime         =   models.DateTimeField(u'领用时间',blank = True,null = True)
    PublishedInfo  =   models.TextField(u'刊登信息',blank = True,null = True)
    PublishedA     =   models.CharField(u'刊登链接',max_length=255,null = True)
    DepartmentID   =   models.CharField(u'领用部门编号',max_length=10,null = True)
    pid            =   models.IntegerField(u'业务流水号',null = True,db_index =True)
    class Meta:
        verbose_name=u'本部门领用记录'
        verbose_name_plural=u' 步骤12--本部门领用记录'
        db_table = 't_product_depart_get'
        ordering =  ['-id']
    def __unicode__(self):
        return u'id:%s MainSKU:%s'%(self.id,self.MainSKU)
