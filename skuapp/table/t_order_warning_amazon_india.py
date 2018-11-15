# -*- coding: utf-8 -*-
from django.db import models

class t_order_warning_amazon_india(models.Model):
    shopName            = models.CharField(u'店铺名', max_length=64, blank=True, null=True)
    PlatformName        = models.CharField(u'平台名', max_length=32, blank=True, null=True)
    WarningDays         = models.CharField(u'预警剩余日期', max_length=32, blank=True, null=True)
    WarningInfo         = models.CharField(u'预警信息', max_length=32, blank=True, null=True)
    UpdateTime          = models.DateTimeField(u'更新时间', blank=True, null=True)
    WarningDesc         = models.CharField(u'预警描述', max_length=64, blank=True, null=True)
    AmazonOrderId       = models.CharField(u'Amazon订单号', max_length=64, blank=True, null=True)

    class Meta:
        verbose_name=u'订单预警信息'
        verbose_name_plural=u'订单预警信息'
        db_table = 't_order_warning_amazon_india'
    def __unicode__(self):
        return u'%s'%(self.id)
