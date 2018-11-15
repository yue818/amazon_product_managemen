# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models

class t_cfg_b_logisticway(models.Model):
    code             =   models.CharField(u'物流方式编号',max_length=10,blank = True,null = True)
    name             =   models.CharField(u'物流方式名称',max_length=16,blank = True,null = True)
    Discount         =   models.IntegerField(u'折扣',blank = True,null = True)
    updatetime       =   models.DateTimeField(u'更新时间',auto_now=True,)

    class Meta:
        verbose_name=u'物流方式中文折扣配置表'
        verbose_name_plural=u' 物流方式中文折扣配置表'
        db_table = 't_cfg_b_logisticway'
        ordering =  ['id']
    def __unicode__(self):
        return u'id:%s'%(self.id)
