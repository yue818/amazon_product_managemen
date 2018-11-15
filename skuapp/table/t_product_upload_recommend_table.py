# -*- coding: utf-8 -*-
from django.db import models
from public import *


class t_product_upload_recommend_table(models.Model):
    MainSKU            =   models.CharField(u'主SKU',max_length=64,blank = True,null = True)
    PICURL             =   models.CharField(u'图片URL',max_length=255,blank = True,null = True)
    CreateTime         =   models.DateField(u'开发时间',max_length=64,blank = True,null = True)
    Order7days         =   models.IntegerField(u'7天订单数',max_length=64,blank = True,null = True)
    Nub                =   models.IntegerField(u'链接数',max_length=64,blank = True,null = True)
    PlatformName       =   models.CharField(u'平台',max_length=31,blank = True,null = True)
    SKU                =   models.CharField(u'SKU',max_length=64,blank = True,null = True)
    UpLoad_Nub         =   models.IntegerField(u'铺货链接数',max_length=64,blank = True,null = True)

    class Meta:

        verbose_name=u'产品铺货推荐'
        verbose_name_plural=verbose_name
        db_table = 't_product_upload_recommend_table'
        ordering = ['-Order7days']

    def __unicode__(self):
        return u'%s'%(self.id)