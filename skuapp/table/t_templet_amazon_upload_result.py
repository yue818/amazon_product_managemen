#-*-coding:utf-8-*-
from django.db import models
from .t_templet_amazon_base import *

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_templet_amazon_upload_result.py
 @time: 2017/12/16 9:40
"""
class t_templet_amazon_upload_result(t_templet_amazon_base):
    """Amazon刊登结果表"""
    ShopSets        = models.TextField(u'待刊登店铺', blank=True, null=True)
    resultInfo      = models.CharField(u'处理结果',max_length=200,blank = True,null = True)
    errorMessages   = models.TextField(u'错误信息', blank=True, null=True)
    mqResponseInfo  = models.CharField(u'MQ回调消息查询条件',max_length=200,blank = True,null = True)

    class Meta:
        verbose_name = u'Amazon刊登结果'
        verbose_name_plural = verbose_name
        db_table = 't_templet_amazon_upload_result'
        ordering = ['-updateTime']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)