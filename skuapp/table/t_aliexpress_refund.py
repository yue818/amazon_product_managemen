# -*- coding: utf-8 -*-
from django.db import models
from public import *

class t_aliexpress_refund(models.Model):
    ShopOrderNumber                 = models.CharField(u'店铺单号', max_length=20, blank=True, null=False)
    CorrespondingSalesNumber        = models.CharField(u'对应销售单号', max_length=20, blank=True, null=False)
    RefundsType                     = models.CharField(u'退款类型', max_length=20, blank=True, null=False)
    AfterSaleType                   = models.CharField(u'售后类型', max_length=20, blank=True, null=False)
    MainTableRemark                 = models.CharField(u'主表备注', max_length=20, blank=True, null=False)
    ShopSKU                         = models.CharField(u'ShopSKU', max_length=20, blank=True, null=False)
    SKU                             = models.CharField(u'SKU', max_length=20, blank=True, null=False)
    QuantityOfGoods                 = models.CharField(u'数量', max_length=20, blank=True, null=False)
    AmountOfMoney                   = models.CharField(u'金额', max_length=20, blank=True, null=False)
    FineMeterRemark                 = models.CharField(u'细表备注', max_length=20, blank=True, null=False)
    RedirectCustomerServiceReason   = models.CharField(u'重寄售后原因', max_length=20, blank=True, null=False)
    ShopName                        = models.CharField(u'卖家简称', max_length=64, blank=True, null=True)
    ExportState                     = models.CharField(u'导出状态',choices=getChoices(ChoiceExportState1),max_length=32,blank = True,null = True)
    ImportTime                      = models.DateTimeField(u'导入时间',max_length=16,blank = True,null = True)
    ImportPerson                    = models.CharField(u'导入人', max_length=64, blank=True, null=True)
    ExportTime                      = models.DateTimeField(u'导出时间',max_length=16,blank = True,null = True)

    class Meta:
        verbose_name=u'速卖通退款记录'
        verbose_name_plural=u'速卖通退款记录'
        db_table = 't_aliexpress_refund'
        ordering =  ['-id']
    def __unicode__(self):
        return u'id:%s'%(self.id)


