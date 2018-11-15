# -*- coding: utf-8 -*-
from django.db import models

class t_order_track_info_amazon_india(models.Model):
    AmazonOrderId = models.CharField(u'Amazon订单号', max_length=32, blank=True, null=True)
    track_info = models.TextField(u'物流信息', blank=True, null=True)
    track_status = models.CharField(u'物流状态', max_length=64, blank=True, null=True)
    trackNumber = models.CharField(u'运单号', max_length=32, blank=True, null=True)
    track_TDate = models.CharField(u'取件日期', max_length=64, blank=True, null=True)
    track_From = models.CharField(u'出发地', max_length=64, blank=True, null=True)
    track_Des = models.CharField(u'目的地', max_length=64, blank=True, null=True)
    track_StateDesc = models.CharField(u'状态描述', max_length=64, blank=True, null=True)
    track_ADate = models.CharField(u'签收日期', max_length=64, blank=True, null=True)
    track_Sign = models.CharField(u'签收人', max_length=64, blank=True, null=True)
    track_company = models.CharField(u'物流公司', max_length=64, blank=True, null=True)
    track_service = models.CharField(u'配送服务', max_length=32, blank=True, null=True)
    LableData = models.CharField(u'物流运单面单URL', max_length=200, blank=True, null=True)
    UpdateTime = models.DateTimeField(u'同步时间', blank=True, null=True)

    class Meta:
        verbose_name=u'Amazon印度站gati物流信息'
        verbose_name_plural=u'Amazon印度站gati物流信息'
        db_table = 't_order_track_info_amazon_india'
    def __unicode__(self):
        return u'%s'%(self.id)