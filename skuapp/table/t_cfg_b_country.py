# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models

class t_cfg_b_country(models.Model):
    country_code             =   models.CharField(u'国家编码',max_length=24,blank = True,null = True)
    country                  =   models.CharField(u'国家中文',max_length=32,blank = True,null = True)
    CURRENCYCODE             =   models.CharField(u'当前货币编号',max_length=24,blank = True,null = True)
    updatetime               =   models.DateTimeField(u'更新时间',auto_now=True,)

    class Meta:
        verbose_name=u'国家配置表'
        verbose_name_plural=u'国家配置表'
        db_table = 't_cfg_b_country'
        ordering =  ['id']
    def __unicode__(self):
        return u'id:%s'%(self.id)
