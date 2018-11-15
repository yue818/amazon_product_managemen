# -*- coding: utf-8 -*-
from django.db import models

class t_config_mstsc_perm(models.Model):
    ShopName                =   models.CharField(u'店铺名称',max_length=32,blank = True,null = True)
    PermK                   =   models.CharField(u'权限描述(D:部门编号,S:员工编号)',max_length=8,blank = True,null = True)
    PermV                   =   models.CharField(u'权限值',max_length=32,blank = True,null = True) #D对应部门编号，S对应员工工号
    class Meta:
        verbose_name=u'远程桌面权限'
        verbose_name_plural=u'远程桌面权限'
        db_table = 't_config_mstsc_perm'
        ordering =  ['ShopName']
    def __unicode__(self):
        return u'%s'%(self.id)

