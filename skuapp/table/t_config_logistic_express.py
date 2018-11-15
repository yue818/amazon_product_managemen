# -*- coding: utf-8 -*-
from django.db import models
from .public import *


class t_config_logistic_express(models.Model):
    ExpressID    = models.CharField(u'物流公司',max_length=64,blank = True,null = True)
    KeyInfo1     = models.CharField(u'关键信息1',max_length=64,blank = True,null = True)
    KeyInfo2     = models.CharField(u'关键信息2',max_length=64,blank = True,null = True)
    Url          = models.CharField(u'URL',max_length=64,blank = True,null = True )


    class Meta:
        verbose_name = u'物流预警配置表'
        verbose_name_plural = verbose_name
        db_table = 't_config_logistic_express'
    def __unicode__(self):
        return u'%s'%(self.id)
