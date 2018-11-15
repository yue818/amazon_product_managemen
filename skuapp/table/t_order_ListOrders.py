# -*- coding: utf-8 -*-
from django.db import models

#amazon 主订单内容
class t_order_ListOrders(models.Model):
    ShopName                =   models.CharField(u'店铺名称',max_length=32,blank = True,null = True)
    RequestId               =   models.CharField(u'RequestId',max_length=32,blank = True,null = True)
    LastUpdatedAfter        =   models.CharField(u'LastUpdatedAfter',max_length=32,blank = True,null = True)
    LastUpdatedBefore       =   models.CharField(u'LastUpdatedBefore',max_length=32,blank = True,null = True)
    AmazonOrderId           =   models.CharField(u'AmazonOrderId',max_length=32,blank = True,null = True)
    Orders                  =   models.TextField(u'订单内容',blank = True,null = True)
    UpdateTime              =   models.DateTimeField(u'更新时间',auto_now=True,blank = True,null = True)
    class Meta:
        verbose_name=u'主订单内容(Amazon)'
        verbose_name_plural=u'主订单内容(Amazon)'
        db_table = 't_order_ListOrders'
        ordering =  ['id']
    def __unicode__(self):
        return u'%s'%(self.id)