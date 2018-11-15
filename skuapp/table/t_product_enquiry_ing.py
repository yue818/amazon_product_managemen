# -*- coding: utf-8 -*-
from t_base import t_base
#6) 正在询价 t_product_enquiry_ing
from django.db import models
class t_product_enquiry_ing(t_base):
    auditnote = models.TextField(u'审核员备注', blank=True, null=True)
    class Meta:
        verbose_name=u'正在询价'
        verbose_name_plural=u' 步骤06--正在询价'
        db_table = 't_product_enquiry_ing'
        ordering =  ['CreateTime']
    def __unicode__(self):
        return u'id:%s MainSKU:%s'%(self.id,self.MainSKU)