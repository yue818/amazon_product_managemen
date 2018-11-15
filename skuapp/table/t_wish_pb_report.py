#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_wish_pb_report.py
 @time: 2018-06-16 15:09
"""
from django.db import models

class t_wish_pb_report(models.Model):
    id          = models.IntegerField(u'流水号', primary_key=True)
    createuser  = models.CharField(u'广告创建人', max_length=20, blank=True, null=True)
    spend       = models.DecimalField(u'花费', max_digits=10, decimal_places=2)
    gmv         = models.DecimalField(u'销售额', max_digits=10, decimal_places=2)
    spend_gmv   = models.DecimalField(u'AS(%)', max_digits=8, decimal_places=2)
    flag        =models.CharField(u'操作人标识', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = u'WISH广告统计报表'
        verbose_name_plural = u'WISH广告统计报表'
        db_table = 't_wish_pb_report'
        unique_together = ('flag', 'createuser')

    def __unicode__(self):
        return u'%s' % (self.createuser, )


class t_wish_pb_report_meta(models.Model):
    id         = models.IntegerField(u'流水号', primary_key=True)
    createuser = models.CharField(u'广告创建人', max_length=20, blank=True, null=True)
    product_id = models.CharField(u'产品ID', max_length=25, blank=True, null=True)
    p_date     = models.DateField(u'日期')
    spend      = models.DecimalField(u'花费', max_digits=6, decimal_places=2)
    gmv        = models.DecimalField(u'销售额', max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = u'WISH广告报表元数据'
        verbose_name_plural = u'WISH广告报表元数据'
        db_table = 'v_t_wish_pb_report'

    def __unicode__(self):
        return u'%s' % (self.id, )