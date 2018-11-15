#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_wish_pb_earnings_rep.py
 @time: 2018-07-23 10:26
"""

from django.db import models



class t_wish_pb_earnings_show(models.Model):
    id          = models.IntegerField(u'流水号', primary_key=True)
    product_id  = models.CharField(u'产品ID', max_length=25)
    pbgmv       = models.DecimalField(u'广告期间-销售额(¥)', max_digits=12, decimal_places=2)
    spend       = models.DecimalField(u'广告花费(¥)', max_digits=12, decimal_places=4)
    grossprofit = models.DecimalField(u'广告期间-毛利(¥)', max_digits=12, decimal_places=2)

    gmv         = models.DecimalField(u'非广告期间-销售额(¥)', max_digits=12, decimal_places=2)
    earning     = models.DecimalField(u'非广告期间-毛利(¥)', max_digits=12, decimal_places=2)
    totearning  = models.DecimalField(u'总毛利(¥)', max_digits=12, decimal_places=2)
    username    = models.CharField(u'操作人', max_length=25)

    class Meta:
        verbose_name = u'WISH收益报表'
        verbose_name_plural = u'WISH收益报表'
        db_table = 't_wish_pb_earnings_show'
        unique_together = ('username', 'product_id')
        ordering = ['-totearning']

    def __unicode__(self):
        return u'%s' % (self.product_id, )


class t_wish_pb_earnings_meta(models.Model):
    id         = models.IntegerField(u'流水号', primary_key=True)
    product_id = models.CharField(u'产品ID', max_length=25)
    p_date     = models.DateField(u'日期')
    date_flag  = models.SmallIntegerField(u'日期标识')
    gmv        = models.DecimalField(u'销售额', max_digits=8, decimal_places=2)
    spend      = models.DecimalField(u'花费', max_digits=8, decimal_places=4)
    grossprofit  = models.DecimalField(u'毛利额', max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = u'WISH收益报表元数据'
        verbose_name_plural = u'WISH收益报表元数据'
        db_table = 't_wish_pb_earnings_rep'

    def __unicode__(self):
        return u'%s' % (self.id, )

