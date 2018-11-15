# -*- coding: utf-8 -*-
from t_api_schedule import t_api_schedule
from django.db import models


# API指令执行计划
class t_api_schedule_ing_wish_upload(t_api_schedule):
    WishResultID = models.IntegerField(u'铺货结果ID', max_length=20, blank=True, null=True)
    class Meta:
        verbose_name = u'WISH铺货API指令执行计划'
        verbose_name_plural = verbose_name
        db_table = 't_api_schedule_ing_wish_upload'
        ordering = ['id']

    def __unicode__(self):
        return u'id:%s CMDID:%s' % (self.id, self.CMDID)
