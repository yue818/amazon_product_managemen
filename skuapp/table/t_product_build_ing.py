# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models
#7) 正在建资料 t_product_build_ing
class t_product_build_ing(t_base):
    auditnote=models.TextField(u'审核员备注',blank = True,null = True)
    class Meta:
        verbose_name=u'正在建资料'
        verbose_name_plural=u' 步骤07--正在建资料'
        db_table = 't_product_build_ing'
        ordering =  ['CreateTime']
    def __unicode__(self):
        return u'id:%s MainSKU:%s'%(self.id,self.MainSKU)