# -*- coding: utf-8 -*-
from django.db import models
from .public import *

class t_tort_brands_info(models.Model):
    class_name  = models.CharField(u'分类',choices=getChoices(300),max_length=255,blank = True,null = True)
    brands      = models.CharField(u'主品牌', max_length=255, blank=True, null=True)
    viceBrands  = models.CharField(u'品牌', max_length=255, blank=True, null=True)
    pictureUrl  = models.CharField(u'图形商标', max_length=255, blank=True, null=True)

    class Meta:
        verbose_name=u'阿里速卖通侵权查询'
        verbose_name_plural=u'阿里速卖通侵权查询'
        db_table = 't_tort_brands_info'
    def __unicode__(self):
        return self.id