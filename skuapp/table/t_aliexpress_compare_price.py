# -*- coding: utf-8 -*-
from django.db import models
class t_aliexpress_compare_price(models.Model):
    OurProductID       =   models.CharField(u'我方ProductID',max_length=600,blank = True,null = True)
    OurMainSKU         =   models.CharField(u'我方主SKU',max_length=16,blank = True,null = True)
    OurSales       =   models.CharField(u'我方总销量',max_length=16,blank = True,null = True)
    OurWeekSales      =   models.CharField(u'我方周销量',max_length=16,blank = True,null = True)
    OurPrice           =   models.CharField(u'我方价格',max_length=16,blank = True,null = True)

    OppositeProductID      =   models.BigIntegerField(u'对方ProductID',blank = True,null = True)
    OppositeSales            =   models.CharField(u'对方订单数',max_length=16,blank = True,null = True)
    OppositeWeekSales         =   models.CharField(u'对方周销量',max_length=16,blank = True,null = True)
    OppositePrice = models.CharField(u'对方价格',max_length=16,blank=True, null=True)

    QueryTime = models.DateTimeField(u'查询时间',blank=True, null=True)

    class Meta:
        verbose_name=u'速卖通比价信息'
        verbose_name_plural=verbose_name
        db_table = 't_aliexpress_compare_price'
        ordering =  ['-QueryTime']
    def __unicode__(self):
        return u'%s %s'%(self.id,self.QueryTime)