# -*- coding: utf-8 -*-
from t_product_inventory_warnning import t_product_inventory_warnning

class t_product_inventory_warnning_stocking(t_product_inventory_warnning): 
    class Meta:
        verbose_name=u'申请备货'
        verbose_name_plural=u'申请备货'
        proxy = True
    def __unicode__(self):
        return u'%s'%(self.id)