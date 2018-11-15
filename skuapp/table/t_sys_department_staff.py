# -*- coding: utf-8 -*-
from django.db import models
#部门员工对应关系表
class t_sys_department_staff(models.Model):
    DepartmentID   =   models.CharField(u'部门编号',max_length=10,null = True)
    StaffID        =   models.CharField(u'工号',max_length=20,null = True,unique= True)
    class Meta:
        verbose_name=u'员工表'
        verbose_name_plural=u'*员工表'
        db_table = 't_sys_department_staff'
        ordering =  ['DepartmentID']
    def __unicode__(self):
        return u'id =%d DepartmentID=%s  StaffID = %s'%(self.id, self.DepartmentID,self.StaffID)
