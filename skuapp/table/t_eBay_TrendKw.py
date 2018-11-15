#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_eBay_TrendKw.py
 @time: 2018-08-03 9:06
"""

from django.db import models

class t_eBay_TrendKw(models.Model):
    id = models.AutoField(u'流水号', primary_key=True)

    TrendDate   = models.CharField(u'趋势日期', max_length=20, blank=True, null=True)
    TrendSite   = models.CharField(u'站点', max_length=10, blank=True, null=True)
    TrendTitle  = models.CharField(u'趋势主题', max_length=100, blank=True, null=True)
    TrendDesc   = models.TextField(u'趋势描述', blank=True, null=True)
    BurstKw     = models.CharField(u'相关关键词', max_length=255, blank=True, null=True)
    TrendSearches = models.CharField(u'趋势活跃量', max_length=10, blank=True, null=True)
    ImgUrl      = models.CharField(u'图片地址', max_length=255, blank=True, null=True)
    Updatetime  = models.DateTimeField(u'更新时间',)


    class Meta:
        verbose_name = u'eBay趋势关键词'
        verbose_name_plural = verbose_name
        db_table = 't_ebay_trendkw'
        ordering = ['-TrendDate']

    def __unicode__(self):
        return u'%s' % (self.id)