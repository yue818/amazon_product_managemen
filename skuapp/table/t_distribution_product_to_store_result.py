# coding=utf-8

from django.db import models
from public import *

class t_distribution_product_to_store_result(models.Model):

    PlatformName    =   models.CharField(u'平台名称',max_length=32,blank = True,null = True)
    PID             =   models.CharField(u'铺货ID',max_length=20,blank = True,null = True)
    SKU             =   models.CharField(u'csvSKU',max_length=32,blank = True,null = True)
    ShopName        =   models.CharField(u'店铺名称', max_length=32, blank=True, null=True)
    Submitter       =   models.CharField(u'提交人',max_length=10, blank=True, null=True)
    SubTime         =   models.DateTimeField(u'提交时间', blank=True, null=True)
    ScheduleTime    =   models.DateTimeField(u'指令计划执行时间', blank=True, null=True)
    Status          =   models.CharField(u'铺货结果',choices=getChoices(ChoiceDistributionResult),max_length=255,blank=True, null=True)
    Params          =   models.TextField(u'参数(JSON/XML格式)',blank = True,null = True)
    ParentSKU       =   models.CharField(u'ParentSKU',max_length=32,blank = True,null = True)
    Type            =   models.CharField(u'铺货类型',choices=getChoices(ChoiceDistributionType),max_length=20,blank=True,null=True)
    ErrorMessage    =   models.TextField(u'错误信息',blank=True,null=True)

    class Meta:
        verbose_name=u'铺货结果'
        verbose_name_plural=verbose_name
        db_table = 't_distribution_product_to_store_result'
        ordering =  ['-id']
    def __unicode__(self):
        return u'%s'%(self.id)