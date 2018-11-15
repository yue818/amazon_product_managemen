# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models


class t_wish_screenshot(models.Model):
    shopNameOfficial = models.CharField(u'店铺名', max_length=32, blank=True, null=True)
    seller                  =   models.CharField(u'店长/销售员',max_length=32,blank = True,null = True)
    Published           =   models.CharField(u'刊登员',max_length=32,blank = True,null = True)
    Operators           =   models.CharField(u'运营人员',max_length=32,blank = True,null = True)
    screenshotUrl_firstPage  = models.CharField(u'首页截图', max_length=64, blank=True, null=True)
    screenshotUrl_orderPage = models.CharField(u'订单截图', max_length=64, blank=True, null=True)
    updateTime = models.CharField(u'更新时间', max_length=16, blank=True, null=True)
    ip         =models.CharField(u'ip', max_length=32, blank=True, null=True)
    remark=     models.CharField(u'备注', max_length=64, blank=True, null=True)

    class Meta:
        verbose_name = u'Wish店铺截图'
        verbose_name_plural = u' Wish店铺截图'
        db_table = 't_wish_screenshot'
        ordering = ['shopNameOfficial']

    def __unicode__(self):
        return u'id:%s' % (self.id)