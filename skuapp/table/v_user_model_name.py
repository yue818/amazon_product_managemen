# -*- coding: utf-8 -*-
from django.db import models

class v_user_model_name(models.Model):
    model=models.CharField(u'model',max_length=100)
    model_name=models.CharField(u'model_name',max_length=100)
    app_label=models.CharField(u'app_label',max_length=100)
    user_id = models.DecimalField(u'user_id',max_digits=10,decimal_places=0)

    class Meta:
        verbose_name = u'v_user_model_name'
        verbose_name_plural = u'v_user_model_name'
        db_table = 'v_user_model_name'

    def __unicode__(self):
        return self.id
