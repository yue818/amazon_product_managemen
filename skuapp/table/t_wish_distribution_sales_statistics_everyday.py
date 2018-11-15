# coding=utf-8

"""
每日销售统计 MODEL
"""

from django.db import models


class t_wish_distribution_sales_statistics_everyday(models.Model):

    s_date                  =   models.DateField(u'销售日期', blank=True, null=True)
    s_out_order_num         =   models.IntegerField(u'出单数', max_length=11, blank=True, null=True)
    s_aproved_num           =   models.IntegerField(u'审核通过数', max_length=11, blank=True, null=True)
    s_sales_num             =   models.IntegerField(u'销售额', max_length=11, blank=True, null=True)
    s_week                  =   models.IntegerField(u'销售周', max_length=11, blank=True, null=True)

    class Meta:
        verbose_name = u'每日销售统计'
        verbose_name_plural = verbose_name
        ordering = ['-s_date']
        db_table = 't_wish_distribution_sales_statistics_everyday'
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)