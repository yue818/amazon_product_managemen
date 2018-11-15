# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models
#10.3)  信息录入 t_product_enter_ing
class t_product_enter_ing(t_base):
    auditnote = models.TextField(u'审核员备注', blank=True, null=True)
    class Meta:
        verbose_name=u'信息录入'
        verbose_name_plural=u' 步骤10.3--信息录入'
        db_table = 't_product_enter_ing'
        ordering =  ['CreateTime']
    def __unicode__(self):
        return u'id:%s MainSKU:%s'%(self.id,self.MainSKU)