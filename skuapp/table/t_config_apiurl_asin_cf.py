# -*- coding: utf-8 -*-
from django.db import models
from public import *


class t_config_apiurl_asin_cf(models.Model):
    URL            =   models.CharField(u'URL',max_length=200,blank = True,null = True)
    ASIN           =   models.CharField(u'ASIN',max_length=16,blank = True,null = True)
    Status         =   models.CharField(u'状态',choices=getChoices(ChoiceStatus2),max_length=64,blank = True,null = True)
    UplsitTime     =   models.DateTimeField(u'上榜时间',blank = True,null = True)
    RefreshTime    =   models.DateTimeField(u'刷新时间',blank = True,null = True)
    Title          =   models.CharField(u'Title',max_length=64,blank = True,null = True)
    Brand          =   models.CharField(u'Brand',max_length=64,blank = True,null = True)
    Feature        =   models.TextField(u'Feature',blank = True,null = True)
    ListPrice      =   models.CharField(u'ListPrice(美元)',max_length=10,blank = True,null = True)
    SmallImage     =   models.ImageField(u'图片',blank=True, null=True)
    ProductGroup   =   models.CharField(u'ProductGroup',max_length=32,blank = True,null = True)
    Error          =   models.CharField(u'Error',max_length=100,blank = True,null = True)
    Serial         =   models.IntegerField(u'序列号',blank = True,null=True)
    Rank           =   models.IntegerField(u'排名',max_length=11,blank = True,null = True)
    Remarks        =   models.CharField(u'备注',max_length=255,blank = True,null = True)
    group1         =   models.CharField(u'一级分类',max_length=100,blank = True,null = True,db_index =True)
    group2         =   models.CharField(u'二级分类',max_length=100,blank = True,null = True,db_index =True)
    group3         =   models.CharField(u'三级分类',max_length=100,blank = True,null = True,db_index =True)
    group4         =   models.CharField(u'四级分类',max_length=100,blank = True,null = True,db_index =True)
    group5         =   models.CharField(u'五级分类',max_length=100,blank = True,null = True,db_index =True)
    PlatformName   =   models.CharField(u'平台名称',max_length=16,blank = True,null = True)
    DealName       =   models.CharField(u'领用人',max_length=64,blank = True,null = True)
    DealTime       =   models.DateTimeField(u'领用时间',blank = True,null = True)
    YNEnabled      =   models.CharField(u'是否启用',choices=getChoices(ChoiceStatus1),default='0',max_length=6,blank = True,null = True)
    Abandoned      =   models.CharField(u'是否弃用',choices=getChoices(ChoiceAbandoned),default='0',max_length=6,blank = True,null = False)
    Collar         =   models.CharField(u'是否领用',choices=getChoices(ChoiceCollar),default='0',max_length=6,blank = True,null = False)
    category       =   models.CharField(u'类别',max_length=31,blank = True,null = True,db_index =True)
    Weight         =   models.DecimalField(u'重量',max_digits=10, decimal_places=2,blank = True,null = True)
    Weight_Units   =   models.CharField(u'重量单位',max_length=15,blank = True,null = True)
    Size           =   models.CharField(u'尺寸',max_length=64,blank = True,null = True)
    Size_Units     =   models.CharField(u'尺寸单位',max_length=32,blank = True,null = True)
    Added_Time     =   models.DateField(u'上架时间',blank = True,null = True)

    class Meta:
        verbose_name=u'Amazon已有重复'
        verbose_name_plural=u'Amazon已有重复'
        db_table = 't_config_apiurl_asin'
        ordering =  ['-UplsitTime']
    def __unicode__(self):
        return u'%s'%(self.id)