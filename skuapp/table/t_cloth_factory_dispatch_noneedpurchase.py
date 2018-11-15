# -*- coding: utf-8 -*-
"""
 @desc:
 @author: wangzhiyang
 @site:
 @software: PyCharm
 @file: t_cloth_factory_dispatch_noneedpurchase.py
 @time: 2018/6/08 8:53
"""
from t_cloth_factory_dispatch_needpurchase import t_cloth_factory_dispatch_needpurchase
#API指令执行计划完成表
class t_cloth_factory_dispatch_noneedpurchase(t_cloth_factory_dispatch_needpurchase):
    class Meta:
        verbose_name=u'不需采购供应链服装列表'
        verbose_name_plural=verbose_name
        db_table = 't_cloth_factory_dispatch'
        ordering =  ['-id']
        proxy = True
    def __unicode__(self):
        return u'id:%s sku:%s'%(self.id,self.SKU)