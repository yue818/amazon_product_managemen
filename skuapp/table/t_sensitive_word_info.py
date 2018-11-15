# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models
from public import *
from django.utils.safestring import mark_safe

class t_sensitive_word_info(models.Model):
    sensitive_words         =   models.CharField(u'敏感关键词',max_length=100,blank = True,null = True)
    Input_man               =   models.CharField(u'信息录入员',max_length=100,blank = True,null = True)
    Input_time              =   models.DateTimeField(u'录入时间',blank = True,null = True)

    class Meta:
        verbose_name=u'敏感关键词信息录入表'
        verbose_name_plural=u'敏感关键词信息录入表'
        db_table = 't_sensitive_word_info'
        ordering =  ['-id']
    def __unicode__(self):
        return u'id:%s'%(self.id)
