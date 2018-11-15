# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models

class t_cfg_standard_small(models.Model):
    standard_id                =   models.IntegerField(u'规格id',blank = True,null = True)
    standard_small_code        =   models.CharField(u'小规格code',max_length=32,blank = True,null = True)
    standard_small_name        =   models.CharField(u'小规格名称',max_length=32,blank = True,null = True)
    standard_small_desc        =   models.TextField(u'小规格描述',blank = True,null = True)
    updatetime                 =   models.DateTimeField(u'更新时间',blank = True,null = True)

    class Meta:
        verbose_name=u'小规格类型配置表'
        verbose_name_plural=u'小规格类型配置表'
        db_table = 't_cfg_standard_small'
        ordering =  ['id']
    def __unicode__(self):
        return u'id:%s'%(self.id)
