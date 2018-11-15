#-*-coding:utf-8-*-
"""  
 @desc:  服装体系销售统计
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_report_sales_clothingsystem.py
 @time: 2018-04-09 8:47
"""

from django.db import models

class t_report_sales_clothingsystem(models.Model):

    TimeName    =   models.CharField(u'销售日期', max_length=10, blank=False, null=False)
    TimeType    =   models.PositiveSmallIntegerField(u'日期种类', blank=False, null=False)
    PlatformName=   models.CharField(u'销售平台', max_length=16, blank=False, null=False)
    ProductID   =   models.CharField(u'产品ID', max_length=100, blank=True, null=True)
    MainSKU     =   models.CharField(u'主SKU', max_length=32, blank=True, null=True)
    ShopName    =   models.CharField(u'店铺名称', max_length=50, blank=True, null=True)
    BmpUrl      =   models.CharField(u'图片路径', max_length=255, blank=True, null=True)
    SalesVolume =   models.IntegerField(u'销售量', max_length=11, blank=False, null=False)
    UpdateTime  =   models.DateTimeField(u'更新时间', auto_now=True, blank=False, null=False)

    class Meta:
        verbose_name = u'服装体系销售统计'
        verbose_name_plural = verbose_name
        ordering = ['-TimeName']
        db_table = 't_report_sales_clothingsystem'
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)