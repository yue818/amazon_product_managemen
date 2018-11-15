# -*- coding: utf-8 -*-
from django.db import models

class t_config_aliexpress_pl(models.Model):
    aliexpress_pl = models.CharField(u'速卖通品类',max_length=255,null = True)
    py_pl = models.CharField(u'普元品类',max_length=255,null=True)
    mainsku = models.CharField(u'MainSKU',max_length=255,null=True)
    class Meta:
        verbose_name=u'速卖通品类配置'
        verbose_name_plural=u'速卖通品类配置'
        db_table = 't_config_aliexpress_pl'
        ordering =  ['-id']
    def __unicode__(self):
        return u'id:%s'%(self.id)