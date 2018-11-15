# -*- coding: utf-8 -*-
from django.db import models

class t_shop_amazon_india(models.Model):
    ShopName = models.CharField(u'店铺简称', max_length=64)
    ShopUserName = models.CharField(u'店长姓名', max_length=64)
    UserAdress = models.CharField(u'详细地址', max_length=200)
    UserPhoneArea = models.CharField(u'电话区号', max_length=12, blank=True, null=True)
    Mobile = models.CharField(u'手机号码', max_length=32)
    PostCode = models.CharField(u'邮编', max_length=32)
    Email = models.CharField(u'邮箱', max_length=64, blank=True, null=True)
    CountryCode = models.CharField(u'国家代码', max_length=20)
    Company = models.CharField(u'公司名称', max_length=100)
    Province = models.CharField(u'州/省', max_length=64, blank=True, null=True)
    City = models.CharField(u'城市', max_length=64)
    UpdateTime = models.DateTimeField(u'更新时间', blank=True, null=True)
    UserPhoneTel = models.CharField(u'电话号码', max_length=32)
    UserPhoneExt = models.CharField(u'分机号码', max_length=12, blank=True, null=True)

    class Meta:
        verbose_name = u'Amazon印度店铺管理'
        verbose_name_plural = u'Amazon印度店铺管理'
        db_table = 't_shop_amazon_india'
    def __unicode__(self):
        return str(self.id)