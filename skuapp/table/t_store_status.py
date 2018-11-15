# -*- coding: utf-8 -*-
from django.db import models
from public import *

class t_store_status(models.Model):
    ShopName            =   models.CharField(u'卖家简称',max_length=32,blank = True,null = True)
    Seller              =   models.CharField(u'店长/销售员',max_length=32,blank = True,null = True)
    StoreStatus         =   models.CharField(u'店铺状态',max_length=32,blank = True,null = True)
    AccountName         =   models.CharField(u'店铺账号',max_length=32,blank = True,null = True)
    AccountNote         =   models.TextField(u'店铺账号备注',max_length=127,blank = True,null = True)
    PaymentSituation    =   models.CharField(u'缴费情况',max_length=32,blank = True,null = True)
    PaymentRemarks      =   models.TextField(u'缴费情况备注',max_length=127,blank = True,null = True)
    AccountNumber       =   models.CharField(u'账户编号',max_length=32,blank = True,null = True)
    AccountManager      =   models.CharField(u'现客户经理',max_length=32,blank = True,null = True)
    CardNumber          =   models.CharField(u'绑定卡号/账户号',max_length=32,blank = True,null = True)
    ShopOperationsNote  =   models.TextField(u'店铺运营情况备注',max_length=127,blank = True,null = True)
    CreateStaffName     =   models.CharField(u'提交人',max_length=32,blank = True,null = True)
    CreateTime          =   models.DateTimeField(u'提交时间',blank = True,null = True)
    DepartmentID        =   models.CharField(u'部门编号',max_length=10,blank = True,null = True)
    
    class Meta:
        verbose_name=u'店铺状态一览表'
        verbose_name_plural=verbose_name
        db_table = 't_store_status'

    def __unicode__(self):
        return u'%s'%(self.id)