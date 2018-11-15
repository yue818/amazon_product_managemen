# -*- coding: utf-8 -*-
from django.db import models
from public import *
import django.utils.timezone as timezone


class d_work_report(models.Model):
    ReportMan = models.CharField(u'报告人', max_length=20, blank=True, null=False)
    Department = models.CharField(u'部门', max_length=20, blank=True, null=True)
    ReportDateDay = models.DateField(u'报告日期',default=timezone.now)
    JobContent = models.TextField(u'工作内容', max_length=512, blank=True, null=True)
    MeetProblem = models.TextField(u'遇到的问题', max_length=512, blank=True, null=True)
    Harvest = models.TextField(u'建议与收获', max_length=512, blank=True, null=True)
    Others = models.TextField(u'其他', max_length=512, blank=True, null=True)


    class Meta:
        verbose_name=u'每日工作报告表'
        verbose_name_plural=u'每日工作报告表'
        db_table = 'd_work_report'
        ordering =  ['-ReportDateDay','Department']
    def __unicode__(self):
        return u'id:%s'%(self.id)