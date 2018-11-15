# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.safestring import mark_safe
# Create your models here.
def getDepartmentID():
    return t_sys_department.objects.values_list('DepartmentID','DepartmentName').all().order_by('id') 
class t_config_mstsc_log(models.Model):
    ShopName                =   models.CharField(u'店铺名称',max_length=32,blank = True,null = True)
    UserName                =   models.CharField(u'用户名',max_length=32,blank = True,null = True)
    FirstName               =   models.CharField(u'中文名',max_length=32,blank = True,null = True) #D对应部门编号，S对应员工工号
    LoginInTime             =   models.DateTimeField(u'登入时间',max_length=32,blank = True,null = True)
    LoginOutTime            =   models.DateTimeField(u'退出时间',max_length=32,blank = True,null = True)
    LastAnswerTime          =   models.DateTimeField(u'刷新时间',max_length=32,blank = True,null = True)
    QuitReason              =   models.CharField(u'状态',max_length=32,blank = True,null = True)
    class Meta:
        verbose_name=u'远程桌面登录日志'
        verbose_name_plural=u'远程桌面登录日志'
        db_table = 't_config_mstsc_log'
        ordering =  ['ShopName']
    def __unicode__(self):
        return u'%s'%(self.id)