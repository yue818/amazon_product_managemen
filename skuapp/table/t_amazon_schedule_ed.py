# -*- coding: utf-8 -*-
from t_api_schedule import t_api_schedule
from django.db import models
#API指令执行计划完成表
class t_amazon_schedule_ed(t_api_schedule):
    ShopNameIP =   models.CharField(u'店铺IP',max_length=32,blank = True,null = True)

    class Meta:
        verbose_name=u'API指令执行计划完成表'
        verbose_name_plural=u'API指令执行计划完成表'
        db_table = 't_amazon_schedule_ed'
        ordering =  ['id']
    def __unicode__(self):
        return u'id:%s CMDID:%s'%(self.id,self.CMDID)