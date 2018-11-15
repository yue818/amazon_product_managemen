# -*- coding: utf-8 -*-
from django.db import models


class amzon_india_price_config(models.Model):
    id                 =   models.IntegerField(u'ID',blank = True,primary_key=True)
    ShopName           =   models.CharField(u'店铺名',max_length=200,blank = True,null = True)
    EXCHANGE_RATE      =   models.CharField(u'汇率',max_length=200,blank = True,null = True)
    PROFIT_RATE        =   models.CharField(u'利润率',max_length=200,blank = True,null = True)
    TRACK_PRICE_ELEC   =   models.CharField(u'gati运费(带电)',max_length=200,blank = True,null = True)
    TRACK_PRICE_UNELEC =   models.CharField(u'gati运费(不带电)',max_length=200,blank = True,null = True)
    TRACK_DEAL_WEIGHT  =   models.CharField(u'gati处理费规格(首重)',max_length=200,blank = True,null = True)
    TRACK_DEAL_PRICE   =   models.CharField(u'gati处理费规格(单价)',max_length=200,blank = True,null = True)
    MARKETED           =   models.CharField(u'MARKETED',max_length=200,blank = True,null = True)
    MANUFACTURED       =   models.CharField(u'MANUFACTURED',max_length=200,blank = True,null = True)
    MRP_START          =   models.CharField(u'MRP_START',max_length=200,blank = True,null = True)
    MRP_END            =   models.CharField(u'MRP_END',max_length=200,blank = True,null = True)
    CUSTOMER_PHONE     =   models.CharField(u'CUSTOMER_PHONE',max_length=200,blank = True,null = True)
    END_MESSAGE        =   models.CharField(u'END_MESSAGE',max_length=200,blank = True,null = True)
    TABLE_WIDTH        =   models.IntegerField(u'字体大小', max_length=11, blank=False, null=False)

    class Meta:
        verbose_name=u'AMZON印度站价格配置'
        verbose_name_plural=u'AMZON印度站价格配置'
        db_table = 'amzon_india_price_config'
        ordering =  ['-id']
    def __unicode__(self):
        return u'%s'%(self.id,)

