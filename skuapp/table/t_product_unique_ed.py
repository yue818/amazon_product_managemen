# -*- coding: utf-8 -*-
from t_base import t_base

#3) 审核完成-待开发 t_product_unique_ed
class t_product_unique_ed(t_base):
    class Meta:
        verbose_name=u'已调研待开发'
        verbose_name_plural=u' 步骤03--已调研待开发'
        db_table = 't_product_unique_ed'
        ordering =  ['CreateTime']
    def __unicode__(self):
        return u'id:%s MainSKU:%s'%(self.id,self.MainSKU)