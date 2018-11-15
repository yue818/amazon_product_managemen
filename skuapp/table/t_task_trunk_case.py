# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models
from public import *
from django.contrib.auth.models import User


class t_task_trunk_case(models.Model):
    Test_sight                      =   models.TextField(u'测试场景', blank=True, null=True)
    Test_case                       =   models.TextField(u'测试用例',blank=True, null=True)
    Test_hope_result                =   models.CharField(u'测试期望结果',max_length=225)
    Test_result                     =   models.CharField(u'测试结果', max_length=225)
    Test_developer                  =   models.CharField(u'开发人',max_length=225,blank = True,null = True)
    Test_verifier                   =   models.CharField(u'测试验证人', max_length=225,blank = True,null = True)
    Test_verifier_time              =   models.DateField(u'测试验证时间',blank = True,null = True)
    Original_number                 =   models.IntegerField(u'任务号',max_length=11,blank=True,null=True)


    class Meta:
        verbose_name=u'任务处理测试用例'
        verbose_name_plural=u'任务处理测试用例'
        db_table = 't_task_trunk_case'
        ordering =  ['id']
    def __unicode__(self):
        return u'id:%s'%(self.id)