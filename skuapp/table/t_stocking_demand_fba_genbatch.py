# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 王芝杨
 @site: 
 @software: PyCharm
 @file: t_stocking_demand_fba_genbatch.py
 @time: 2018-08-11

"""
from t_stocking_demand_fba import t_stocking_demand_fba

class t_stocking_demand_fba_genbatch(t_stocking_demand_fba):
    class Meta:
        verbose_name = u'FBA生成批次'
        verbose_name_plural = verbose_name
        db_table = 't_stocking_demand_fba'
        proxy = True
    def __unicode__(self):
        return u'%s' % (self.id)