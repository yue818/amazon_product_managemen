# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models
from public import *

class t_joom_refund(models.Model):
    #ProductID                  =   models.CharField(u'产品ID', max_length=32,blank = True, null = True)
    SKU                        =   models.CharField(u'SKU', max_length=64,blank = True, null = True)
    nid                        =   models.CharField(u'订单编号', max_length=64,blank = True, null = True)
    ShopNum                    =   models.CharField(u'店铺单号',max_length=100,blank = True,null = True)
    RefundPrice                =   models.CharField(u'退款价格',max_length=32,blank=True,null=True)
    RefundReason               =   models.CharField(u'退款原因',max_length=100,blank = True,null = True)
    UploadMan                  =   models.CharField(u'导入人', max_length=100, blank=True, null=True)
    UploadTime                 =   models.DateTimeField(u'导入时间',blank=True, null=True)
    UpdateTime                 =   models.DateTimeField(u'更新时间',auto_now = True)

    class Meta:
        verbose_name=u'Joom退款'
        verbose_name_plural=u'Joom退款'
        db_table = 't_joom_refund'
        ordering =  ['-id']
    def __unicode__(self):
        return u'id:%s'%(self.id)
