# -*- coding: utf-8 -*-
from django.db import models
from .public import *


class t_config_logistic(models.Model):
    LogisticName = models.CharField(u'物流方式',max_length=64,blank = True,null = True)  
    ExpressID    = models.CharField(u'物流公司',max_length=64,blank = True,null = True)
    ServiceID    = models.CharField(u'承运平台',max_length=64,blank = True,null = True)
    Oversea      = models.CharField(u'海外/国内',max_length=3,choices=getChoices(OverSea))


    class Meta:
        verbose_name = u'物流方式配置表'
        verbose_name_plural = verbose_name
        db_table = 't_config_logistic'
    def __unicode__(self):
        return u'%s'%(self.id)
