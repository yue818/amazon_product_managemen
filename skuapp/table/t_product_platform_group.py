# -*- coding: utf-8 -*-
from django.db import models
from public import *
class t_product_platform_group(models.Model):
    PlatformName         =   models.CharField(u'平台名称',choices=getChoices(ChoicePlatformName),max_length=16,blank = True,null = True)
    RefreshTime          =   models.DateField(u'刷新时间',blank = True,null = True)
    QNumber              =   models.CharField(u'全部数量',max_length=32,blank = True,null = True)
    YNumber              =   models.CharField(u'录入数量',max_length=32,blank = True,null = True)
    Date                 =   models.DateField(u'日期',blank = True,null = True)

    class Meta:
        verbose_name=u'平台分组'
        verbose_name_plural=verbose_name
        db_table = 't_product_platform_group'
        ordering =  ['-Date']
        #proxy = True
    def __unicode__(self):
        return u'id:%s'%(self.id)