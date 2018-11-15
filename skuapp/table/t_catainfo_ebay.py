# -*- coding: utf-8 -*-
from django.db import models
from public import *
class t_catainfo_ebay(models.Model):
    id             =   models.AutoField(u'流水号',primary_key=True)
    CatagoryID     =   models.CharField(u'分类ID',max_length=15,blank = False,null = False,db_index =True)
    CatagoryName1  =   models.CharField(u'分类名称',max_length=127,blank = False,null = False)
    URL            =   models.CharField(u'分类目录地址',max_length=127,blank = True,null = True)
    bsURL          =   models.CharField(u'热销榜单地址',max_length=127,blank = True,null = True)
    cata1          =   models.CharField(u'一级分类',max_length=63,blank = False,null = False,db_index =True)
    cata2          =   models.CharField(u'二级分类',max_length=63,blank = True,null = True,db_index =True)
    cata3          =   models.CharField(u'三级分类',max_length=63,blank = True,null = True,db_index =True)
    cata4          =   models.CharField(u'四级分类',max_length=63,blank = True,null = True,db_index =True)
    cata5          =   models.CharField(u'五级分类',max_length=63,blank = True,null = True,db_index =True)
    CreateTime     =   models.DateTimeField(u'创建时间',blank = True,null = True)
    CatagoryLv     =   models.CharField(u'分类等级',max_length=6,blank = False,null = False)
    LastRefreshTimeE=  models.DateTimeField(u'最后刷新时间',blank = True,null = True)
    mount           =   models.CharField(u'本周产品数目',max_length=6,blank = True,null = True,db_index =True)
    refresh         =   models.CharField(u'新产品数目',max_length=6,blank = True,null = True,db_index =True)
    tagBS           =   models.CharField(u'抓取热销榜',choices=getChoices(ChoiceYN),default='Y',max_length=10,blank = False,null = False,db_index =True)
    bsSoldCond      =   models.IntegerField(u'周销量门槛',blank = True,null=True)
    tagBM           =   models.CharField(u'是否抓取BESTMATCH',choices=getChoices(ChoiceYN),default='N',max_length=10,blank = False,null = False,db_index =True)
    StaffID         =   models.CharField(u'工号',max_length=31,blank = True,null = True)
    department      =   models.CharField(u'开发部门',choices=getChoices(ChoiceDev),default='Others',max_length=15,blank = True,null = False)
    
    class Meta:
        verbose_name=u'eBay分类信息配置'
        verbose_name_plural=u'eBay分类信息配置'
        db_table = 't_catainfo_ebay'
        ordering =  ['-refresh']
    def __unicode__(self):
        return u'%s'%(self.CatagoryID)