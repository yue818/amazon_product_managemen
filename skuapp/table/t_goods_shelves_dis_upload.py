# -*- coding: utf-8 -*-
from django.db import models
from public import *
from pyapp.models import *
from skuapp.table.t_goods_shelves import t_goods_shelves

class t_goods_shelves_dis_upload(t_goods_shelves):

    class Meta:
        verbose_name=u'Wish产品上架'
        verbose_name_plural=verbose_name
        proxy = True
        ordering =  ['-Orders7Days']
        
    def __unicode__(self):
        return u'%s'%(self.id)