# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models
#12)    部门领用记录 t_product_depart_get
class t_wish_honor(models.Model):
    ShopName        =   models.CharField(u'店铺名',max_length=32,blank = True,null = True)
    ShopNameOfficial        =   models.CharField(u'店铺名称',max_length=32,blank = True,null = True)
    seller                  =   models.CharField(u'销售员',max_length=32,blank = True,null = True)
    ShopHonor       =   models.CharField(u'诚信状况',max_length=255,blank = True,null = True)
    ImitationRate   =   models.CharField(u'仿品率',max_length=32,blank = True,null = True)
    EffectiveTrackingRate   =   models.CharField(u'有效跟踪率',max_length=32,blank = True,null = True)
    DelayedDeliveryRate     =   models.CharField(u'延迟发货率',max_length=32,blank = True,null = True)
    DayAverageScore       =   models.CharField(u'30天平均评分',max_length=32,blank = True,null = True)
    RefundRateWithin63To93  =   models.CharField(u'在63天到93天内的退款率',max_length=32,blank = True,null = True)
    updateTime              =   models.CharField(u'更新时间',max_length=16,blank = True,null = True)

    class Meta:
        verbose_name=u'Wish诚信店铺详情'
        verbose_name_plural=u' Wish诚信店铺详情'
        db_table = 't_wish_honor'
        ordering =  ['id']
    def __unicode__(self):
        return u'id:%s'%(self.id)