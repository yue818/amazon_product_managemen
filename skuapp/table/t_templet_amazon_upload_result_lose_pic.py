#-*-coding:utf-8-*-


"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_templet_amazon_upload_result_lose_pic.py
 @time: 2018/4/12 13:51
"""   
from django.db import models
from .t_templet_amazon_base import *


class t_templet_amazon_upload_result_lose_pic(t_templet_amazon_base):
    """Amazon刊登图片缺失记录"""
    ShopSets = models.TextField(u'待铺货店铺', blank=True, null=True)
    resultInfo = models.CharField(u'处理结果', max_length=200, blank = True, null = True)
    errorMessages = models.TextField(u'错误信息', blank=True, null=True)
    mqResponseInfo = models.CharField(u'MQ回调消息查询条件', max_length=200,blank = True, null = True)
    is_display = models.IntegerField(u'是否展示', max_length=1, blank=True, null=True)

    class Meta:
        verbose_name = u'Amazon刊登成功图片缺失记录'
        verbose_name_plural = verbose_name
        db_table = 't_templet_amazon_upload_result_lose_pic'
        ordering = ['-id']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)