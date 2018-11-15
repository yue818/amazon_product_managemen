# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models

class t_cfg_b_emsfare(models.Model):
    platform_country_code             =   models.CharField(u'平台国家编号',max_length=16,blank = True,null = True)
    countrycode                       =   models.CharField(u'目的地国家编号',max_length=16,blank = True,null = True)  
    logisticwaycode                   =   models.CharField(u'物流方式编号',max_length=16,blank = True,null = True)
    weightlimit                       =   models.IntegerField(u'重量限制',blank = True,null = True)   
    weightlimit_logisticwaycode       =   models.CharField(u'超过最大重量对应物流编号',max_length=16,blank = True,null = True) 
    weightlimit2                      =   models.IntegerField(u'重量限制2',blank = True,null = True)   
    weightlimit2_logisticwaycode      =   models.CharField(u'超过最大重量对应物流编号2',max_length=16,blank = True,null = True)  
    pricelimit                        =   models.DecimalField(u'价格限制',max_digits=8,decimal_places=4,blank = True,null = True)   
    pricelimit_logisticwaycode        =   models.CharField(u'超过最大价格对应物流编号',max_length=16,blank = True,null = True)
    updatetime                        =   models.DateTimeField(u'更新时间',auto_now=True,)

    class Meta:
        verbose_name=u'平台国家物流方式配置表'
        verbose_name_plural=u' 平台国家物流方式配置表'
        db_table = 't_cfg_b_emsfare'
        ordering =  ['id']
    def __unicode__(self):
        return u'id:%s'%(self.id)
