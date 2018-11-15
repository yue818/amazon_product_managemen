# -*- coding: utf-8 -*-
"""
 @desc:
 @author: wangzhiyang
 @site:
 @software: PyCharm
 @file: t_cloth_factory_dispatch_history.py
 @time: 2018/6/11 8:53
"""
from t_cloth_factory_dispatch_needpurchase import t_cloth_factory_dispatch_needpurchase
#API指令执行计划完成表
class t_cloth_factory_dispatch_history(t_cloth_factory_dispatch_needpurchase):
    class Meta:
        verbose_name=u'需采购和不需采购历史数据'
        verbose_name_plural=verbose_name
        db_table = 't_cloth_factory_dispatch'
        ordering =  ['-id']
        proxy = True
    def __unicode__(self):
        return u'id:%s sku:%s'%(self.id,self.SKU)