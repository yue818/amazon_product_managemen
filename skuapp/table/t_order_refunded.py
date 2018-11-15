# -*- coding: utf-8 -*-
from django.db import models
from public import *
class t_order_refunded(models.Model):
    #PlatformName   =   models.CharField(u'反向链接平台',choices=getChoices(ChoicePlatformName),max_length=16,blank = True,null = True)
    ShopName                =   models.CharField(u'店铺名称',max_length=32,blank = True,null = True)
    OrderDate              =   models.CharField(u'订单日期',max_length=64,blank = True,null = True)
    OrderState               =   models.CharField(u'订单状态',choices=getChoices(ChoiceOrderState),max_length=64,null = True)
    OrderId                 =   models.CharField(u'订单ID',max_length=64,blank = True,null = True)
    #SKU              =   models.CharField(u'SKU',max_length=64,blank = True,null = True)
    ShopSKU              =   models.CharField(u'店铺SKU',max_length=64,blank = True,null = True)
    ProductID              =   models.CharField(u'产品ID',max_length=64,blank = True,null = True)
    Quantity              =   models.IntegerField(u'订单数量',max_length=11,blank = True,null = True)
    Price              =   models.CharField(u'单价',max_length=32,blank = True,null = True)
    Shipping              =   models.CharField(u'Shipping',max_length=32,blank = True,null = True)
    Shippedon              =   models.CharField(u'装运日期',max_length=32,blank = True,null = True)
    LastUpdated              =   models.DateTimeField(u'平台更新时间',max_length=32,blank = True,null = True)
    UpdateTime              =   models.DateTimeField(u'更新时间',auto_now=True,blank = True,null = True)
    Image              =   models.CharField(u'图片',max_length=200,blank = True,null = True)
    Title              =   models.CharField(u'标题',max_length=255,blank = True,null = True)
    RefundDate       =     models.CharField(u'退款日期',max_length=32,blank = True,null = True)
    RefundReason      =    models.CharField(u'退款原因',max_length=100,blank = True,null = True)

	
    class Meta:
        verbose_name=u'订单退款信息'
        verbose_name_plural=u'订单退款信息'
        db_table = 't_order'
        ordering =  ['id']
    def __unicode__(self):
        return u'%s'%(self.id)