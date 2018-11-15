# -*- coding: utf-8 -*-
from django.db import models


class t_wish_keywords(models.Model):
    keyword = models.CharField(u'关键词', max_length=32, blank=True, null=True)
    poArrRate = models.CharField(u'预计可能达到', max_length=32, blank=True, null=True)
    preCompe = models.CharField(u'预估竞争度', max_length=32, blank=True, null=True)
    proBid = models.CharField(u'建议竞价', max_length=32, blank=True, null=True)
    rank = models.IntegerField(u'排名', max_length=11, blank=True, null=True)
    updateTime = models.DateTimeField(u'更新时间', blank=True, null=True)

    class Meta:
        verbose_name = u'WISH关键词'
        verbose_name_plural = verbose_name
        db_table = 't_wish_keywords'
        ordering = ['rank']

    def __unicode__(self):
        return u'id:%s' % (self.id)