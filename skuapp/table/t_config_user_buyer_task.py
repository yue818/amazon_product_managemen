# -*- coding: utf-8 -*-
from django.db import models
from skuapp.table.t_store_marketplan_execution_log  import *
from skuapp.table.t_config_user_buyer import t_config_user_buyer

def getBuyerAccount():
    #t_store_marketplan_execution_log_obj = t_store_marketplan_execution_log.objects.values('BuyerAccount')
    #if t_store_marketplan_execution_log_obj.exists():
        #BuyerAccount = t_store_marketplan_execution_log_obj[0]['BuyerAccount']
    #return ub.objects.values_list('BuyerAccount','BuyerAccount').exclude(BuyerAccount__in= t_store_marketplan_execution_log_obj).order_by('BuyerAccount')
    t_store_marketplan_execution_log_objs = t_store_marketplan_execution_log.objects.values('BuyerAccount')
    return t_config_user_buyer.objects.exclude(BuyerAccount__in=t_store_marketplan_execution_log_objs).values_list('BuyerAccount','BuyerAccount').order_by('BuyerAccount')

class t_config_user_buyer_task(models.Model):
    StaffId      = models.CharField(u'员工ID',max_length=32,blank = True,null = True )
    FirstName    = models.CharField(u'中文名称',max_length=32,blank = True,null = True)
    Updatetime   = models.DateTimeField(u'更新时间',auto_now_add=True,blank = True,null = True )

    class Meta:
        verbose_name = u'营销执行表'
        verbose_name_plural = verbose_name
        db_table = 't_config_user_buyer_task'
    def __unicode__(self):
        return u'%s'%(self.StaffId)
