# -*- coding: utf-8 -*-
"""
 @desc:开发产品审核 如果是“通过审核”操作，记录审核人以及审核时间，将选中记录推送至“已开发带询价”界面
                    如果是“驳回“操作，请首先检测“产品专员备注”，如果为空，请提示错误，不予操作，如果“产品专员备注“不为空，将选中记录推送到”正在开发“界面
                    如果是”不开发“操作，请首先检测”产品专员备注“，如果为空，请提示错误，不予操作，如果“产品专员备注“不为空，将选中记录推送到”不开发产品“界面
 @author: wangzhiyang
 @site:
 @software: PyCharm
 @file: t_product_develop_audit.py
 @time: 2018/4/28 8:53
"""
from django.db import models
from t_base import t_base
class t_product_develop_audit(t_base):
    auditnote = models.TextField(u'审核员备注', blank=True, null=True)
    class Meta:
        verbose_name=u'已开发待审核'
        verbose_name_plural = verbose_name
        db_table = 't_product_develop_ing'
        ordering =  ['CreateTime']
    def __unicode__(self):
        return u'id:%s MainSKU:%s'%(self.id,self.MainSKU)
