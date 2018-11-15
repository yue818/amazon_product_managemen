# -*-coding=utf-8-*-
from django.db import models

class t_paypal_payout_log(models.Model):
    Payout_Account  = models.CharField(u'付款账号',max_length=50,blank = True,null = True)
    Receipt_Account = models.CharField(u'收款账号',max_length=50,blank = True,null = True)
    Account         = models.DecimalField(u'转账金额(单位:$)',max_digits=4,decimal_places=2,blank=False,null=False)
    Status          = models.CharField(u'付款状态', max_length=32, blank=True, null=True)
    Payout_Time     = models.DateTimeField(u'付款时间', blank=True, null=True)
    Log             = models.CharField(u'日志',max_length=255,blank = True,null = True)

    class Meta:
        verbose_name = u'paypal付款记录'
        verbose_name_plural = u'paypal付款记录'
        db_table = 't_paypal_payout_log'
    def __unicode__(self):
        return self.id