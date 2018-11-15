# -*- coding: utf-8 -*-
from django.db import models
from public import *
class t_old_used_shopcode(models.Model):
    shopcode_used       =   models.CharField(u'特征码',max_length=32,blank = True,null = True)
    platform            =   models.CharField(u'平台名',max_length=32,blank = True,null = True)
    class Meta:
        #app_label = 'pyapp'
        verbose_name=u'已使用特征码记录表'
        verbose_name_plural=verbose_name
        db_table = 't_old_used_shopcode'
        ordering =  ['-id']
    def __unicode__(self):
        return u'%s'%(self.id)