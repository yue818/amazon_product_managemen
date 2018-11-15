# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models

class t_cfg_b_emsfare_country2(models.Model):
    country_code             =   models.CharField(u'国家编号',max_length=24,blank = True,null = True)
    logisticwaycode          =   models.CharField(u'物流方式编号',max_length=64,blank = True,null = True)
    getprice                 =   models.TextField(u'价格计算Code',blank = True,null = True)
    getprice_desc            =   models.TextField(u'运费计算逻辑',blank = True,null = True)
    Bracketid                =   models.IntegerField(u'分档计费外键ID',blank = True,null = True)
    updatetime               =   models.DateTimeField(u'更新时间',auto_now=True,)

    class Meta:
        verbose_name=u'目的国家—运费计算配置表'
        verbose_name_plural=u'目的国家—运费计算配置表'
        db_table = 't_cfg_b_emsfare_country2'
        ordering =  ['id']
    def __unicode__(self):
        return u'id:%s'%(self.id)
