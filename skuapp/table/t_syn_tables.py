# -*- coding: utf-8 -*-
from django.db import models
class t_syn_tables(models.Model):
    TableName      =   models.CharField(u'表名',max_length=32,blank = True,null = True)
    AllCount       =   models.IntegerField(u'总数',blank = True,null = True)
    BeginTime      =   models.DateTimeField(u'开始时间',blank = True,null = True)
    EndTime        =   models.DateTimeField(u'结束时间',blank = True,null = True)
    class Meta:
        verbose_name = u'同步配置信息'
        verbose_name_plural = u'同步配置信息'
        db_table = 't_syn_tables'
    def __unicode__(self):
        return u'%s %s'%(self.id,self.TableName)