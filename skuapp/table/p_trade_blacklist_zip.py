# -*- coding: utf-8 -*-
from django.db import models
from public import *
from django.db import transaction,connection
from skuapp.table.t_sys_param import *


class p_trade_blacklist_zip(models.Model):
    NID                 =   models.IntegerField(u'NID')
    EMAIL               =   models.CharField(u'邮箱',max_length=32,blank = True,null = True)
    #RECEIVERBUSINESS    =  models.CharField(u'邮箱',max_length=32,blank = True,null = True)
    RECEIVERID          =   models.CharField(u'接收方ID',max_length=32,blank = True,null = True)
    COUNTRYCODE         =   models.CharField(u'国家代号',max_length=32,blank = True,null = True)
    SUFFIX              =   models.CharField(u'店铺名称',max_length=32,blank = True,null = True)
    ORDERTIME           =   models.DateTimeField(u'订单时间',blank = True,null = True)
    SHIPTOSTREET        =   models.CharField(u'地址一',max_length=32,blank = True,null = True)
    SHIPTOSTREET2       =   models.CharField(u'地址二',max_length=32,blank = True,null = True)
    SHIPTOZIP           =   models.CharField(u'邮编',max_length=32,blank = True,null = True)
    AllGoodsDetail      =   models.CharField(u'MainSKU',max_length=32,blank = True,null = True)
    Operate             =   models.CharField(u'操作',choices=getChoices(OP),max_length=16,blank = True,null = True)
    OperateDescription  =   models.TextField(u'操作描述',max_length=16,blank = True,null = True)
    OperateTime         =   models.DateTimeField(u'操作时间',blank = True,null = True,auto_now=True)
    TbTime              =   models.DateTimeField(u'同步时间',blank = True,null = True)
    pic                 =   models.CharField(u'图片',max_length=32,blank = True,null = True)
    From_type           =   models.CharField(u'标记',max_length=11,blank = True,null = True)

    class Meta:
        verbose_name=u'邮编黑名单'
        verbose_name_plural=u'邮编黑名单信息'
        db_table = 'p_trade_blacklist_zip'

    def __unicode__(self):
        return u'NID:%s'%(self.NID)
