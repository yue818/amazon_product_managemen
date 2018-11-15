# -*- coding: utf-8 -*-
from django.db import models
from public import *
from django.db import transaction,connection
from skuapp.table.t_sys_param import *


class t_online_info_logistic(models.Model):
    id                  =   models.IntegerField(u'id',primary_key=True)
    Country             =   models.CharField(u'收货国家',max_length=32,blank = True,null = True)
    #Status              =   models.CharField(u'状态',max_length=32,blank = True,null = True)
    ShopName            =   models.CharField(u'店铺名称',max_length=32,blank = True,null = True)
    TrackNo             =   models.CharField(u'追踪号',max_length=32,blank = True,null = True)
    batchnum            =   models.CharField(u'批次号',max_length=32,blank = True,null = True) 
    LogisticName        =   models.CharField(u'物流方式',max_length=32,blank = True,null = True)
    ExpressName         =   models.CharField(u'快递公司',max_length=32,blank = True,null = True)
    ClosingDate         =   models.DateTimeField(u'发货时间',blank = True,null = True)
    OrderTime           =   models.DateTimeField(u'订单时间',blank = True,null = True)
    OrderNum            =   models.CharField(u'订单编号',max_length=32,blank = True,null = True)
    LogisticInfo        =   models.TextField(u'物流信息',blank = True,null = True)
    LogisticInfoFrom    =   models.CharField(u'物流信息来源',choices=((u'快递公司',u'快递公司'),(u'承运商',u'承运商'),),max_length=100,blank = True)
    TradeTime           =   models.DateTimeField(u'交易时间',blank = True,null = True)
    UpdateTime          =   models.DateTimeField(u'更新时间',blank = True,null = True)
    ErrorCode           =   models.CharField(u'错误代码',max_length=16,blank = True,null = True)
    #ErrorText           =   models.CharField(u'错误信息',max_length=255,blank = True,null = True)
    #WarningStatus      =   models.CharField(u'预警状态',max_length=32,blank = True,null = True)

    class Meta:
        verbose_name=u'物流跟踪信息'
        verbose_name_plural=u'物流跟踪信息'
        db_table = 't_online_info_logistic'
        ordering = ['id']
    def __unicode__(self):
        return u'id:%s'%(self.id)
