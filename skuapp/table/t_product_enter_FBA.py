# -*- coding: utf-8 -*-
from t_product_build_FBA import t_product_build_FBA

class t_product_enter_FBA(t_product_build_FBA):

    class Meta:
        verbose_name = u'FBA-信息录入'
        verbose_name_plural = verbose_name
        db_table = "t_product_build_fba"

        proxy = True
    def __unicode__(self):
        return u'id:%s,FBA-sku:%s'%(self.id,self.SKU)
