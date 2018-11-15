# -*- coding: utf-8 -*-
from django.db import models

class t_config_paypal_account(models.Model):
    Paypal_Account = models.CharField(u'paypal账号',max_length=50,blank = True,null = True)
    Client_Id      = models.CharField(u'Client_id',max_length=100,blank = True,null = True)
    Client_Secret  = models.CharField(u'Client_Secret', max_length=100, blank=True, null=True)
    Api_UserName   = models.CharField(u'Api_UserName', max_length=100, blank=True, null=True)
    Api_Password   = models.CharField(u'Api_Password', max_length=100, blank=True, null=True)
    Api_Signature  = models.CharField(u'Api_Signature', max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = u'paypal账号配置表'
        verbose_name_plural = u'paypal账号配置表'
        db_table = 't_config_paypal_account'
    def __unicode__(self):
        return u'Paypal_Account=%s Client_Id=%s Client_Secret=%s Api_UserName=%s Api_Password=%s ' \
               u'Api_Signature=%s'%(self.Paypal_Account,self.Client_Id,self.Client_Secret,self.Api_UserName,self.Api_Password,self.Api_Signature)