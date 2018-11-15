# -*- coding: utf-8 -*-
from django.db import models
from django.utils.safestring import mark_safe
#amazon 广告活动业绩报告
class t_report_GET_SP_MEGA_REPORT_(models.Model):

    ShopName        =   models.CharField(u'店铺名称',max_length=32,blank = True,null = True)
    CampaignName    =   models.CharField(max_length=32,blank = True,null = True)
    AdGroupName     =   models.CharField(max_length=32,blank = True,null = True)
    AdvertisedSKU   =   models.CharField(u'AdvertisedSKU',max_length=32,blank = True,null = True)
    Keyword         =   models.CharField(u'Keyword',max_length=64,blank = True,null = True)
    MatchType       =   models.CharField(max_length=32,blank = True,null = True)
    StartDate       =   models.DateTimeField(u'Start Date',blank = True,null = True)
    EndDate         =   models.DateTimeField(u'End Date',blank = True,null = True)
    Clicks          =   models.CharField(u'Sum of Clicks',max_length=32,blank = True,null = True)
    Impressions     =   models.CharField(mark_safe(u'Sum of<br>Impression'),max_length=32,blank = True,null = True)
    CTR             =   models.CharField(mark_safe(u'Click Through<br>Rate'),max_length=32,blank = True,null = True)
    TotalSpend      =   models.CharField(mark_safe(u'Sum of<br>Total Spend'),max_length=32,blank = True,null = True)
    AverageCPC      =   models.CharField(mark_safe(u'Average Cost<br>Per Click'),max_length=32,blank = True,null = True)
    #Currency        =   models.CharField(max_length=32,blank = True,null = True)
    WeekOrderSales      =   models.CharField(mark_safe(u'Product Sales<br>within 1 Week of Click'),max_length=32,blank = True,null = True) #1-week Ordered Product Sales
    WeekOrderPlaced     =   models.IntegerField(mark_safe(u'Orders Placed<br>within 1 Week of Click'),blank = True,null = True) #1-week Orders Placed
    WeekRate        =   models.CharField(u'Conversion Rate',max_length=32,blank = True,null = True) #1-week Conversion Rate
    #RefreshTime     =   models.DateTimeField(u'刷新时间',blank = True,null = True)

    class Meta:
        verbose_name=u'广告活动业绩报告(Amazon)'
        verbose_name_plural=u'广告活动业绩报告(Amazon)'
        db_table = 't_report_GET_SP_MEGA_REPORT_'
        ordering =  ['id']
    def __unicode__(self):
        return u'%s'%(self.id)
