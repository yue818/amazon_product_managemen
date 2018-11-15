# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models
from public import *
from django.contrib.auth.models import User
    


class t_task_operation_log(models.Model):
    Original_number          =   models.IntegerField(u'任务号',blank=True, null=True)
    Flow_way_status          =   models.CharField(u'任务流向',max_length=32,blank=True,null=True)
    Flow_handle_result       =   models.CharField(u'处理结果',max_length=32,blank=True,null=True)
    Flow_handle_remark       =   models.TextField(u'处理备注',blank=True,null=True)
    Flow_handle_man          =   models.CharField(u'处理人',max_length=32,blank=True,null=True)
    Flow_handle_time         =   models.DateTimeField(u'处理时间',blank=True,null=True)
                             

    class Meta:
        verbose_name=u'任务操作日志'
        verbose_name_plural=u'任务操作日志'
        db_table = 't_task_operation_log'
        ordering =  ['-id']
    def __unicode__(self):
        return u'Original_number:%s'%(self.id)