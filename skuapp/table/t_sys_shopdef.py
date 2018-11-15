# -*- coding: utf-8 -*-
from django.db import models
#店铺定义表
class t_sys_shopdef(models.Model):
    ShopID         =   models.CharField(u'店铺代码',max_length=32,null = True,db_index =True)
    ShopDesc       =   models.CharField(u'店铺描述',max_length=32,null = True)
    StaffID        =   models.CharField(u'店长工号',max_length=16,blank = True,null = True,db_index =True)
    ShopkeeperName =   models.CharField(u'店长姓名',max_length=16,blank = True,null = True)
    CreateTime     =   models.DateField(u'店铺创建时间',max_length=16,null = True)
    UpdateTime     =   models.DateTimeField(u'更新时间',auto_now=True,blank = True,null = True)
    class Meta:
        verbose_name=u'店铺定义表'
        verbose_name_plural=u'店铺定义表'
        db_table = 't_sys_shopdef'
        ordering =  ['ShopID',]
    def __unicode__(self):
        return u'%s %s %s'%(self.id,self.ShopID,self.ShopkeeperName)