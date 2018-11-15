# -*- coding: utf-8 -*-
from django.db import models
class v_user_model(models.Model):
    user_id = models.DecimalField(u'user_id',max_digits=10,decimal_places=0)
    app_label = models.CharField(u'app_label', max_length=100)
    model = models.CharField(u'model', max_length=100)

    class Meta:
        verbose_name = u'v_user_model'
        verbose_name_plural = u'v_user_model'
        db_table = 'v_user_model'
    def __unicode__(self):
        return self.user_id
