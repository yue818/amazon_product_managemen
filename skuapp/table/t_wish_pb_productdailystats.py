#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_wish_pb_productdailystats.py
 @time: 2018-05-25 13:39
"""

from django.db import models

class thousandSeparatorField(models.CharField):
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if not value:
            return value
        try:
            return format(value, ',')
        except Exception:
            return value
    def get_prep_value(self, value):
        if not value:
            return value
        try:
            return int(value.replace(',', ''))
        except Exception:
            return value

class t_wish_pb_productdailystats(models.Model):
    id					= models.AutoField(u'流水号', primary_key=True)
    campaign_id			= models.CharField(u'活动ID', max_length=25, blank=True, null=True)
    product_id			= models.CharField(u'产品ID', max_length=25, blank=True, null=True)
    p_date              = models.DateField(u'日期')
    date_flag           = models.SmallIntegerField(u'数据标识')
    impressions		    = thousandSeparatorField(u'总曝光量', max_length=20, blank=True, null=True)
    paid_impressions	= thousandSeparatorField(u'付费曝光量', max_length=20, blank=True, null=True)
    spend				= models.DecimalField(u'花费', max_digits=6, decimal_places=2)
    sales				= models.IntegerField(u'订单数')
    gmv					= models.DecimalField(u'销售额', max_digits=8, decimal_places=2)
    updatetime			= models.DateTimeField(u'更新时间')

    class Meta:
        verbose_name = u'Wish广告业绩'
        verbose_name_plural = u'Wish广告业绩'
        db_table = 't_wish_pb_productdailystats'
        ordering = ['-p_date']

    def __unicode__(self):
        return u'%s' % (self.product_id, )