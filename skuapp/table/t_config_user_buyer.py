# -*- coding: utf-8 -*-
from django.db import models
from .public import *


class t_config_user_buyer(models.Model):
    StaffId      = models.CharField(u'员工ID',max_length=32,blank = True,null = True)  
    BuyerAccount = models.CharField(u'买家账号',max_length=63,blank = True,null = True)
    CreateTime   = models.DateTimeField(u'创建时间',auto_now_add=True,blank = True,null = True)
    UpdateTime   = models.DateTimeField(u'更新时间',auto_now=True,blank = True,null = True )
    Status       = models.CharField(u'状态',max_length=32,choices=getChoices(ChoiceYN))
    PaypalAccount= models.CharField(u'Paypal账号', max_length=32,blank = True,null = True)
    Balance      = models.DecimalField(u'余额',max_digits=6,decimal_places=2,blank=False,null=False)
    UserID       = models.CharField(u'UserID',max_length=100,blank = True,null = True)

    class Meta:
        verbose_name = u'买家账号配置表'
        verbose_name_plural = verbose_name
        db_table = 't_config_user_buyer'
    def __unicode__(self):
        return u'StaffId=%s BuyerAccount=%s Status=%s Balance=%s'%(self.StaffId,self.BuyerAccount,self.Status,self.Balance)
