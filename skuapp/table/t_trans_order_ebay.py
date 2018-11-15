# -*- coding: utf-8 -*-
from django.db import models
from public import *
#各店铺在线信息
class t_trans_order_ebay(models.Model):
    spBuyerName    =   models.CharField(u'买家姓名',max_length=64,blank = True,null = True)
    spCarrier      =   models.CharField(u'运输方式',max_length=32,blank = True,null = True)
    spTracking     =   models.CharField(u'运输路线',max_length=64,blank = True,null = True)
    spCreateDate   =   models.CharField(u'订单生产日期',max_length=32,blank = True,null = True)
    itemSite       =   models.CharField(u'产地',max_length=16,blank = True,null = True)
    itemTitle      =   models.CharField(u'标题',max_length=128,blank = True,null = True)
    itemQuantity   =   models.IntegerField(u'数量',max_length=12,blank = True,null = True)
    itemPrice      =   models.FloatField(u'价格',max_length=12)
    transid        =   models.CharField(u'运输ID',max_length=32,blank = True,null = True)
    itemid         =   models.CharField(u'产品标识id',max_length=32,blank = True,null = True)
    orderid        =   models.CharField(u'订单ID',max_length=64,blank = True,null = True)

    
    class Meta:
        verbose_name=u'ebay订单运输信息'
        verbose_name_plural=u'ebay订单运输信息'
        db_table = 't_trans_order_ebay'
    def __unicode__(self):
        return u'%s'%(self.id)