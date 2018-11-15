# -*- coding: utf-8 -*-
from django.db import models
class v_django_type(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField('python model class name', max_length=100)

    class Meta:
        verbose_name = u'content type'
        verbose_name_plural = u'content types'
        db_table = 'v_django_type'

    def __unicode__(self):
        return self.id