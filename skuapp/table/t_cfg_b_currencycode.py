# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models

class t_cfg_b_currencycode(models.Model):
    CURRENCYCODE      =   models.CharField(u'当前货币编号',max_length=16,blank = True,null = True)
    CurrencyName      =   models.CharField(u'货币中文名称',max_length=16,blank = True,null = True)
    ExchangeRate      =   models.DecimalField(u'汇率',max_digits=18,decimal_places=6,blank = True,null = True)
    updateTime        =   models.DateTimeField(u'更新时间',auto_now=True,)

    class Meta:
        verbose_name=u'货币汇率表'
        verbose_name_plural=u' 货币汇率表'
        db_table = 't_cfg_b_currencycode'
        ordering =  ['id']
    def __unicode__(self):
        return u'id:%s'%(self.id)
