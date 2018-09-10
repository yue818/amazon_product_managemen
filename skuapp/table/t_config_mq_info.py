#-*-coding:utf-8-*-
from django.db import models
"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_config_mq_info.py
 @time: 2018/1/10 17:51
"""
class t_config_mq_info(models.Model):
    PlatformName = models.CharField(u'平台名称', max_length=16, blank=True, null=True)
    IP = models.CharField(u'店铺IP', max_length=32, blank=True, null=True)
    Name = models.CharField(u'店铺名称', max_length=32, blank=True, null=True)
    K = models.CharField(u'Key', max_length=20, null=True)
    V = models.CharField(u'Value', max_length=64, blank=True, null=True)

    class Meta:
        verbose_name=u'MQ配置'
        verbose_name_plural=u'MQ配置'
        db_table = 't_config_mq_info'
    def __unicode__(self):
        return u'%s'%(self.id)