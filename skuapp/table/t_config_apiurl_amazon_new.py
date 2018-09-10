# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_config_apiurl_amazon_new.py
 @time: 2018-04-08 14:01
"""  

from django.db import models


class t_config_apiurl_amazon_new(models.Model):
    site = models.CharField(u'站点', max_length=32, blank=True, null=True)
    category = models.CharField(u'商品类目', max_length=100, blank=True, null=True)
    RootID = models.CharField(u'商品目录ID', max_length=32, blank=True, null=True)
    group_all = models.CharField(u'目录', max_length=800, blank=True, null=True)
    item_type = models.CharField(u'节点类型', max_length=200, blank=True, null=True)
    CreateUser = models.CharField(u'采集人', max_length=32, blank=True, null=True)
    CreateTime = models.DateTimeField(u'采集时间', blank=True, null=True)
    UpdateUser = models.CharField(u'更新人', max_length=32, blank=True, null=True)
    UpdateTime = models.DateTimeField(u'更新时间', blank=True, null=True)

    class Meta:
        verbose_name = u'Amazon商品类目表'
        verbose_name_plural = verbose_name
        db_table = 't_config_apiurl_amazon_new'
        ordering = ['-id']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)