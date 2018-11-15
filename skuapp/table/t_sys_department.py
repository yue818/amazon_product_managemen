# -*- coding: utf-8 -*-
from django.db import models
#部门表
class t_sys_department(models.Model):
    DepartmentID      =   models.CharField(u'部门编号',max_length=10,null = True)
    DepartmentName    =   models.CharField(u'部门名称',max_length=20,unique= True,null = True)
    class Meta:
        verbose_name=u'部门表'
        verbose_name_plural=u'*部门表'
        db_table = 't_sys_department'
        ordering =  ['DepartmentID']
    def __unicode__(self):
        return u'id =%d DepartmentName=%s '%(self.id, self.DepartmentName)
