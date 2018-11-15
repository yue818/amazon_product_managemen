# -*- coding:utf-8 -*-
from django.db import models

class t_history(models.Model):
        username =models.CharField(max_length=60,blank=True,null=True)
        user_url =models.CharField(max_length=80,blank=True,null=True)
        url_time =models.DateTimeField(blank=True,null=True)
        url_names =models.CharField(max_length=100,blank=True,null=True)
        user_urls=models.CharField(max_length=255,blank=True,null=True)

        class Meta:
                 verbose_name =u'最近记录'
                 verbose_name_plural =verbose_name
                 db_table = 't_history'
                 ordering = ['-id']

        def __unicode__(self):
            return u'%s' % (self.id)


