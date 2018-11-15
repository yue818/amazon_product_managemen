# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models
#12)    部门领用记录 t_product_depart_get
class t_config_ip(models.Model):
    IP             =   models.CharField(u'IP',max_length=16,blank = True,null = True)
    CloudName      =   models.CharField(u'云平台',max_length=16,blank = True,null = True)
    UpdateTime     =   models.DateTimeField(u'更新时间',auto_now=True,)

    class Meta:
        verbose_name=u'IP配置信息'
        verbose_name_plural=u' IP配置信息'
        db_table = 't_config_ip'
        ordering =  ['id']
    def __unicode__(self):
        return u'id:%s'%(self.id)
