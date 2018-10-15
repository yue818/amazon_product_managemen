#-*-coding:utf-8-*-
from django.db import models
"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_config_apiurl_amazon.py
 @time: 2017/12/18 15:34
"""
from .public import *


class t_config_shop_alias(models.Model):
    ShopName = models.CharField(u'卖家简称', max_length=64, blank=True, null=True)
    ShopAlias = models.CharField(u'店铺名', max_length=64, blank=True, null=True)
    PlatformName = models.CharField(u'平台名', max_length=32, blank=True, null=True)
    ShopType = models.CharField(u'店铺类型',  choices=getChoices(ChoiceAmazonShopType), max_length=1, default=1, blank=True, null=True)
    ShopStatus = models.CharField(u'店铺状态', choices=getChoices(ChoiceAmazonShopStatus), max_length=1, default=1, blank=True, null=True)
    Remark = models.CharField(u'备注', max_length=255, blank=True, null=True)
    CreateUser = models.CharField(u'采集人', max_length=32, blank=True, null=True)
    CreateTime = models.DateTimeField(u'采集时间', blank=True, null=True)
    UpdateUser = models.CharField(u'更新人', max_length=32, blank=True, null=True)
    UpdateTime = models.DateTimeField(u'更新时间', blank=True, null=True)

    class Meta:
        verbose_name = u'Amazon卖家店铺配置表'
        verbose_name_plural = verbose_name
        db_table = 't_config_shop_alias'
        ordering = ['ShopName']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)