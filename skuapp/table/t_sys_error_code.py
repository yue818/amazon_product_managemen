#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_sys_error_code.py
 @time: 2018-05-12 15:48
"""

from django.db import models

class t_sys_error_code(models.Model):
    id = models.AutoField(u'流水号', primary_key=True)
    error_code = models.CharField(u'错误代码', max_length=8)
    error_text = models.CharField(u'错误内容', max_length=64, blank=True, null=True)
    possible_reason = models.CharField(u'错误原因', max_length=128, blank=True, null=True)

    class Meta:
        verbose_name = u'错误代码'
        verbose_name_plural = u'错误代码'
        db_table = 't_sys_error_code'
        ordering = ['-id']

    def __unicode__(self):
        return u'%s' % (self.id, )