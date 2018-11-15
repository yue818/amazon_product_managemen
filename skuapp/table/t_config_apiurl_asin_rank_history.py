# -*- coding: utf-8 -*-
from django.db import models

class t_config_apiurl_asin_rank_history(models.Model):
    ASIN                   =   models.CharField(u'ASIN',max_length=32,blank = True,null = True)
    Rank                   =   models.CharField(u'Rank',max_length=8,blank = True,null = True)
    RefreshTime            =   models.DateTimeField(u'RefreshTime',blank = True,null = True) 
    class Meta:
        verbose_name=u'ASIN 历史排名'
        verbose_name_plural=verbose_name
        db_table = 't_config_apiurl_asin_rank_history'
        ordering =  ['-RefreshTime']
    def __unicode__(self):
        return u'%s'%(self.id)
