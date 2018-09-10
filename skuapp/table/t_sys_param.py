# -*- coding: utf-8 -*-
from django.db import models

class t_sys_param(models.Model):
    Type       =   models.IntegerField(u'参数类型',max_length=11,blank = True,null = True)
    TypeDesc   =   models.CharField(u'参数类型描述',max_length=32,blank = True,null = True)
    TypeName   =   models.CharField(u'参数类型名称',max_length=32,blank = True,null = True)
    Seq        =   models.IntegerField(u'参数序号',max_length=11,blank = True,null = True)
    V          =   models.CharField(u'参数值',max_length=32,blank = True,null = True)
    VDesc      =   models.CharField(u'参数值描述',max_length=32,blank = True,null = True)
    UpdateTime =   models.DateTimeField(u'更新时间',auto_now=True,blank = True,null = True)
    class Meta:
        verbose_name=u'系统参数配置'
        verbose_name_plural=u'系统参数配置'
        db_table = 't_sys_param'
        ordering =  ['Type','Seq']
    def __unicode__(self):
        return u'%s'%(self.id)


