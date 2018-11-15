# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_templet_amazon_upload_fail.py
 @time: 2018-04-11 13:16
"""  
# from django.db import models
# from .t_templet_amazon_upload_result import *
# class t_templet_amazon_upload_fail(t_templet_amazon_upload_result):
#     """Amazon铺货失败记录"""
#     class Meta(t_templet_amazon_upload_result.Meta):
#         # verbose_name = u'Amazon铺货失败记录'
#         # verbose_name_plural = verbose_name
#         db_table = 't_templet_amazon_upload_fail'
#         # ordering = ['-id']
#         # app_label = 'skuapp'
#
#     def __unicode__(self):
#         return u'%s' % (self.id)

from django.db import models
from .t_templet_amazon_base import *


class t_templet_amazon_upload_fail(t_templet_amazon_base):
    """Amazon刊登失败记录"""
    ShopSets = models.TextField(u'待铺货店铺', blank=True, null=True)
    resultInfo = models.CharField(u'处理结果', max_length=200, blank = True, null = True)
    errorMessages = models.TextField(u'错误信息', blank=True, null=True)
    mqResponseInfo = models.CharField(u'MQ回调消息查询条件', max_length=200,blank = True, null = True)
    is_display = models.IntegerField(u'是否展示', max_length=1, blank=True, null=True)

    class Meta:
        verbose_name = u'Amazon刊登失败记录'
        verbose_name_plural = verbose_name
        db_table = 't_templet_amazon_upload_fail'
        ordering = ['-id']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)