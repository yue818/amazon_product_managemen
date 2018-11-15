# -*- coding: utf-8 -*-
from django.db import models
#from public import *
class t_report_GET_SP_AUTO_TARGETING_REPORT_(models.Model):
    # ShopName                =   models.CharField(u'店铺名称',max_length=32,blank = True,null = True)
    # CampaignName            =   models.CharField(max_length=32,blank = True,null = True)
    # AdGroupName             =   models.CharField(max_length=32,blank = True,null = True)
    # CustomerSearchTerm      =   models.CharField(max_length=64,blank = True,null = True)
    # Keyword                 =   models.CharField(max_length=64,blank = True,null = True)
    # MatchType               =   models.CharField(max_length=32,blank = True,null = True)
    # FirstDayofImpression    =   models.CharField(max_length=32,blank = True,null = True)
    # LastDayofImpression     =   models.CharField(max_length=32,blank = True,null = True)
    # Impressions             =   models.CharField(max_length=32,blank = True,null = True)
    # Clicks                  =   models.CharField(max_length=32,blank = True,null = True)
    # CTR                     =   models.CharField(max_length=32,blank = True,null = True)
    # TotalSpend              =   models.CharField(max_length=32,blank = True,null = True)
    # AverageCPC              =   models.CharField(max_length=32,blank = True,null = True)
    # ACoS                    =   models.CharField(max_length=32,blank = True,null = True)
    # Currency                =   models.CharField(max_length=32,blank = True,null = True)
    # RefreshTime             =   models.DateTimeField(u'刷新时间',blank = True,null = True)

    ShopName = models.CharField(u'店铺名称', max_length=32, blank=True, null=True)
    CampaignName = models.CharField(u'广告活动名称', max_length=32, blank=True, null=True)
    AdGroupName = models.CharField(u'广告组名称', max_length=32, blank=True, null=True)
    CustomerSearchTerm = models.CharField(u'客户搜索词', max_length=64, blank=True, null=True)
    Keyword = models.CharField(u'关键字', max_length=64, blank=True, null=True)
    MatchType = models.CharField(u'匹配类型', max_length=32, blank=True, null=True)
    FirstDayofImpression = models.CharField(u'开始日期', max_length=32, blank=True, null=True)
    LastDayofImpression = models.DateTimeField(u'日期', max_length=32, blank=True, null=True)
    Impressions = models.CharField(u'展现量', max_length=32, blank=True, null=True)
    Clicks = models.CharField(u'点击量', max_length=32, blank=True, null=True)
    CTR = models.CharField(u'点击率(CTR)', max_length=32, blank=True, null=True)
    TotalSpend = models.CharField(u'花费', max_length=32, blank=True, null=True)
    AverageCPC = models.CharField(u'每次点击成本(CPC)', max_length=32, blank=True, null=True)
    ACoS = models.CharField(u'广告成本销售比(ACoS)', max_length=32, blank=True, null=True)
    Currency = models.CharField(u'货币', max_length=32, blank=True, null=True)
    WeekOrdersPlaced = models.IntegerField(u'7天总订单数(#)', max_length=32, blank=True, null=True)
    WeekProductSales = models.CharField(u'7天总销售额($)', max_length=32, blank=True, null=True)
    WeekConversionRate = models.CharField(u'7天的转化率', max_length=32, blank=True, null=True)
    WeekSameSkuOrdered = models.CharField(u'7天内广告SKU销售量(#)', max_length=32, blank=True, null=True)
    WeekOtherSkuOrdered = models.CharField(u'7天内其他SKU销售量(#)', max_length=32, blank=True, null=True)
    WeekSameSkuSales = models.CharField(u'7天内广告SKU销售额($)', max_length=32, blank=True, null=True)
    WeekOtherSkuSales = models.CharField(u'7天内其他SKU销售额($)', max_length=32, blank=True, null=True)
    RefreshTime = models.DateTimeField(u'刷新时间', blank=True, null=True)

    class Meta:
        verbose_name = u'广告投放报告(Amazon)'
        verbose_name_plural = u'广告投放报告(Amazon)'
        db_table = 't_report_new_get_sp_auto_targeting_report_'
        ordering = ['-id']
    def __unicode__(self):
        return u'%s'%(self.id)
#list_display=('id','ShopName','CampaignName','AdGroupName','CustomerSearchTerm','Keyword','MatchType','FirstDayofImpression','LastDayofImpression','Impressions','Clicks','CTR','TotalSpend','AverageCPC','ACoS','Currency','RefreshTime',)