# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models

class t_wish_honorShop(models.Model):
    ip                      =   models.CharField(u'店铺IP',max_length=32,blank = True,null = True)
    ShopName                =   models.CharField(u'店铺名称',max_length=32,blank = True,null = True)
    seller                  =   models.CharField(u'销售员',max_length=32,blank = True,null = True)
    PlatformName            =   models.CharField(u'平台', max_length=32, blank=True, null=True)
    class Meta:
        verbose_name = u'Wish诚信店铺'
        verbose_name_plural = u' Wish诚信店铺'
        db_table = 't_config_mstsc'
        ordering = ['id']

    def __unicode__(self):
        return u'ShopName:%s' % (self.ShopName)