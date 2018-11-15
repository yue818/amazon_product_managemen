# -*- coding: utf-8 -*-
from django.db import models
from public import *
class t_hotsale_proinfo_ebay(models.Model):
    URL             =   models.CharField(u'反向链接',max_length=127,blank = True,null = True)
    ProductID       =   models.CharField(u'产品ID',max_length=15,blank = True,null = True,db_index =True)
    CreateTime      =   models.DateTimeField(u'入榜时间',blank = True,null = True)
    Title           =   models.CharField(u'产品名称',max_length=127,blank = True,null = True)
    Price           =   models.CharField(u'价格(美元)',max_length=10,blank = True,null = True)
    Image           =   models.ImageField(u'图片',blank=True, null=True)
    SrcImage        =   models.ImageField(u'源图片',blank=True, null=True)
    CatagoryID      =   models.CharField(u'分类ID',max_length=32,blank = True,null = True)
    sold            =   models.IntegerField(u'周销量',blank = True,null=True)
    ifDone          =   models.CharField(u'是否做过',choices=getChoices(ChoiceYN),default='N',max_length=6,blank = True,null = True)
    shipping        =   models.CharField(u'是否免邮',max_length=63,blank = True,null = True)
    cata1           =   models.CharField(u'一级分类',max_length=63,blank = True,null = True,db_index =False)
    cata2           =   models.CharField(u'二级分类',max_length=63,blank = True,null = True,db_index =False)
    cata3           =   models.CharField(u'三级分类',max_length=63,blank = True,null = True,db_index =False)
    cata4           =   models.CharField(u'四级分类',max_length=63,blank = True,null = True,db_index =False)
    cata5           =   models.CharField(u'五级分类',max_length=63,blank = True,null = True,db_index =False)
    used            =   models.CharField(u'当前状态',choices=getChoices(ChoiceDealStat),default='N',max_length=6,blank = True,null = True)
    remark          =   models.TextField(u'备注',max_length=511,blank = True,null = True,db_index =False)
    lastRefreshTime =   models.DateTimeField(u'刷新时间',blank = True,null = True)
    isDiscard       =   models.CharField(u'是否已弃用',choices=getChoices(ChoiceYN),default='N',max_length=6,blank = True,null = True)
    isStop          =   models.CharField(u'是否已下架',choices=getChoices(ChoiceYN),default='N',max_length=6,blank = True,null = True)
    location        =   models.CharField(u'Item location',max_length=63,blank = True,null = True,db_index =False)
    tagTime         =   models.DateTimeField(u'处理时间',blank = True,null = True)
    tagUser         =   models.CharField(u'当前处理人',max_length=31,blank = True,null = True)
    dRating         =   models.IntegerField(u'日上升',blank = True,null=True)
    wRating         =   models.IntegerField(u'周上升',blank = True,null=True)
    department      =   models.CharField(u'开发部门',choices=getChoices(ChoiceDev),default='Others',max_length=15,blank = True,null = False)
    region          =   models.CharField(u'产品地区',choices=getChoices(ChoiceItemLoction),max_length=31,blank = True,null = True,db_index =False)
    
    class Meta:
        verbose_name=u'eBay热销榜单信息'
        verbose_name_plural=u'eBay热销榜单信息'
        db_table = 't_hotsale_proinfo_ebay'
        ordering =  ['-CreateTime']
    def __unicode__(self):
        return u'%s'%(self.id)