# -*- coding: utf-8 -*-
from t_base import t_base
#19)    已经重复 t_product_repeats
class t_product_repeats(t_base):
    class Meta:
        verbose_name=u'不开发产品'
        verbose_name_plural=verbose_name
        db_table = 't_product_repeats'
        ordering =  ['-id']
    def __unicode__(self):
        return u'id =%d StaffID=%s name =%s'%(self.id, self.StaffID,self.Name)
