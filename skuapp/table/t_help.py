# -*- coding: utf-8 -*-
from django.db import models
class t_help(models.Model):
    StepID            = models.CharField(u'步骤ID',max_length=32,blank = True,null=True)
    Stepdescription   = models.CharField(u'步骤描述',max_length=32,blank = True,null = True)
    HelpContent       = models.TextField(u'帮助内容',blank = True,null = True)

    class Meta:
        verbose_name=u'帮助信息'
        verbose_name_plural=u'帮助信息'
        db_table = 't_help'
        ordering =  ['-id']
    def __unicode__(self):
        return u'%s'%(self.id)
