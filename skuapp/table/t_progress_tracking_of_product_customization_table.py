# -*- coding: utf-8 -*-
from django.db import models

class t_progress_tracking_of_product_customization_table(models.Model):
    SurveyTime       = models.DateTimeField(u'调研时间', blank = True, null = True)
    SurveyPerson     = models.CharField(u'调研员',max_length=16,blank = True,null = True)
    ImageURL         = models.CharField(u'图片URL',max_length=255,blank = True,null = True)
    MainSKU          = models.CharField(u'检索SKU',max_length=16,blank = True,null = True)
    SKU              = models.CharField(u'SKU',max_length=16,blank = True,null = True)
    Name             = models.CharField(u'商品名称',max_length=255,blank = True,null = True)
    KeyWords         = models.CharField(u'关键字',max_length=128,blank = True,null = True)
    ReverseLink      = models.CharField(u'反向链接',max_length=255,blank = True,null = True)
    SupplierLink     = models.CharField(u'供应商链接',max_length=255,blank = True,null = True)
    SurveyAnalysis   = models.TextField(u'调研分析',max_length=500,blank = True,null = True)
    MakeDemand       = models.TextField(u'定做要求',max_length=500,blank = True,null = True)
    DevelopRemark    = models.TextField(u'开发备注',max_length=500,blank = True,null = True)
    SupplyChainDeveloper    = models.CharField(u'供应链开发员',max_length=16,blank = True,null = True)
    FinishTime              = models.DateTimeField(u'计划完成时间',blank = True, null = True)
    CheckPerson             = models.CharField(u'审核人', max_length=16,blank = True, null = True)
    CheckTime               = models.DateTimeField(u'审核时间',blank = True, null = True)
    CheckRemark             = models.TextField(u'审核意见',max_length=500,blank = True, null = True)
    RateOfProgress          = models.CharField(u'进度',max_length=32,blank = True, null = True)
    Enclosure               = models.FileField(u'附件',max_length=128,blank = True, null = True)
    DonePerson              = models.CharField(u'完成操作人', max_length=16, blank=True, null=True)
    DoneTime                = models.DateTimeField(u'完成操作时间', blank=True, null=True)
    Submiter                = models.CharField(u'提交人', max_length=16, blank=True, null=True)
    SubmitTime              = models.DateTimeField(u'提交时间', blank=True, null=True)
    FromClothes             = models.SmallIntegerField(u'是否来自服装', default=0)

    class Meta:
        verbose_name = u'产品定做落地跟踪表'
        verbose_name_plural = verbose_name
        db_table = 't_progress_tracking_of_product_customization_table'
    def __unicode__(self):
         return u'%s'%(self.id)