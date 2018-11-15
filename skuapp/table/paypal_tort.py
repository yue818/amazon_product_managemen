# -*- coding: utf-8 -*-
from django.db import models
from public import *

class paypal_tort(models.Model):
    Brand                        = models.CharField(u'品牌', max_length=64, blank=True, null=False)
    GraphicTrademark             = models.CharField(u'图形商标', max_length=64, blank=True, null=False)
    Site                         = models.CharField(u'官网', max_length=100, blank=True, null=False)
    Category                     = models.CharField(u'分类', max_length=20, blank=True, null=False)


    class Meta:
        verbose_name=u'paypal侵权汇总表'
        verbose_name_plural=u'paypal侵权汇总表'
        db_table = 'paypal_tort'
        ordering =  ['-id']
    def __unicode__(self):
        return u'id:%s'%(self.id)



