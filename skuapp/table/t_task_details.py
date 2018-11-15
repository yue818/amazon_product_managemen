# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models
from public import *
from skuapp.table.t_task_trunk import *

def gett_task_trunkChoices():
    return t_task_trunk.objects.values_list('Task_name_original','Task_name_original').order_by('Task_name_original')

class t_task_details(models.Model):
    Current_number           =   models.AutoField(u'当前任务号',max_length=12,primary_key=True, blank=False, null=False)
    Original_number          =   models.IntegerField(u'原始任务号',blank = True,null = True)
    Parent_number            =   models.IntegerField(u'父任务号',blank = True,null = True)
    Create_man               =   models.CharField(u'创建人', max_length=32, blank=True, null=True)
    Task_handler             =   models.CharField(u'处理人', max_length=32, blank=True, null=True)
    Task_name_original       =   models.CharField(u'原始任务名称',choices=gett_task_trunkChoices(),max_length=32, blank=True, null=True)
    Task_name_parent         =   models.CharField(u'父任务名称', max_length=32, blank=True, null=True)
    Task_name_current        =   models.CharField(u'当前任务名称', max_length=32, blank=True, null=True)
    Task_status              =   models.CharField(u'任务状态',choices=getChoices(ChoiceTaskOperation),max_length=32, blank=True, null=True)
    Create_time              =   models.DateField(u'创建时间', auto_now_add = True)
    Update_time              =   models.DateField(u'更新时间', auto_now = True )

    class Meta:
        verbose_name=u'任务详情'
        verbose_name_plural=u'任务详情'
        db_table = 't_task_details'
        ordering =  ['Current_number']
    def __unicode__(self):
        return u'Current_number:%s'%(self.Current_number)