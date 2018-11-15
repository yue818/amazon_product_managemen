# -*- coding: utf-8 -*-
from django.db import models

class t_api_schedule(models.Model):
    id                      =   models.AutoField(u'指令流水号',primary_key=True)
    ShopName                =   models.CharField(u'店铺名称',max_length=32,blank = True,null = True)
    PlatformName            =   models.CharField(u'平台名称',max_length=32,blank = True,null = True)
    CMDID                   =   models.CharField(u'指令ID',max_length=64,blank = True,null = True)
    ScheduleTime            =   models.DateTimeField(u'计划执行时间',blank = True,null = True)
    ActualBeginTime         =   models.DateTimeField(u'实际开始时间',blank = True,null = True)
    ActualEndTime           =   models.DateTimeField(u'实际结束时间',blank = True,null = True)
    Status                  =   models.CharField(u'状态0-等待;1-运行中;2-结束',max_length=32,blank = True,null = True)
    ProcessingStatus        =   models.CharField(u'平台返回的处理状态',max_length=32,blank = True,null = True)
    Processed               =   models.IntegerField(u'处理数',max_length=11,blank = True,null = True)
    Successful              =   models.IntegerField(u'成功数',max_length=11,blank = True,null = True)
    WithError               =   models.IntegerField(u'错误数',max_length=11,blank = True,null = True)
    WithWarning             =   models.IntegerField(u'警告数',max_length=11,blank = True,null = True)
    TransactionID           =   models.CharField(u'对方返回事务号',max_length=32,blank = True,null = True)
    InsertTime              =   models.DateTimeField(u'插入时间',blank = True,null = True)
    UpdateTime              =   models.DateTimeField(u'更新时间',auto_now=True,blank = True,null = True)
    Timedelta               =   models.IntegerField(u'重试间隔(s)',max_length=11,blank = True,null = True)
    RetryCount              =   models.IntegerField(u'重试次数',max_length=11,blank = True,null = True)
    Params                  =   models.TextField(u'参数(JSON/XML格式)',blank = True,null = True)
    class Meta:
        abstract = True
    def __unicode__(self):
        return u'id:%s CMDID:%s'%(self.id,self.CMDID)