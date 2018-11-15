# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models

class t_cfg_platform_country(models.Model):
    platform_country_code             =   models.CharField(u'平台编号',max_length=24,blank = True,null = True)
    platform_country_name             =   models.CharField(u'平台中文',max_length=32,blank = True,null = True)
    #kickback                          =   models.DecimalField(u'平台扣点',max_digits=3,decimal_places=2,blank = True,null = True)
    basefee                           =   models.DecimalField(u'平台额外小费(对应国家货币)',max_digits=8,decimal_places=4,blank = True,null = True)
    #CURRENCYCODE                      =   models.CharField(u'当前货币编号',max_length=24,blank = True,null = True)
    updatetime                        =   models.DateTimeField(u'更新时间',auto_now=True,)

    class Meta:
        verbose_name=u'平台配置表'
        verbose_name_plural=u' 平台配置表'
        db_table = 't_cfg_platform_country'
        ordering =  ['id']
    def __unicode__(self):
        return u'id:%s'%(self.id)
