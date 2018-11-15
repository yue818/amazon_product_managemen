#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_wish_pb_finance_rep.py
 @time: 2018-07-14 13:33
"""

from django.db import models

class t_wish_pb_finance_rep(models.Model):
    id          = models.IntegerField(u'流水号', primary_key=True)
    shopname    = models.CharField(u'店铺简称', max_length=50, blank=True, null=True)
    createuser  = models.CharField(u'广告创建人', max_length=20, blank=True, null=True)
    storename   = models.CharField(u'仓库类别', max_length=50, blank=True, null=True)
    p_date      = models.DateField(u'日期')
    impressions = models.IntegerField(u'总曝光量',)
    paid_impressions = models.IntegerField(u'付费曝光量',)
    spend = models.DecimalField(u'花费', max_digits=10, decimal_places=4)
    sales = models.IntegerField(u'订单数')
    gmv = models.DecimalField(u'销售额', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = u'WISH广告费用报表'
        verbose_name_plural = u'WISH广告费用报表'
        db_table = 't_wish_pb_finance_rep'
        ordering = ['-p_date', 'shopname']

    def __unicode__(self):
        return u'%s' % (self.createuser, )