# -*- coding: utf-8 -*-
from django.db import models
class model_name(models.Model):
    table_name  =   models.CharField(u'table_name', max_length=100)
    model_name  =   models.CharField(u'model_name', max_length=100)
    model       =   models.CharField(u'model',max_length=100)
    group1      =   models.CharField(u'group1',max_length=100)
    group1_seq  =   models.CharField(u'group1_seq',max_length=32)
    group2      =   models.CharField(u'group2',max_length=100)
    group2_seq  =   models.CharField(u'group2_seq',max_length=32)
    app_label   =   models.CharField(u'app_label',max_length=100)
    Serial      =   models.CharField(u'Serial',max_length=32)
    class Meta:
        ordering =  ['Serial']
        verbose_name = u'model_name'
        verbose_name_plural = u'model_name'
        db_table = 'model_name'
    def __unicode__(self):
        return self.id