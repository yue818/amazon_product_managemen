# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models
from skuapp.table.t_cfg_category_info import *


class t_cfg_category_info(models.Model):
    id                         =   models.IntegerField(u'本级品类ID',primary_key=True)
    CategoryId                 =   models.IntegerField(u'上级品类ID',blank = True,null = True)
    CategoryName               =   models.CharField(u'品类名称',max_length=64,blank = True,null = True)

    class Meta:
        verbose_name=u'品类配置表'
        verbose_name_plural=u'品类配置表'
        db_table = 't_cfg_category_info'
        ordering =  ['id']
    def __unicode__(self):
        return u'id:%s'%(self.id)
