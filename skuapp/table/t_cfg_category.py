# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models

class t_cfg_category(models.Model):
    category_id                =   models.IntegerField(u'品类外键ID',blank = True,null = True)
    category_code              =   models.CharField(u'品类code',max_length=32,blank = True,null = True)
    category_name              =   models.CharField(u'品类名称',max_length=32,blank = True,null = True)
    logisticwaycode            =   models.TextField(u'物流方式code',blank = True,null = True)
    logisticwaycode_desc       =   models.TextField(u'物流方式描述',blank = True,null = True)
    updatetime                 =   models.DateTimeField(u'更新时间',blank = True,null = True)

    class Meta:
        verbose_name=u'品类配置表'
        verbose_name_plural=u'品类配置表'
        db_table = 't_cfg_category'
        ordering =  ['id']
    def __unicode__(self):
        return u'id:%s'%(self.id)
