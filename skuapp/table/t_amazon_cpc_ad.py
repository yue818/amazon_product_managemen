# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_cpc_ad.py
 @time: 2018-05-15 19:50
 ##
"""  

from django.db import models
from .public import *


class t_amazon_cpc_ad(models.Model):

    shop_name = models.CharField(u'店铺名', max_length=100, blank=True, null=True)
    shop_site = models.CharField(u'站点', max_length=5, blank=True, null=True)
    seller_sku = models.CharField(u'店铺SKU', max_length=64, blank=True, null=True)
    asin = models.CharField(u'ASIN值', max_length=64, blank=True, null=True)
    title = models.CharField(u'标题', max_length=255, blank=True, null=True)
    image_url = models.ImageField(u'图片', max_length=255, blank=True, null=True)
    score = models.FloatField(u'评分', max_length=5, null=True)
    review_cnt = models.IntegerField(u'Review量', max_length=10, blank=True, null=True)
    price = models.FloatField(u'价格', max_length=10, null=True)
    quantity = models.CharField(u'库存', max_length=10, null=True)
    is_fba = models.IntegerField(u'是否FBA', max_length=1, blank=True, null=True)
    create_date = models.DateTimeField(u'创建日期', blank=True, null=True)
    on_sale_date = models.DateTimeField(u'开售日期', blank=True, null=True)
    profit_rate = models.FloatField(u'利润率', max_length=5, blank=True, null=True)
    # orders_3days = models.IntegerField(u'3天销量', max_length=5, blank=True, null=True)
    orders_7days = models.IntegerField(u'7天销量', max_length=5, blank=True, null=True)
    orders_15days = models.IntegerField(u'15天销量', max_length=5, blank=True, null=True)
    orders_30days = models.IntegerField(u'30天销量', max_length=5, blank=True, null=True)
    orders_total = models.IntegerField(u'总销量', max_length=5, blank=True, null=True)
    product_state = models.CharField(u'销售备注', choices=getChoices(CpcProductState), max_length=5, blank=True, null=True)
    inventory = models.IntegerField(u'可售库存', max_length=5, blank=True, null=True)
    sale_remark = models.CharField(u'销售备注1', max_length=1000, blank=True, null=True)
    link_orders = models.IntegerField(u'链接出单量', max_length=5, blank=True, null=True)
    ad_orders = models.IntegerField(u'广告出单量', max_length=5, blank=True, null=True)
    link_sales = models.FloatField(u'链接销售额', max_length=5, blank=True, null=True)
    ad_sales = models.FloatField(u'广告销售额', max_length=5, blank=True, null=True)
    ad_cost = models.FloatField(u'广告花费', max_length=5, blank=True, null=True)
    expose_cnt = models.IntegerField(u'曝光量', max_length=5, blank=True, null=True)
    click_cnt = models.IntegerField(u'点击量', max_length=5, blank=True, null=True)
    ad_remark = models.CharField(u'广告备注', max_length=1000, blank=True, null=True)
    operation_record = models.CharField(u'操作记录', max_length=255, blank=True, null=True)
    product_id_type = models.CharField(u'product_id_type', max_length=64, blank=True, null=True)
    Status = models.FileField(u'Status', max_length=32, blank=True, null=True)
    Parent_asin = models.CharField(u'Parent_asin', max_length=64, blank=True, null=True)
    afn_listing_exists = models.CharField(u'FBA链接', max_length=32, blank=True, null=True)
    afn_warehouse_quantity = models.IntegerField(u'FBA库存', max_length=32, blank=True, null=True)
    afn_fulfillable_quantity = models.IntegerField(u'可售数', max_length=32, blank=True, null=True)
    afn_unsellable_quantity = models.IntegerField(u'不可售数', max_length=32, blank=True, null=True)
    afn_reserved_quantity = models.IntegerField(u'预留数', max_length=31, blank=True, null=True)
    afn_total_quantity = models.IntegerField(u'总数量', max_length=32, blank=True, null=True)
    per_unit_volume = models.CharField(u'单位体积', max_length=32, blank=True, null=True)
    afn_inbound_working_quantity = models.IntegerField(u'待入库数', max_length=32, blank=True, null=True)
    afn_inbound_shipped_quantity = models.IntegerField(u'在途数', max_length=32, blank=True, null=True)
    afn_inbound_receiving_quantity = models.IntegerField(u'正在接收数', max_length=32, blank=True, null=True)
    RefreshTime = models.DateTimeField(u'刷新时间', blank=True, null=True)
    sku = models.CharField(u'商品SKU', max_length=64, blank=True, null=True)

    class Meta:
        verbose_name = u'AMZ listing管理'
        verbose_name_plural = verbose_name
        db_table = 't_amazon_cpc_ad'
        ordering = ['-Parent_asin', 'product_id_type']

    def __unicode__(self):
        return u'%s' % self.id



# class t_amazon_cpc_ad(models.Model):
#     ShopName = models.CharField(u'店铺名', max_length=32, blank=True, null=True)
#     AdvertisedSKU = models.CharField(u'SKU', max_length=64, blank=True, null=True)
#     StartDate = models.DateTimeField(u'开始日期', blank=True, null=True)
#     EndDate = models.DateTimeField(u'结束日期', blank=True, null=True)
#     Clicks = models.CharField(u'点击量', max_length=32, blank=True, null=True)
#     Impressions = models.CharField(u'Impression量', max_length=32, blank=True, null=True)
#     CTR = models.CharField(u'CTR', max_length=32, blank=True, null=True)
#     TotalSpend = models.CharField(u'总花费', max_length=32, blank=True, null=True)
#     AverageCPC = models.CharField(u'CPC', max_length=32, blank=True, null=True)
#     Currency = models.CharField(max_length=32, blank=True, null=True)
#     DayOrdersPlaced = models.CharField(u'日订单', max_length=32, blank=True, null=True)
#     DayOrderedProductSales = models.CharField(u'日销售额', max_length=32, blank=True, null=True)
#     DayConversionRate = models.CharField(u'日转化率', max_length=32, blank=True, null=True)
#     ShopSite  = models.CharField(u'站点', max_length=5, blank=True, null=True)
#
#     class Meta:
#         verbose_name = u'AMAZON CPC广告'
#         verbose_name_plural = verbose_name
#         db_table = 't_amazon_ad_report'
#
#     def __unicode__(self):
#         return u'%s' % self.id
