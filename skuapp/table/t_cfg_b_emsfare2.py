# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models

class t_cfg_b_emsfare2(models.Model):
    platform_country_code             =   models.CharField(u'平台国家编号',max_length=16,blank = True,null = True)
    countrycode                       =   models.CharField(u'目的地国家编号',max_length=16,blank = True,null = True)
    standard_id                       =   models.IntegerField(u'规格外键ID',blank = True,null = True)
    category_id                       =   models.IntegerField(u'品类外键ID',blank = True,null = True)
    extra_id                          =   models.IntegerField(u'额外费用外键ID',blank = True,null = True)
    kickback                          =   models.DecimalField(u'平台扣点',max_digits=4,decimal_places=2,blank = True,null = True) 
    price_point                       =   models.IntegerField(u'价格分界点',blank = True,null = True)
    logisticwaycode                   =   models.TextField(u'物流方式逻辑',blank = True,null = True)
    logisticwaycode_desc              =   models.TextField(u'物流方式描述',blank = True,null = True)
    updatetime                        =   models.DateTimeField(u'更新时间',auto_now=True,)

    class Meta:
        verbose_name=u'平台国家—物流方式配置表'
        verbose_name_plural=u'平台国家—物流方式配置表'
        db_table = 't_cfg_b_emsfare2'
        ordering =  ['id']
    def __unicode__(self):
        return u'id:%s'%(self.id)
