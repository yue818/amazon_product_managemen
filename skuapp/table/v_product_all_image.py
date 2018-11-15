# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models
#16)    未录入商品信息 t_product_allsku
class v_product_all_image(t_base):
    T            =   models.CharField(u'目前位置',max_length=16,null = True,db_index =True)
    class Meta:
        verbose_name=u'未完成图片'
        verbose_name_plural=u' 未完成图片'
        db_table = 'v_product_all_image'

    def __unicode__(self):
        return u'id=%s name =%s'%(self.id,self.MainSKU)