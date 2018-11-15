# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models

class t_cfg_extra_fee(models.Model):
    get_fba_price                     =   models.TextField(u'fba价格规则',blank = True,null = True)
    get_fba_price_desc                =   models.TextField(u'fba价格描述',blank = True,null = True)
    get_js_price                      =   models.TextField(u'结算价格规则',blank = True,null = True)
    get_js_price_desc                 =   models.TextField(u'结算价格描述',blank = True,null = True)
    get_qg_price                      =   models.TextField(u'清关价格规则',blank = True,null = True)
    sb_discount                       =   models.CharField(u'申报折扣',max_length=32,blank = True,null = True)
    bcd_rate                          =   models.IntegerField(u'bcd税率',blank = True,null = True)
    yj_rate                           =   models.IntegerField(u'佣金比率',blank = True,null = True)
    xss_rate                          =   models.IntegerField(u'销售税比率',blank = True,null = True) 
    CURRENCYCODE                      =   models.CharField(u'货币代码',max_length=16,blank = True,null = True)
    updatetime                        =   models.DateTimeField(u'更新时间',auto_now=True,)

    class Meta:
        verbose_name=u'额外费用配置表'
        verbose_name_plural=u'额外费用配置表'
        db_table = 't_cfg_extra_fee'
        ordering =  ['id']
    def __unicode__(self):
        return u'id:%s'%(self.id)
