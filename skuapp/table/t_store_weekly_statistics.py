# -*- coding: utf-8 -*-
from django.db import models
from public import *
         
        
class t_store_weekly_statistics(models.Model):
    ShopName            =   models.CharField(u'卖家简称',max_length=32,blank = True,null = True)
    ShopAccount         =   models.CharField(u'店铺账号',max_length=32,blank = True,null = True)
    InvoiceTime         =   models.CharField(u'发票时间',max_length=32,blank = True,null = True)
    PromotionCosts      =   models.CharField(u'平台推广费用',max_length=10,blank = True,null = True)
    TrafficCosts        =   models.CharField(u'流量费用',max_length=10,blank = True,null = True)
    SpendSubtotal       =   models.CharField(u'花费小计',max_length=10,blank = True,null = True)
    RefundAmount        =   models.CharField(u'退款金额',max_length=10,blank = True,null = True)
    OtherFee            =   models.CharField(u'其他费用',max_length=10,blank = True,null = True)
    TotalSales          =   models.CharField(u'销售总额',max_length=10,blank = True,null = True)
    AmountMoney         =   models.CharField(u'打款金额',max_length=10,blank = True,null = True)
    Remarks             =   models.TextField(u'备注',max_length=100,blank = True,null = True)
    CreateStaffName     =   models.CharField(u'提交人',max_length=16,blank = True,null = True)
    CreateTime          =   models.DateTimeField(u'提交时间',blank = True,null = True)
    DepartmentID        =   models.CharField(u'部门编号',max_length=10,blank = True,null = True)
    
    class Meta:
        verbose_name=u'店铺费用周统计表'
        verbose_name_plural=verbose_name
        db_table = 't_store_weekly_statistics'

    def __unicode__(self):
        return u'%s'%(self.id)