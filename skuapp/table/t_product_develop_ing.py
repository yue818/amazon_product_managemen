# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models
from django.utils.safestring import mark_safe

from public import *
#4) 正在开发 t_product_develop_ing
from django.db import models
class t_product_develop_ing(t_base):
    #selectpic        =   models.ImageField(u'选择图片',upload_to='media/',blank=True, null=True)
    auditnote = models.TextField(u'审核员备注', blank=True, null=True)
    class Meta:
        verbose_name=u'正在开发'
        verbose_name_plural=u' 步骤04--正在开发'
        db_table = 't_product_develop_ing'
        ordering =  ['CreateTime']
    def __unicode__(self):
        return u'id:%s MainSKU:%s'%(self.id,self.MainSKU)