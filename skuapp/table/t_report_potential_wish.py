# -*- coding: utf-8 -*-
from django.db import models
from public import *
from .t_online_info_wish import *


class t_report_potential_wish(t_online_info_wish):

    class Meta:
        verbose_name=u'15天爆款商品'
        verbose_name_plural=verbose_name
        db_table = 't_online_info_wish'
        proxy = True
        ordering = ['-SoldXXX']
        
    def __unicode__(self):
        return u'%s'%(self.id)