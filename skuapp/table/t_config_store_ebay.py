# -*- coding: utf-8 -*-

from django.db import models
from public import *

class t_config_store_ebay(models.Model):

    storeName = models.CharField(u'店铺名称', max_length=64, blank=True, null=False)
    accountID = models.CharField(u'店铺ID', max_length=63, blank=True, null=False)
    accountPassword = models.CharField(u'店铺密码', max_length=31, blank=True, null=False)
    appID = models.CharField(u'账号注册的信息', max_length=64, blank=True, null=False)
    token = models.CharField(u'API接口信息', max_length=1023, blank=True, null=False)
    storeOwner = models.CharField(u'账号管理员', max_length=31, blank=True, null=False)
    paypalAccountLarge = models.CharField(u'大额收款邮箱', max_length=63, blank=True, null=False)
    paypalAccountHalf = models.CharField(u'小额收款邮箱', max_length=63, blank=True, null=False)
    status = models.CharField(u'账号状态', max_length=16, blank=True, null=False)
    siteID = models.CharField(u'站点ID',choices=getChoices(ChoiceisEbaySiteID), max_length=8, blank=True, null=False)
    description_prefix_file = models.CharField(u'描述1', max_length=256, blank=True, null=False)
    description_postfox_file = models.CharField(u'描述2', max_length=256, blank=True, null=False)
    shopSkuRule = models.CharField(u'店铺特征码', max_length=64, blank=True, null=False)
    tokenExpireTime = models.DateTimeField(u'API有效期限', blank=True, null=False)
    ShopName = models.CharField(u'本地账号店铺名称', max_length=64, blank=True, null=False)
    refresh_token = models.CharField(u'OAuth刷新Token', max_length=2400, blank=True, null=False)
    OAuthToken = models.CharField(u'OAuthToken', max_length=2048, blank=True, null=False)
    OAuthExpireTime = models.DateTimeField(u'OAuth过期时间', blank=True, null=False)
    refresh_time = models.DateTimeField(u'refresh_token获取时间', blank=True, null=False)

    class Meta:
        verbose_name=u'ebay站点配置表'
        verbose_name_plural=verbose_name
        db_table = 't_config_store_ebay'
        ordering = ['refresh_time']
    def __unicode__(self):
        return u'id:%s' % (self.id)
