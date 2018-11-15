# -*- coding: utf-8 -*-
from django.db import models
from public import *


class t_report_sales_daily(models.Model):
    OrderDay        =   models.DateField(u'订单日期',blank = True,null = True)
    PlatformName    =   models.CharField(u'平台名称',max_length=16,blank = True,null = True)
    ProductID       =   models.CharField(u'产品ID',max_length=100,blank = True,null = True)
    MainSKU         =   models.CharField(u'主SKU',max_length=32,blank = True,null = True)
    ShopName        =   models.CharField(u'店铺名称',max_length=50,blank = True,null = True)
    SKU             =   models.CharField(u'商品SKU',max_length=100,blank = True,null = True)
    ShopSKU         =   models.CharField(u'店铺SKU',max_length=500,blank = True,null = True)
    BmpUrl          =   models.URLField(u'图片链接',blank = True,null = True)
    SalesVolume     =   models.PositiveSmallIntegerField(u'日销售量',max_length=11,blank = True,null = True)
    Updatetime      =   models.DateTimeField(u'更新时间',blank = True,null = True)


    class Meta:
        verbose_name=u'店铺SKU日销量'
        verbose_name_plural=verbose_name
        db_table = 't_report_sales_daily'
        ordering = ['-OrderDay']
    def __unicode__(self):
        return u'id:%s'%(self.id)