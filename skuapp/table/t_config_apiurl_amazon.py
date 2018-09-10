#-*-coding:utf-8-*-
from django.db import models
"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_config_apiurl_amazon.py
 @time: 2017/12/18 15:34
"""
class t_config_apiurl_amazon(models.Model):
    site        = models.CharField(u'站点', max_length=32, blank=True, null=True)
    category    = models.CharField(u'商品类目', max_length=100, blank=True, null=True)
    RootID      = models.CharField(u'商品目录ID', max_length=32, blank=True, null=True)
    groupRoot   = models.CharField(u'根目录', max_length=100, blank=True, null=True)
    group2      = models.CharField(u'二级目录', max_length=100, blank=True, null=True)
    group3      = models.CharField(u'三级目录', max_length=100, blank=True, null=True)
    group4      = models.CharField(u'四级目录', max_length=100, blank=True, null=True)
    group5      = models.CharField(u'五级目录', max_length=100, blank=True, null=True)
    group6      = models.CharField(u'六级目录', max_length=100, blank=True, null=True)
    group7      = models.CharField(u'七级目录', max_length=100, blank=True, null=True)
    group8      = models.CharField(u'八级目录', max_length=100, blank=True, null=True)
    item_type   = models.CharField(u'节点类型', max_length=200, blank=True, null=True)
    CreateUser  = models.CharField(u'采集人', max_length=32, blank=True, null=True)
    CreateTime  = models.DateTimeField(u'采集时间', blank=True, null=True)
    UpdateUser  = models.CharField(u'更新人', max_length=32, blank=True, null=True)
    UpdateTime  = models.DateTimeField(u'更新时间', blank=True, null=True)

    class Meta:
        verbose_name = u'Amazon商品类目表'
        verbose_name_plural = verbose_name
        db_table = 't_config_apiurl_amazon'
        ordering = ['-id']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)