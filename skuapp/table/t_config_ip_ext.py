# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models
from public import *
#12)    部门领用记录 t_product_depart_get
class t_config_ip_ext(models.Model):
    IP             =   models.CharField(u'IP',max_length=32,blank = True,null = True)
    K              =   models.CharField(u'云主机用途',choices=getChoices(ChoiceIPApplication),max_length=32,blank = True,null = True)
    UpdateTime     =   models.DateTimeField(u'更新时间',auto_now=True,)

    class Meta:
        verbose_name=u'IP配置信息扩展'
        verbose_name_plural=u' IP配置信息扩展'
        db_table = 't_config_ip_ext'
        ordering =  ['id']
    def __unicode__(self):
        return u'id:%s'%(self.id)
