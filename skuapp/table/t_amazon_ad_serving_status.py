# -*- coding: utf-8 -*-
from django.db import models
from public import *


class t_amazon_ad_serving_status(models.Model):
    ShopName       =   models.CharField(u'店铺简称',max_length=63,blank = True,null = True)
    ShopType       =   models.CharField(u'店铺类型',max_length=15,blank = True,null = True)
    AccountName    =   models.CharField(u'店铺账号',max_length=31,blank = True,null = True)
    ShopSite       =   models.CharField(u'站点',choices=getChoices(ChoiceSite),max_length=31,blank = True,null = True)
    AdServingStatus=   models.CharField(u'广告投放状态',max_length=15,blank = True,null = True)
    Remarks        =   models.CharField(u'备注',max_length=255,blank = True,null = True)

    class Meta:
        verbose_name=u'亚马逊广告统计'
        verbose_name_plural=verbose_name
        db_table = 't_amazon_ad_serving_status'
        ordering =  ['-id']
        app_label  = 'skuapp'
    def __unicode__(self):
        return u'%s'%(self.id)