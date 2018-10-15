#-*-coding:utf-8-*-
u"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_online_info_wish_low_inventory.py
 @time: 2018/9/18 14:42
"""
from django.db import models
from skuapp.table.public import *

class t_online_info_wish_low_inventory(models.Model):
    PlatformName = models.CharField(u'平台', choices=getChoices(ChoicePlatformName), max_length=16, blank=True, null=True)
    ProductID = models.CharField(u'ProductID', max_length=32, blank=True, null=True)
    ShopIP = models.CharField(u'店铺IP', max_length=32, blank=True, null=True)
    ShopName = models.CharField(u'店铺名称', max_length=32, blank=True, null=True)
    Title = models.CharField(u'Title', max_length=255, blank=True, null=True)
    SKU = models.CharField(u'商品SKU', max_length=32, blank=True, null=True)
    ShopSKU = models.CharField(u'店铺SKU', max_length=32, blank=True, null=True)
    Price = models.CharField(u'价格', max_length=32, blank=True, null=True)
    Quantity = models.IntegerField(u'在线库存', blank=True, null=True)
    filtervalue = models.PositiveSmallIntegerField(u'低库存过滤值', blank=True, null=True)  # 默认为 1  0或1：显示；-1 不显示
    RefreshTime = models.DateTimeField(u'同步时间', blank=True, null=True)
    Status = models.CharField(u'Status', choices=getChoices(ChoiceStatus_wish), max_length=32, blank=True, null=True)
    Image = models.CharField(u'图片', max_length=200, blank=True, null=True)
    ReviewState = models.CharField(u'Review State', choices=getChoices(ChoiceReviewState), max_length=8, blank=True, null=True)
    OfWishes = models.CharField(u'Of Wishes', max_length=8, blank=True, null=True)
    OfSales = models.CharField(u'Of Sales', max_length=8, blank=True, null=True)
    LastUpdated = models.CharField(u'LastUpdated', max_length=32, blank=True, null=True)
    DateUploaded = models.CharField(u'DateUploaded', max_length=32, blank=True, null=True)
    Shipping = models.CharField(u'运费', max_length=32, blank=True, null=True)
    Color = models.CharField(u'颜色', max_length=32, blank=True, null=True)
    Size = models.CharField(u'尺寸', max_length=32, blank=True, null=True)
    msrp = models.CharField(u'标签价', max_length=32, blank=True, null=True)
    ShippingTime = models.CharField(u'运输时间', max_length=32, blank=True, null=True)
    ExtraImages = models.TextField(u'副图', blank=True, null=True)
    Description = models.CharField(u'描述', max_length=255, blank=True, null=True)
    Tags = models.CharField(u'标签', max_length=255, blank=True, null=True)
    ParentSKU = models.CharField(u'ParentSKU', max_length=31, blank=True, null=True)
    MainSKU = models.CharField(u'主SKU', max_length=16, blank=True, null=True)
    ShopSKUImage = models.CharField(u'变种图', max_length=200, blank=True, null=True)
    GoodsStatus = models.CharField(u'商品状态', max_length=31, blank=True, null=True)
    DEExpressShipping = models.CharField(u'德国仓运费', max_length=4, blank=True, null=True)
    DEExpressInventory = models.CharField(u'德国仓库存', max_length=8, blank=True, null=True)
    GBExpressShipping = models.CharField(u'英国仓运费', max_length=4, blank=True, null=True)
    GBExpressInventory = models.CharField(u'英国仓库存', max_length=8, blank=True, null=True)
    USExpressShipping = models.CharField(u'美国仓运费', max_length=4, blank=True, null=True)
    USExpressInventory = models.CharField(u'美国仓库存', max_length=8, blank=True, null=True)
    seller = models.CharField(u'销售员', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name=u'Wish 低库存'
        verbose_name_plural=verbose_name
        db_table = 't_online_info_wish_low_inventory'

    def __unicode__(self):
        return u'--'



