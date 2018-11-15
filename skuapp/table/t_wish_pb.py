# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models
class t_wish_pb(models.Model):
    ShopName                =   models.CharField(u'店铺名',max_length=32,blank = True,null = True)
    #Seller                  =   models.CharField(u'销售员',max_length=32,blank = True,null = True)
    ActivityName            =   models.CharField(u'活动名称',max_length=32,blank = True,null = True)
    ActivityStatus          =   models.CharField(u'活动状态',max_length=32,blank = True,null = True)
    ActivityID              =   models.CharField(u'活动ID',max_length=32,blank = True,null = True)
    Duration                =   models.CharField(u'活动期间',max_length=32,blank = True,null = True)
    Budget                  =   models.CharField(u'预算',max_length=32,blank = True,null = True)
    EnrollFee               =   models.CharField(u'报名总费用',max_length=32,blank = True,null = True)
    TotalFee                =   models.CharField(u'总计',max_length=32,blank = True,null = True)
    ProductNum              =   models.CharField(u'产品',max_length=32,blank = True,null = True)
    ActivityFee             =   models.CharField(u'费用',max_length=32,blank = True,null = True)
    ActivityFlow            =   models.CharField(u'付费流量',max_length=32,blank = True,null = True)
    ProductOrder            =   models.CharField(u'订单',max_length=32,blank = True,null = True)
    ActivityAmount          =   models.CharField(u'成交总额',max_length=32,blank = True,null = True)
    FeeDivAmount            =   models.CharField(u'话费与成交总额之比',max_length=32,blank = True,null = True)
    Pic                     =   models.CharField(u'产品图片',max_length=255,blank = True,null = True)
    ProductID               =   models.CharField(u'产品ID',max_length=255,blank = True,null = True)
    ProductName             =   models.CharField(u'产品名称',max_length=32,blank = True,null = True)
    PbKey                   =   models.TextField(u'关键词',blank = True,null = True)
    PbCharge                =   models.CharField(u'要价',max_length=32,blank = True,null = True)
    PbFee                   =   models.CharField(u'费用',max_length=32,blank = True,null = True)
    PbData                  =   models.CharField(u'付费流量',max_length=32,blank = True,null = True)
    PbOrder                 =   models.CharField(u'订单',max_length=32,blank = True,null = True)
    PbCount                 =   models.CharField(u'成交总额',max_length=32,blank = True,null = True)
    updateTime              =   models.CharField(u'更新时间',max_length=16,blank = True,null = True)

    class Meta:
        verbose_name=u'Wish广告详情'
        verbose_name_plural=u' Wish广告详情'
        db_table = 't_wish_pb'
        ordering =  ['id']
    def __unicode__(self):
        return u'id:%s'%(self.id)