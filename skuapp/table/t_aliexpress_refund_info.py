# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models
from public import *

class t_aliexpress_refund_info(models.Model):
    ShopOrderNumber          =   models.CharField(u'店铺单号', max_length=32,blank = True, null = True)
    ShopName                 =   models.CharField(u'卖家简称',max_length=100,blank = True,null = True)
    Country                  =   models.CharField(u'国家',max_length=32,blank=True,null=True)
    ProductSKU               =   models.CharField(u'商品SKU',max_length=100,blank = True,null = True)
    ClosingDate              =   models.DateTimeField(u'发货时间',blank=True, null=True)
    Sale_price               =   models.DecimalField(u'销售价格',max_digits=6,decimal_places=2,blank=True, null=True)
    Refund_id                =   models.CharField(u'退款ID',max_length=100,blank=True, null=True)
    dj_user                 =   models.CharField(u'登记人',max_length=100,blank = True,null = True)
    Refund_price             =   models.DecimalField(u'退款价格', max_digits=6,decimal_places=2, blank=True, null=True)
    Paypal_Account           =   models.CharField(u'Papal账户', max_length=100, blank=True, null=True)
    Refund_reason            =   models.CharField(u'退款原因',choices=getChoices(ChoiceRefundReason),max_length=100, blank=True, null=True)
    Update_time              =   models.DateTimeField(u'更新时间', blank=True, null=True)
    Remarks                  =   models.TextField(u'备注',blank=True,null=True)

    class Meta:
        verbose_name=u'速卖通退款信息登记'
        verbose_name_plural=u'速卖通退款信息登记'
        db_table = 't_aliexpress_refund_info'
        ordering =  ['-id']
    def __unicode__(self):
        return u'id:%s'%(self.id)
