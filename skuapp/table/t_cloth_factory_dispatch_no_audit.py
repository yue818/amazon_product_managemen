# -*- coding: utf-8 -*-
"""
 @desc:
 @author: wangzhiyang
 @site:
 @software: PyCharm
 @file: t_cloth_factory_dispatch_no_audit.py
 @time: 2018/4/28 8:53
"""
from t_cloth_factory_dispatch_needpurchase import t_cloth_factory_dispatch_needpurchase

class t_cloth_factory_dispatch_no_audit(t_cloth_factory_dispatch_needpurchase):

    class Meta:
        verbose_name=u'排单审核未通过'
        verbose_name_plural=u'排单审核未通过'
        db_table = 't_cloth_factory_dispatch'
        ordering =  ['-id']
        proxy = True
    def __unicode__(self):
        return u'id:%s sku:%s'%(self.id,self.SKU)