# -*- coding: utf-8 -*-
from django.db import models
class t_report_week(models.Model):
    YearWeek       =   models.CharField(u'周编号',max_length=8,blank = True,null = True)
    StepID         =   models.CharField(u'步骤编号',max_length=4,blank = True,null = True)
    AllCount       =   models.IntegerField(u'总数',blank = True,null = True)
    SelfCount      =   models.IntegerField(u'自己总数',blank = True,null = True)
    Rank           =   models.IntegerField(u'排名',blank = True,null = True)
    StaffID        =   models.CharField(u'工号',max_length=16,blank = True,null = True)
    StaffName      =   models.CharField(u'用户名',max_length=16,blank = True,null = True)
    Avg            =   models.DecimalField(u'平均数',max_digits=7,decimal_places=2,null = True)
    Number         =   models.IntegerField(u'同岗位人数',max_length=16,blank = True,null = True)
    class Meta:
        verbose_name=u'按周统计信息'
        verbose_name_plural=verbose_name
        db_table = 't_report_week'
        ordering =  ['-YearWeek']
    def __unicode__(self):
        return u'%s %s'%(self.id,self.YearWeek)