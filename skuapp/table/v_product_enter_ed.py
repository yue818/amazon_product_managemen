# -*- coding: utf-8 -*-
from t_base import t_base
from t_product_enter_ed import t_product_enter_ed
#17)    已录入商品信息 v_product_enter_ed
class v_product_enter_ed(t_product_enter_ed):
    class Meta:
        verbose_name=u'已录入商品信息'
        verbose_name_plural=u' 步骤17--已录入商品信息'
        proxy = True
    def __unicode__(self):
        return u'id:%s MainSKU:%s'%(self.id,self.MainSKU)