#-*-coding:utf-8-*-
from django.db import models

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_templet_config_amazon_published.py
 @time: 2017/12/19 15:36
"""
class t_templet_config_amazon_published(models.Model):
    site                        = models.CharField(u'站点', max_length=32, blank=True, null=True)
    item_type_root              = models.CharField(u'商品类型', max_length=32, blank=True, null=True)
    params                      = models.TextField(u'必填参数', blank=True, null=True)
    merchant_shipping_group_name= models.CharField(u'运输模型', max_length=64, blank=True, null=True)
    CreateTime                  = models.DateTimeField(u'采集时间', blank=True, null=True)
    CreateStaff                 = models.CharField(u'采集人', max_length=32, blank=True, null=True)
    UpdateTime                  = models.DateTimeField(u'更新时间', blank=True, null=True)
    UpdateStaff                 = models.CharField(u'更新人', max_length=32, blank=True, null=True)

    class Meta:
        verbose_name = u'Amazon刊登配置'
        verbose_name_plural = verbose_name
        db_table = 't_templet_config_amazon_published'
        ordering = ['-id']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)