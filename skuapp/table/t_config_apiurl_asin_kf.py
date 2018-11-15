# -*- coding: utf-8 -*-
from django.db import models
from public import *
class t_config_apiurl_asin_kf(models.Model):
    URL            =   models.CharField(u'URL',max_length=200,blank = True,null = True)
    ASIN           =   models.CharField(u'ASIN',max_length=16,blank = True,null = True)
    Status         =   models.CharField(u'状态',choices=getChoices(ChoiceStatus2),max_length=64,blank = True,null = True)
    RefreshTime    =   models.DateTimeField(u'刷新时间',blank = True,null = True)
    Title          =   models.CharField(u'Title',max_length=64,blank = True,null = True)
    Brand          =   models.CharField(u'Brand',max_length=64,blank = True,null = True)
    Feature        =   models.TextField(u'Feature',blank = True,null = True)
    ListPrice      =   models.CharField(u'ListPrice(美元)',max_length=10,blank = True,null = True)
    SmallImage     =   models.ImageField(u'图片',blank=True, null=True)
    ProductGroup   =   models.CharField(u'ProductGroup',max_length=32,blank = True,null = True)
    Error          =   models.CharField(u'Error',max_length=100,blank = True,null = True)
    Serial         =   models.IntegerField(u'序列号',blank = True,null=True)
    Rank           =   models.CharField(u'排名',max_length=255,blank = True,null = True)
    YNDone         =   models.CharField(u'是否做过',choices=getChoices(ChoiceStatus4),default='0',max_length=6,blank = True,null = True)
    Remarks        =   models.CharField(u'备注',max_length=100,blank = True,null = True)
    group1         =   models.CharField(u'一级分类',max_length=100,blank = True,null = True,db_index =True)
    group2         =   models.CharField(u'二级分类',max_length=100,blank = True,null = True,db_index =True)
    group3         =   models.CharField(u'三级分类',max_length=100,blank = True,null = True,db_index =True)
    group4         =   models.CharField(u'四级分类',max_length=100,blank = True,null = True,db_index =True)
    group5         =   models.CharField(u'五级分类',max_length=100,blank = True,null = True,db_index =True)
    DealName       =   models.CharField(u'处理人',max_length=64,blank = True,null = True)
    DealTime       =   models.DateTimeField(u'处理时间',blank = True,null = True)
    PlatformName   =   models.CharField(u'平台名称',max_length=16,blank = True,null = True)

    class Meta:
        verbose_name=u'Amazon ASIN开发'
        verbose_name_plural=u'Amazon ASIN开发'
        db_table = 't_config_apiurl_asin_kf'
        ordering =  ['-id']
    def __unicode__(self):
        return u'%s'%(self.id)