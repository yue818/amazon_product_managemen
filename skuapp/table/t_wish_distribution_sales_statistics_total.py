# coding=utf-8

"""
销售数据累计 MODEL
"""

from django.db import models


class t_wish_distribution_sales_statistics_total(models.Model):

    a_date                  =   models.DateField(u'累计日期', blank=True, null=True)
    a_execute_success_num   =   models.IntegerField(u'累计铺货成功数', max_length=11, blank=True, null=True)
    a_approved_num          =   models.IntegerField(u'累计审核通过数', max_length=11, blank=True, null=True)
    a_approved_percent      =   models.CharField(u'累计审核通过比', max_length=32, blank=True, null=True)
    a_out_order_num         =   models.IntegerField(u'累计出单数', max_length=11, blank=True, null=True)
    a_out_order_percent     =   models.CharField(u'累计出单比', max_length=32, blank=True, null=True)
    a_sales_num             =   models.IntegerField(u'累计销售额', max_length=11, blank=True, null=True)

    class Meta:
        verbose_name = u'累计销售统计'
        verbose_name_plural = verbose_name
        ordering = ['-a_date']
        db_table = 't_wish_distribution_sales_statistics_total'
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)