# -*- coding: utf-8 -*-
from django.db import models
class v_user_content_type_id(models.Model):
    user_id = models.DecimalField(u'user_id',max_digits=10,decimal_places=0)
    content_type_id = models.CharField(u'content_type_id', max_length=100)

    class Meta:
        verbose_name = u'v_user_content_type_id'
        verbose_name_plural = u'v_user_content_type_id'
        db_table = 'v_user_content_type_id'
    def __unicode__(self):
        return self.user_id
