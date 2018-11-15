# -*- coding: utf-8 -*-
from django.db import models
from public import *
import django.utils.timezone as timezone


class w_work_report(models.Model):
    ReportWeek = models.CharField(u'报告<br>周数', max_length=10, blank=True, null=False)
    ReportMan = models.CharField(u'报告人', max_length=20, blank=True, null=False)
    Department = models.CharField(u'部门', max_length=20, blank=True, null=True)
    ReportDate = models.DateField(u'填写日期',auto_now_add=True)
    LastWweekPlan = models.TextField(u'上周计划', max_length=512, blank=True, null=True)
    ThisWeekPlan = models.TextField(u'本周内容', max_length=512, blank=True, null=True)
    NextWeekPlan = models.TextField(u'下周计划', max_length=512, blank=True, null=True)
    WorkSummary = models.TextField(u'工作总结', max_length=512, blank=True, null=True)
    UnsolvedProblems = models.TextField(u'需反馈或解决的问题', max_length=512, blank=True, null=True)
    SolveTime = models.DateField(u'-解决时间-',max_length=16,blank = True,null = True)
    SolveMethod = models.TextField(u'解决办法', max_length=512, blank=True, null=True)
    AttachmentUrl1 = models.FileField(u'附件一', blank=True, null=True)
    AttachmentUrl2 = models.FileField(u'附件二', blank=True, null=True)


    class Meta:
        verbose_name=u'每周工作报告表'
        verbose_name_plural=u'每周工作报告表'
        db_table = 'w_work_report'
        ordering =  ['-ReportWeek','Department','-id']
    def __unicode__(self):
        return u'id:%s'%(self.id)