# -*- coding: utf-8 -*-
from django.db import models
class t_yearweek(models.Model):
    yearweek = models.CharField(u'周编号', max_length=100)
    kf_allcount = models.IntegerField(u'调研开发总数',max_length=16,blank = True,null = True)
    kf_avg = models.DecimalField(u'调研开发平均数',max_digits=10,decimal_places=2)
    kf_number = models.IntegerField(u'调研开发人数',max_length=16,blank = True,null = True)
    jzl_allcount = models.IntegerField(u'建资料总数',max_length=16,blank = True,null = True)
    jzl_avg = models.DecimalField(u'建资料平均数',max_digits=10,decimal_places=2)
    jzl_number = models.IntegerField(u'建资料人数',max_length=16,blank = True,null = True)
    class Meta:
        verbose_name = u'超级用户视图统计表'
        verbose_name_plural = u'超级用户视图统计表'
        db_table = 't_yearweek'
    def __unicode__(self):
         return u'%s'%(self.id)