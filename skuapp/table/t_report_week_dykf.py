# -*- coding: utf-8 -*-
from django.db import models
from t_report_week import t_report_week
class t_report_week_dykf(t_report_week):
    class Meta:
        verbose_name=u'调研开发报表统计'
        verbose_name_plural=verbose_name
        ordering =  ['-YearWeek']
        proxy = True
    def __unicode__(self):
        return u'%s %s'%(self.YearWeek)
