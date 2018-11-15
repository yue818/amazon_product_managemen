#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-02-05 9:21
# @Author  : Zhangyu
# @Site    : 
# @File    : goodsstatus_compare.py
# @Software: PyCharm
from django.db import models
from public import *


class goodsstatus_compare(models.Model):
    id                 =     models.IntegerField(u'id', blank=True, primary_key=True)
    hq_GoodsStatus     =     models.CharField(u'hq_GoodsStatus', max_length=255, blank=True, null=True)
    py_GoodsStatus     =     models.CharField(u'py_GoodsStatus', max_length=255, blank=True, null=True)
    statuscode         =     models.CharField(u'statuscode', max_length=12, blank=True, null=True)

    class Meta:
        verbose_name = u'状态对比'
        verbose_name_plural = verbose_name
        db_table = 'goodsstatus_compare'
        ordering = ['-id']
