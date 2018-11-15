# -*-coding=utf-8-*-
from django.db import models


class t_order_refund_record(models.Model):
    Submiter = models.CharField(u'提交人', max_length=32, blank=True, null=True)
    SubmitTime = models.DateField(u'提交时间', blank=True, null=True)
    ExStatus = models.CharField(u'执行状态', default='WAIT', max_length=32, blank=True, null=True)
    StaTime = models.DateField(u'开始时间', blank=True, null=True)
    EndTime = models.DateField(u'结束时间', blank=True, null=True)
    URL = models.CharField(u'链接', max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = u'退款执行记录'
        verbose_name_plural = u'退款执行记录'
        db_table = 't_order_refund_record'
    def __unicode__(self):
        return u'id:%s' % (self.id)
