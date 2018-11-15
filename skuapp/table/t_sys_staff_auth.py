# -*- coding: utf-8 -*-
from django.db import models

class t_sys_staff_auth(models.Model):
    StaffID       =   models.CharField(u'用户名',max_length=20,blank = True,null = True)
    urltable   =   models.CharField(u'界面地址',max_length=64,blank = True,null = True)
    remark   =   models.CharField(u'备注',max_length=64,blank = True,null = True)
    class Meta:
        verbose_name=u'特殊权限配置'
        verbose_name_plural=u'特殊权限配置'
        db_table = 't_sys_staff_auth'
    def __unicode__(self):
        return u'%s'%(self.id)