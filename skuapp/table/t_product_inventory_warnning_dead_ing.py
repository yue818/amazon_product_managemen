# -*- coding: utf-8 -*-
from t_product_inventory_warnning import t_product_inventory_warnning

class t_product_inventory_warnning_dead_ing(t_product_inventory_warnning): 
    class Meta:
        verbose_name=u'死库待审核'
        verbose_name_plural=u'死库待审核'
        proxy = True
    def __unicode__(self):
        return u'%s'%(self.id)