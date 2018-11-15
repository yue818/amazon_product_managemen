# encoding: utf-8
'''
@author: zhangyu
@contact: 292724306@qq.com
@software: pycharm
@file: wish_notification.py
@time: 2018-06-09 13:34
'''
from django.db import models


class wish_notification(models.Model):
    id = models.IntegerField(primary_key=True)
    shopName = models.CharField(u'店铺名称', max_length=255, blank=True, null=True)
    perma_link = models.CharField(max_length=255, blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    noti_id = models.CharField(max_length=255, blank=True, null=True)
    unview_count = models.IntegerField(u'未阅读通知', max_length=11, blank=True, null=True)
    infractions_count = models.IntegerField(u'违规数', max_length=11, blank=True, null=True)
    Operators = models.CharField(u'运营', max_length=50, blank=True, null=True)
    updateTime = models.DateTimeField(u'同步时间', auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = u'Wish系统消息'
        verbose_name_plural = verbose_name
        db_table = 'wish_notification'
        # proxy = True
        ordering = ['shopName']
