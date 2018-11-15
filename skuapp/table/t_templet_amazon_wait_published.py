#-*-coding:utf-8-*-
from django.db import models
from skuapp.table.t_templet_amazon_base import *
"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_templet_amazon_wait_published.py
 @time: 2017/12/18 12:02
"""


class t_templet_amazon_wait_published(t_templet_amazon_base):


    class Meta:
        verbose_name = u'Amazon待刊登商品'
        verbose_name_plural = verbose_name
        db_table = 't_templet_amazon_wait_published'
        ordering = ['-id']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)