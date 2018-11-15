#-*-coding:utf-8-*-
from django.db import models
from skuapp.table.t_template_amazon_advertising_business_report_base import t_template_amazon_advertising_business_report_base

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_template_amazon_advertising_business_report.py
 @time: 2018/8/21 9:51
"""

class t_template_amazon_advertising_business_report(t_template_amazon_advertising_business_report_base):

    class Meta:
        verbose_name = u'Amazon广告业务报告表'
        verbose_name_plural = verbose_name
        db_table = 't_template_amazon_advertising_business_report'
        ordering = ['-id']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)