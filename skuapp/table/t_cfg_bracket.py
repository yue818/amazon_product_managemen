# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models

class t_cfg_bracket(models.Model):
    bracketid                =   models.IntegerField(u'分档计费ID',blank = True,null = True)
    weight                   =   models.DecimalField(u'重量',max_digits=6,decimal_places=2,blank = True,null = True)
    money                    =   models.DecimalField(u'价格',max_digits=8,decimal_places=4,blank = True,null = True)
    CURRENCYCODE             =   models.CharField(u'当前货币编号',max_length=16,blank = True,null = True)

    class Meta:
        verbose_name=u'分档计费配置表'
        verbose_name_plural=u'分档计费配置表'
        db_table = 't_cfg_bracket'
        ordering =  ['id']
    def __unicode__(self):
        return u'id:%s'%(self.id)
