# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models
#14)    回收站 t_product_recycle
class t_product_recycle(t_base):
    fromTDel = models.CharField(u'删除来源', max_length=32, blank=True, null=True)
    class Meta:
        verbose_name=u'回收站'
        verbose_name_plural=u' 步骤14--回收站'
        db_table = 't_product_recycle'
        ordering =  ['-id']
    def __unicode__(self):
        return u'id =%d StaffID=%s name =%s'%(self.id, self.StaffID,self.Name)