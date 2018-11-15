# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 王芝杨
 @site: 
 @software: PyCharm
 @file: t_stocking_demand_fbw_demand.py
 @time: 2018-10-11

"""
from t_stocking_demand_fbw import t_stocking_demand_fbw

class t_stocking_demand_fbw_demand(t_stocking_demand_fbw):
    class Meta:
        verbose_name = u'FBW备货列表'
        verbose_name_plural = verbose_name
        db_table = 't_stocking_demand_fbw'
        proxy = True
    def __unicode__(self):
        return u'%s' % (self.id)