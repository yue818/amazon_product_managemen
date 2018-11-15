# -*- coding: utf-8 -*-
from django.db import models
#15)    调研开发历史 t_product_survey_history
class t_product_survey_history(models.Model):
    SourcePicPath   =   models.CharField(u'调研图',max_length=100,blank = True,null = True)
    SourceURL       =   models.CharField(u'已调研URL',max_length=100,blank = True,null = True,db_index =True) #作为判断是否URL变化用
    SourcePicPath2  =   models.CharField(u'供货商图',max_length=100,blank = True,null = True)
    SupplierPUrl1   =   models.URLField(u'供货商商品URL一',null = True)
    UpdateTime      =   models.DateTimeField(u'更新时间',auto_now=True,blank = True,null = True)
    StaffID         =   models.CharField(u'工号',max_length=16,blank = True,null = True,db_index =True)
    StaffName       =   models.CharField(u'调研人',max_length=16,blank = True,null = True,db_index =True)
    pid             =   models.IntegerField(u'业务流水号',null = True,db_index =True)
    class Meta:
        verbose_name=u'调研开发历史'
        verbose_name_plural=u' 步骤15--调研开发历史'
        db_table = 't_product_survey_history'
        ordering =  ['-UpdateTime']
    def __unicode__(self):
        return u'%d - %s - %s'%(self.id,self.StaffID,self.SourceURL)
