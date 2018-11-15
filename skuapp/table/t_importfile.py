# -*- coding: utf-8 -*-
from django.db import models

class t_importfile(models.Model):
    Status           =  models.FileField(u'店铺状态表',blank=True, null=True)
    WeeklyStatistics =  models.FileField(u'费用周统计表',blank=True, null=True)
    SalesData        =  models.FileField(u'销售数据',blank=True, null=True)
    MarketPlan       =  models.FileField(u'营销执行',blank=True, null=True)
    ConfigurationFile=  models.FileField(u'配置文件',blank=True, null=True)
    Submitter        =  models.CharField(u'提交人',max_length=16,blank = True,null = True)
    SubTime          =  models.DateTimeField(u'提交时间',blank = True,null = True)

    class Meta:
        verbose_name = u'文档导入'
        verbose_name_plural = verbose_name
        db_table = 't_importfile'
        ordering =  ['-id']

    def __unicode__(self):
        return u'%s'%(self.id)