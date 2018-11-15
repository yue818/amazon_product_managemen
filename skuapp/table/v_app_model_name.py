# -*- coding: utf-8 -*-
from django.db import models
class v_app_model_name(models.Model):
    model = models.DecimalField(u'model',max_digits=10,decimal_places=0)
    app_label = models.CharField(u'app_label', max_length=100)
    model_name = models.CharField(u'model_name', max_length=100)
    Serial = models.DecimalField(u'Serial',max_digits=10,decimal_places=0)
    class Meta:
        ordering =  ['Serial']
        verbose_name = u'v_app_model_name'
        verbose_name_plural = u'v_app_model_name'
        db_table = 'v_app_model_name'
    def __unicode__(self):
        return self.id
