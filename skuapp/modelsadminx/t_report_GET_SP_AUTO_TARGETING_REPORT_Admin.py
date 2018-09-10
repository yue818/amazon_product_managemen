# -*- coding: utf-8 -*-
from django.db import models
from django.utils.safestring import mark_safe

class t_report_GET_SP_AUTO_TARGETING_REPORT_Admin(object):
    # list_display=('id','ShopName','CampaignName','AdGroupName','CustomerSearchTerm','Keyword','MatchType','FirstDayofImpression','LastDayofImpression','Impressions','Clicks','CTR','TotalSpend','AverageCPC','ACoS','Currency','RefreshTime',)
    # list_filter = ('ShopName','CampaignName','AdGroupName','CustomerSearchTerm','Keyword')
    # search_fields =('id','ShopName','CampaignName','AdGroupName','CustomerSearchTerm','Keyword','MatchType','FirstDayofImpression','LastDayofImpression','Impressions','Clicks','CTR','TotalSpend','AverageCPC','ACoS','Currency','RefreshTime',)
    # readonly_fields =('id','ShopName','CampaignName','AdGroupName','CustomerSearchTerm','Keyword','MatchType','FirstDayofImpression','LastDayofImpression','Impressions','Clicks','CTR','TotalSpend','AverageCPC','ACoS','Currency','RefreshTime',)
    def show_roas(self, obj):
        if obj.TotalSpend != 0 and obj.TotalSpend is not None and obj.WeekProductSales is not None and obj.WeekProductSales.strip() != '':
            rt = round(float(obj.WeekProductSales) / float(obj.TotalSpend), 2)
        else:
            rt = ''
        return mark_safe(rt)
    show_roas.short_description = u'投入产出比(RoAS)'

    def show_ctr(self, obj):
        ctr_show = '%.2f' % float(obj.CTR.split('%')[0]) + '%'
        return mark_safe(ctr_show)
    show_ctr.short_description = u'点击率(CTR)'

    def show_week_conversion_rate(self, obj):
        week_conversion = '%.2f' % float(obj.WeekConversionRate.split('%')[0]) + '%'
        return mark_safe(week_conversion)
    show_week_conversion_rate.short_description = u'7天的转化率'



    list_display = ('id', 'LastDayofImpression', 'ShopName', 'CampaignName', 'AdGroupName', 'CustomerSearchTerm', 'Keyword', 'MatchType', 'Impressions', 'Clicks', 'show_ctr', 'TotalSpend', 'AverageCPC', 'ACoS', 'Currency', 'WeekOrdersPlaced', 'WeekProductSales', 'show_roas', 'show_week_conversion_rate', 'WeekSameSkuOrdered', 'WeekOtherSkuOrdered', 'WeekSameSkuSales', 'WeekOtherSkuSales', 'RefreshTime',)
    list_filter = ('ShopName', 'CampaignName', 'AdGroupName', 'CustomerSearchTerm', 'Keyword','LastDayofImpression','MatchType','WeekOrdersPlaced')
    search_fields = ('id', 'ShopName', 'CampaignName', 'AdGroupName', 'CustomerSearchTerm', 'Keyword', 'MatchType', 'FirstDayofImpression', 'LastDayofImpression', 'Impressions', 'Clicks', 'CTR', 'TotalSpend', 'AverageCPC', 'ACoS', 'Currency', 'RefreshTime',)
    readonly_fields = ('id', 'ShopName', 'CampaignName', 'AdGroupName', 'CustomerSearchTerm', 'Keyword', 'MatchType', 'FirstDayofImpression', 'LastDayofImpression', 'Impressions', 'Clicks', 'CTR', 'TotalSpend', 'AverageCPC', 'ACoS', 'Currency', 'RefreshTime',)
