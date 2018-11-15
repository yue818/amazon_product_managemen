# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db import transaction,connection

class t_download_info(models.Model):
    appname=models.CharField(u'名称',max_length=50,blank=True,null=True)
    abbreviation=models.CharField(u'介绍',max_length=20,blank=True,null=True)
    updatetime=models.DateTimeField(u'更新时间',auto_now=True,blank=True,null=True)
    Datasource = models.CharField(u'数据源',max_length=200,blank=True,null=True)
    Belonger  = models.CharField(u'归属人',max_length=64,blank=True,null=True)

    class Meta:
        verbose_name=u'下载中心'
        verbose_name_plural=verbose_name
        db_table='t_download_info'
        ordering=['-id']
    def __unicode__(self):
        return u'%s'%(self.id)