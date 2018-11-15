# -*- coding: utf-8 -*-
from django.db import models
class t_product_oplog(models.Model):
    id          =   models.AutoField(u'日志流水号',primary_key=True)
    MainSKU     =   models.CharField(u'主SKU',max_length=16,db_index = True,blank = True,null = True)
    Name        =   models.CharField(u'品名',max_length=64,blank = True,null = True)
    Name2       =   models.CharField((u'商品名称<br>(中文)'),max_length=32,null = True)
    OpID        =   models.CharField(u'用户名',max_length=16,db_index = True,blank = True,null = True)
    OpName      =   models.CharField(u'姓名',max_length=8,blank = True,null = True)
    StepID      =   models.CharField(u'步骤编号',max_length=4,blank = True,null = True)
    StepName    =   models.CharField(u'步骤名称',max_length=16,blank = True,null = True)
    BeginTime   =   models.DateTimeField(u'开始时间',blank = True,null = True)
    EndTime     =   models.DateTimeField(u'结束时间',blank = True,null = True)
    pid         =   models.IntegerField(u'业务流水号',db_index = True,blank = True,null = True)
    class Meta:
        verbose_name=u'操作记录'
        verbose_name_plural=u'操作记录'
        db_table = 't_product_oplog'
        ordering =  ['-BeginTime']
    def __unicode__(self):
        return u'%s: %s %s %s %s %s %s %s %s %s'%(self.id,self.MainSKU,self.Name2,self.OpID,self.OpName,self.StepID,self.StepName,self.BeginTime,self.EndTime,self.pid)