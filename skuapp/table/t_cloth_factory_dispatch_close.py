# -*- coding: utf-8 -*-
"""
 @desc:
 @author: wangzhiyang
 @site:
 @software: PyCharm
 @file: t_cloth_factory_dispatch_close.py
 @time: 2018/4/28 8:53
"""
from t_cloth_factory_dispatch_needpurchase import t_cloth_factory_dispatch_needpurchase

class t_cloth_factory_dispatch_close(t_cloth_factory_dispatch_needpurchase):
    class Meta:
        verbose_name=u'已建普源采购单'
        verbose_name_plural=u'已建普源采购单'
        db_table = 't_cloth_factory_dispatch'
        ordering =  ['-id']
        proxy = True
    def __unicode__(self):
        return u'id:%s sku:%s'%(self.id,self.SKU)