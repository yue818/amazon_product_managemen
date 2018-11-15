# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models

class t_cfg_standard_large(models.Model):
    standard_id                =   models.IntegerField(u'规格id',blank = True,null = True)
    standard_large_code        =   models.CharField(u'大规格code',max_length=32,blank = True,null = True)
    standard_large_name        =   models.CharField(u'大规格名称',max_length=32,blank = True,null = True)
    standard_large_desc        =   models.TextField(u'大规格描述',blank = True,null = True)
    updatetime                 =   models.DateTimeField(u'更新时间',blank = True,null = True)

    class Meta:
        verbose_name=u'大规格类型配置表'
        verbose_name_plural=u'大规格类型配置表'
        db_table = 't_cfg_standard_large'
        ordering =  ['id']
    def __unicode__(self):
        return u'id:%s'%(self.id)
