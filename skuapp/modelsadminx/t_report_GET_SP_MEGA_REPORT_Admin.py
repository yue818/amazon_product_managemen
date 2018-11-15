# -*- coding: utf-8 -*-
from django.db import models
from urllib import urlencode
from django.utils.safestring import mark_safe
from skuapp.table.t_online_shopinfo_amazon import t_online_shopinfo_amazon


class t_report_GET_SP_MEGA_REPORT_Admin(object):

    def show_keyword(self,obj):
        rt = u'<a href = "/Project/admin/skuapp/t_report_get_sp_auto_targeting_report_/?%s">%s</a>'%(urlencode({'_p_ShopName__exact':obj.ShopName,'_p_CampaignName__exact':obj.CampaignName,'_p_AdGroupName__exact':obj.AdGroupName}),obj.Keyword)
        return mark_safe(rt)
    show_keyword.short_description = u"Keyword"
    
    def show_image_url(self,obj):
        rt = ''
        t_online_shopinfo_amazon_objs = t_online_shopinfo_amazon.objects.filter(seller_sku = obj.AdvertisedSKU)
        if t_online_shopinfo_amazon_objs.exists():
            rt =  '<img src="%s"  width="120" height="120"  alt = "%s"  title="%s"  />  '%(t_online_shopinfo_amazon_objs[0].image_url,t_online_shopinfo_amazon_objs[0].image_url,t_online_shopinfo_amazon_objs[0].image_url)
        return mark_safe(rt)
    show_image_url.short_description = u'图片'

    list_display=('id','show_image_url','AdvertisedSKU','ShopName','StartDate','EndDate','show_keyword','MatchType','TotalSpend','Clicks','Impressions','AverageCPC','CTR','WeekOrderSales','WeekOrderPlaced','WeekRate')
    list_filter = ('StartDate','EndDate','WeekOrderPlaced')
    search_fields = ('id','AdvertisedSKU','ShopName','StartDate','EndDate','Keyword','TotalSpend','Clicks','Impressions','AverageCPC','CTR','WeekOrderSales','WeekOrderPlaced','WeekRate')
    readonly_fields = ('id','AdvertisedSKU','StartDate','EndDate','Keyword','TotalSpend','Clicks','Impressions','AverageCPC','CTR','WeekOrderSales','WeekOrderPlaced','WeekRate')
