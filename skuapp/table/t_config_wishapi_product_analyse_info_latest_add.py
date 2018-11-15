# -*- coding: utf-8 -*-
from django.db import models
from public import *

class t_config_wishapi_product_analyse_info_latest_add(models.Model):

    id = models.IntegerField(u'id', max_length=11, blank=False, null=False, primary_key='id')
    Pid = models.CharField(u'商品ID', max_length=200, blank=False, null=False)
    Name = models.CharField(u'标题ListingTitle', max_length=200, blank=True, null=True)
    SourcePicPath = models.CharField(u'调研图', max_length=255, blank=True, null=True)
    approved_date = models.DateTimeField(u'开张时间', blank=True, null=True)
    NumBought = models.IntegerField(u'总购买人数', blank=True, null=True)
    ShelveDay = models.DateTimeField(u'上架日期', blank=True, null=True)
    UnitPrice = models.IntegerField(u'单价', max_length=16, blank=True, null=True)
    OrdersLast7Days = models.IntegerField(u'7天order数', max_length=16, blank=True, null=True)
    OrdersLast7to14Days = models.IntegerField(u'前8-14天order数', max_length=16, blank=True, null=True)
    SupplierID = models.TextField(u'是否有供货商', max_length=100, choices=getChoices(ChoiceSupplierID),blank=True, null=True)
    DealName = models.CharField(u'处理人', max_length=64, blank=True, null=True)
    DealTime = models.DateTimeField(u'处理时间', blank=True, null=True)
    YNDone = models.CharField(u'是否做过', max_length=6, choices=getChoices(ChoiceYNDone), default='N',blank=True, null=True)
    Remarks = models.CharField(u'备注', max_length=255, blank=True, null=True)
    salesgrowth = models.IntegerField(u'增长率', max_length=20, blank=True, null=True)
    Op_time = models.DateTimeField(u'采集时间', max_length=14, blank=False, null=False)
    Collar = models.CharField(u'开发状态', choices=getChoices(ChoiceCollar), default='0', max_length=20, blank=True,null=False)

    class Meta:
        verbose_name=u'WISH 24小时内新增采集'
        verbose_name_plural=u'WISH 24小时内新增采集'
        db_table = 't_config_wishapi_product_analyse_info'
        ordering = ['-Op_time']
    def __unicode__(self):
        return u'%s'%(self.id)