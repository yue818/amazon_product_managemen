# coding=utf-8


from django.db import models
from public import *


class t_order_out_of_stock(models.Model):

    Plateform           =   models.CharField(u'平台', choices=getChoices(ChoicePlatformName), max_length=64, blank=True, null=True)
    ExportDate          =   models.DateField(u'导出日期', blank=True, null=True)
    OrderId             =   models.IntegerField(u'订单编号', max_length=32, blank=True, null=True)
    DelayDays           =   models.IntegerField(u'延迟天数', max_length=4, blank=True, null=True)
    Seller              =   models.CharField(u'卖家简称', max_length=128, blank=True, null=True)
    Details             =   models.TextField(u'商品明细', blank=True, null=True)
    TradingTime         =   models.DateTimeField(u'交易时间', blank=True, null=True)
    ExcelFile           =   models.FileField(u'缺货订单Excel文件', blank=True, null=True)
    CreateTime          =   models.DateTimeField(u'导入Online时间', blank=True, null=True)
    CreateStaff         =   models.CharField(u'导入人', max_length=16, blank=True, null=True)


    class Meta:
        verbose_name = u'缺货订单信息'
        verbose_name_plural = verbose_name
        db_table = 't_order_out_of_stock'
        app_label = 'skuapp'
        ordering = ['-ExportDate']

    def __unicode__(self):
        return u'id:%s'%(self.id)