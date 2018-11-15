# -*- coding: utf-8 -*-

from django.db import models
class t_supply_chain_production_basic_permission(models.Model):
    username=models.CharField(max_length=32, blank=True, null=True)
    account=models.CharField(max_length=32, blank=True, null=True)


    class Meta:
        verbose_name = u'供应链款生产基础资料权限'
        verbose_name_plural = verbose_name
        db_table = u't_supply_chain_production_basic_permission'

    def __unicode__(self):
        return u'%s' % (self.account)
