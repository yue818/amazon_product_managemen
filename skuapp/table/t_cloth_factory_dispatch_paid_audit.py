# -*- coding: utf-8 -*-
"""
 @desc:
 @author: wangzhiyang
 @site:
 @software: PyCharm
 @file: t_cloth_factory_dispatch_paid_audit.py
 @time: 2018/4/28 8:53
"""
from t_cloth_factory_dispatch_needpurchase import t_cloth_factory_dispatch_needpurchase

class t_cloth_factory_dispatch_paid_audit(t_cloth_factory_dispatch_needpurchase):

    class Meta:
        verbose_name=u'排单计划审核'
        verbose_name_plural=u'排单计划审核'
        db_table = 't_cloth_factory_dispatch'
        proxy = True
        ordering = ['-id']
    def __unicode__(self):
        return u'id:%s sku:%s'%(self.id,self.SKU)