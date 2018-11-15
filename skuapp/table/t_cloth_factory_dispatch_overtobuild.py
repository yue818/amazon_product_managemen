# -*- coding: utf-8 -*-
"""
 @desc:
 @author: wangzhiyang
 @site:
 @software: PyCharm
 @file: t_cloth_factory_dispatch_overtobuild.py
 @time: 2018/4/28 8:53
"""
from t_cloth_factory_dispatch_needpurchase import t_cloth_factory_dispatch_needpurchase

class t_cloth_factory_dispatch_overtobuild(t_cloth_factory_dispatch_needpurchase):
    class Meta:
        verbose_name=u'生产完成可建普源采购单'
        verbose_name_plural=u'已确认交付'
        db_table = 't_cloth_factory_dispatch'
        ordering =  ['-id']
        proxy = True
    def __unicode__(self):
        return u'id:%s sku:%s'%(self.id,self.SKU)