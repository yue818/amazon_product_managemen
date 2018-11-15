# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models

class t_cfg_b_emsfare_country(models.Model):
    country_code             =   models.CharField(u'国家编号',max_length=24,blank = True,null = True)
    logisticwaycode          =   models.CharField(u'物流方式编号',max_length=10,blank = True,null = True)
    seq                      =   models.IntegerField(u'默认优先级',blank = True,null = True)
    BaseMoney                =   models.DecimalField(u'基础费用',max_digits=8,decimal_places=4,blank = True,null = True)
    BeginWeight              =   models.IntegerField(u'初始重量(g)',max_length=10,blank = True,null = True)
    BeginMoney               =   models.DecimalField(u'初始费用',max_digits=8,decimal_places=4,blank = True,null = True)
    AddWeight                =   models.IntegerField(u'超出重量(g)',max_length=10,blank = True,null = True)
    Bracketid                =   models.IntegerField(u'分档计费方式ID',blank = True,null = True)
    AddMoney                 =   models.DecimalField(u'超出费用',max_digits=8,decimal_places=4,blank = True,null = True)
    updateTime               =   models.DateTimeField(u'更新时间',auto_now=True,)

    class Meta:
        verbose_name=u'运费计算配置表'
        verbose_name_plural=u' 运费计算配置表'
        db_table = 't_cfg_b_emsfare_country'
        ordering =  ['id']
    def __unicode__(self):
        return u'id:%s'%(self.id)
