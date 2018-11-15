# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models
from public import *

class t_aliexpress_refund_info_all(models.Model):
    ShopOrderNumber          =   models.CharField(u'店铺单号',max_length=32,blank=True,null=True)
    ShopName                 =   models.CharField(u'卖家简称',max_length=100,blank = True,null = True)
    ProductSKU               =   models.CharField(u'商品SKU',max_length=100,blank = True,null = True)
    ClosingDate              =   models.DateTimeField(u'发货时间',blank=True, null=True)
    Sale_price               =   models.DecimalField(u'销售价格',max_digits=6,decimal_places=2,blank=True, null=True)
    Country                  =   models.CharField(u'国家',max_length=32,blank=True,null=True)
    Update_time              =   models.DateTimeField(u'更新时间', blank=True, null=True)

    class Meta:
        verbose_name=u'普源同步速卖通退款更新详情表'
        verbose_name_plural=u'普源同步速卖通退款更新详情表'
        db_table = 't_aliexpress_refund_info_all'
        ordering =  ['-id']
    def __unicode__(self):
        return u'id:%s'%(self.id)
