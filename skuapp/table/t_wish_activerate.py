#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: changyang  
 @site: 
 @software: PyCharm
 @file: t_wish_activerate.py
 @time: 2018-08-20 15:19
"""

from django.db import models


PdType = [(1, u'周'), (2, u'月')]

class t_wish_activerate(models.Model):
    id          =   models.AutoField(u'流水号', primary_key=True)
    PeriodNO    =   models.CharField(u'周期序号', max_length=7, blank=False, null=False)
    PeriodType  =   models.PositiveSmallIntegerField(u'周期种类', choices=PdType, blank=False, null=False)
    PeriodStart =   models.DateField(u'开始时间', blank=True, null=True)
    PeriodEnd   =   models.DateField(u'结束时间', blank=True, null=True)
    UploadCnt   =   models.IntegerField(u'铺货链接数', blank=True, null=True)
    OrderCnt    =   models.IntegerField(u'出单链接数', blank=True, null=True)
    ActiveRate  =   models.DecimalField(u'激活率', max_digits=6, decimal_places=2, blank=True, null=True)
    Sales       =   models.DecimalField(u'销售额($)', max_digits=10, decimal_places=2, blank=True, null=True)
    UpdateTime  =   models.DateTimeField(u'更新时间', blank=False, null=False)

    class Meta:
        verbose_name = u'铺货激活率'
        verbose_name_plural = verbose_name
        ordering = ['-id']
        db_table = 't_wish_activerate'
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)