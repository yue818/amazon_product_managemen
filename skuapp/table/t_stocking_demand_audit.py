# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: wangzy
 @site: 
 @software: PyCharm
 @file: t_stocking_demand_audit.py
 @time: 2018-04-20 10:30

"""
from t_stocking_demand_list import t_stocking_demand_list

class t_stocking_demand_audit(t_stocking_demand_list):

    class Meta:
        verbose_name = u'采购计划审核'
        verbose_name_plural = verbose_name
        db_table = 't_stocking_demand_list'
        proxy = True
    def __unicode__(self):
        return u'%s' % (self.id)