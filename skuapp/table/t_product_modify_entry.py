# -*- coding: utf-8 -*-
from t_product_information_modify import t_product_information_modify
class t_product_modify_entry(t_product_information_modify):
    class Meta:
        verbose_name=u'信息修改录入'
        verbose_name_plural=verbose_name
        proxy = True
    def __unicode__(self):
        return u'id:%s'%(self.id)