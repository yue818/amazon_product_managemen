#-*-coding:utf-8-*-
from django.db import models

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_template_product_config_amazon.py
 @time: 2018/1/23 10:00
"""
class t_template_product_config_amazon(models.Model):
    site = models.CharField(u'站点', max_length=32, blank=True, null=True)
    product_type = models.CharField(u'刊登种类', max_length=64, blank=True, null=True)
    feed_product_type = models.TextField(u'产品类型', blank=True, null=True)
    params = models.TextField(u'必填字段', blank=True, null=True)
    createTime = models.DateTimeField(u'采集时间', blank=True, null=True)
    createUser = models.CharField(u'采集人', max_length=32, blank=True, null=True)
    updateTime = models.DateTimeField(u'更新时间', blank=True, null=True)
    updateUser = models.CharField(u'更新人', max_length=32, blank=True, null=True)

    class Meta:
        verbose_name = u'Amazon刊登种类配置'
        verbose_name_plural = verbose_name
        db_table = 't_template_product_config_amazon'
        ordering = ['-id']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)
