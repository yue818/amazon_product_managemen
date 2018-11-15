# -*- coding: utf-8 -*-
from django.db import models
from .public import *

class t_product_ad_conversion_rate(models.Model):
    image                    =   models.CharField(u'图片',max_length=63,blank = True,null = True)
    AdvertisedSKU            =   models.CharField(u'刊登SKU',max_length=64,blank = True,null = True)
    ShopName                 =   models.CharField(u'卖家简称',max_length=64,blank = True,null = True)
    Keyword                  =   models.CharField(u'关键字',max_length=64,blank = True,null = True)
    MatchType                =   models.CharField(u'MatchType',max_length=64,blank = True,null = True)
    Remarks                  =   models.TextField(u'备注',max_length=500,blank = True,null = True)
    KeywordRemarks           =   models.CharField(u'关键字状态',choices=getChoices(ChoiceKeyWordsStatus),max_length=11,blank = True,null = True)
    ADStatusRemarks          =   models.CharField(u'广告组状态',choices=getChoices(ChoiceADStatus),max_length=11,blank = True,null = True)
    CampaignName             =   models.CharField(u'广告系列名称',max_length=64,blank = True,null = True)
    AdGroupName              =   models.CharField(u'广告组名称',max_length=64,blank = True,null = True)
    WTotalHits               =   models.IntegerField(u'周点击数(次)',max_length=11,blank = True,null = True)
    MTotalHits               =   models.IntegerField(u'月点击数(次)',max_length=11,blank = True,null = True)
    TotalHits                =   models.IntegerField(u'总点击数(次)',max_length=11,blank = True,null = True)
    WOrder                   =   models.IntegerField(u'周订单数(个)',max_length=11,blank = True,null = True)
    MOrder                   =   models.IntegerField(u'月订单数(个)',max_length=11,blank = True,null = True)
    ZOrder                   =   models.IntegerField(u'总订单数(个)',max_length=11,blank = True,null = True)
    TotalConversionRate      =   models.DecimalField(u'总转化率(%)',max_digits=11,decimal_places=2,blank = True,null = True)
    MonthlyConversionRate    =   models.DecimalField(u'月转化率(%)',max_digits=11,decimal_places=2,blank = True,null = True)
    WeeklyConversionRate     =   models.DecimalField(u'周转化率(%)',max_digits=11,decimal_places=2,blank = True,null = True)
    ASIN                     =   models.CharField(u'ASIN',max_length=15,blank = True,null = True)
    ZImpressions             =   models.DecimalField(u'总曝光率',max_digits=11,decimal_places=2,blank = True,null = True)
    ZTotalSpend              =   models.DecimalField(u'总花费',max_digits=11,decimal_places=2,blank = True,null = True)
    ZDayOrderedProductSales  =   models.DecimalField(u'总产出',max_digits=11,decimal_places=2,blank = True,null = True)
    ZACoS                    =   models.DecimalField(u'总ACoS',max_digits=11,decimal_places=2,blank = True,null = True)
    MImpressions             =   models.DecimalField(u'月曝光率',max_digits=11,decimal_places=2,blank = True,null = True)
    MTotalSpend              =   models.DecimalField(u'月花费',max_digits=11,decimal_places=2,blank = True,null = True)
    MDayOrderedProductSales  =   models.DecimalField(u'月产出',max_digits=11,decimal_places=2,blank = True,null = True)
    MACoS                    =   models.DecimalField(u'月ACoS',max_digits=11,decimal_places=2,blank = True,null = True)
    WImpressions             =   models.DecimalField(u'周曝光率',max_digits=11,decimal_places=2,blank = True,null = True)
    WTotalSpend              =   models.DecimalField(u'周花费',max_digits=11,decimal_places=2,blank = True,null = True)
    WDayOrderedProductSales  =   models.DecimalField(u'周产出',max_digits=11,decimal_places=2,blank = True,null = True)
    WACoS                    =   models.DecimalField(u'周ACoS',max_digits=11,decimal_places=2,blank = True,null = True)
    
    ZCPC                     =   models.DecimalField(u'总CPC',max_digits=11,decimal_places=2,blank = True,null = True)
    WCPC                     =   models.DecimalField(u'周CPC',max_digits=11,decimal_places=2,blank = True,null = True)
    MCPC                     =   models.DecimalField(u'月CPC',max_digits=11,decimal_places=2,blank = True,null = True)
    
    class Meta:
        verbose_name=u'广告转化率'
        verbose_name_plural=verbose_name
        db_table = 't_product_ad_conversion_rate'
        ordering =  ['id']
    def __unicode__(self):
        return u'%s'%(self.id)