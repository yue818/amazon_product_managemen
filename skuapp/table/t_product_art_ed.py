# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models
#10.2)  信息审核 t_product_art_ed
class t_product_art_ed(t_base):
    auditnote = models.TextField(u'审核员备注', blank=True, null=True)
    class Meta:
        verbose_name=u'信息审核'
        verbose_name_plural=u' 步骤10.2--信息审核'
        db_table = 't_product_art_ed'
        ordering =  ['CreateTime']
    def __unicode__(self):
        return u'id:%s MainSKU:%s'%(self.id,self.MainSKU)