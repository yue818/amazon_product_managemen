# -*- coding: utf-8 -*-
from django.db import models
#API指令执行计划完成表
class t_cloth_factory(models.Model):
    id = models.AutoField(u'业务流水号', primary_key=True)
    name = models.CharField(u'服装外派工厂名', max_length=256, blank=True, null=True)
    value = models.CharField(u'服装外派工厂值', max_length=256, blank=True, null=True)

    class Meta:
        verbose_name=u'服装外派工厂'
        verbose_name_plural=u'服装外派工厂'
        db_table = 't_cloth_factory'
        ordering =  ['id']
    def __unicode__(self):
        return u'id:%s'%(self.id)