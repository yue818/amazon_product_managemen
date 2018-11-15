#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_tort_info_image.py
 @time: 2018-05-09 17:31
"""
from django.db import models

class t_tort_info_image(models.Model):
    id = models.IntegerField(u'流水号', primary_key=True)
    detail = models.CharField(u'图片列表', max_length=1000)

    class Meta:
        verbose_name = u'侵权图片展示'
        verbose_name_plural = u'侵权图片展示'
        db_table = 'v_t_tort_info_image'
        ordering = ['-id']

    def __unicode__(self):
        return u'%s' % (self.id, )