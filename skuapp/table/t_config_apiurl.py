# -*- coding: utf-8 -*-
from django.db import models
from public import *
class t_config_apiurl(models.Model):
    URL            =   models.CharField(u'URL',max_length=200,blank = True,null = True)
    Status         =   models.CharField(u'状态',choices=getChoices(ChoiceStatus1),default='0',max_length=6,blank = True,null = True)
    runStatus      =   models.CharField(u'运行状态',choices=getChoices(ChoiceStatus3),default='0',max_length=6,blank = True,null = True)
    RefreshTimeB   =   models.DateTimeField(u'刷新开始时间',blank = True,null = True)
    RefreshTimeE   =   models.DateTimeField(u'刷新结束时间',blank = True,null = True)
    RefreshCount   =   models.IntegerField(u'刷新个数',blank = True,null = True)
    pageAllCount   =   models.IntegerField(u'网页总个数',blank = True,null = True)
    oldAllCount    =   models.IntegerField(u'列表总个数',blank = True,null = True)
    UpdateTime     =   models.DateTimeField(u'更新时间',auto_now=True,blank = True,null = True)
    StaffID        =   models.CharField(u'工号',max_length=16,blank = True,null = True,db_index =True)
    group1         =   models.CharField(u'一级分类',max_length=100,blank = True,null = True,db_index =True)
    group2         =   models.CharField(u'二级分类',max_length=100,blank = True,null = True,db_index =True)
    group3         =   models.CharField(u'三级分类',max_length=100,blank = True,null = True,db_index =True)
    group4         =   models.CharField(u'四级分类',max_length=100,blank = True,null = True,db_index =True)
    group5         =   models.CharField(u'五级分类',max_length=100,blank = True,null = True,db_index =True)
    category       =   models.CharField(u'类别',max_length=31,blank = True,null = True,db_index =True)

    class Meta:
        verbose_name=u'Amazon URL配置'
        verbose_name_plural=u'Amazon URL配置'
        db_table = 't_config_apiurl'
        ordering =  ['-id']
        app_label  = 'skuapp'
    def __unicode__(self):
        return u'%s'%(self.id)