# -*- coding: utf-8 -*-
from django.db import models
from public import *
        
        
class t_store_summary_of_sales_profit_data(models.Model):
    ShopName            =   models.CharField(u'卖家简称',max_length=32,blank = True,null = True)
    Seller              =   models.CharField(u'负责人/销售员',max_length=32,blank = True,null = True)
    ShopAccount         =   models.CharField(u'店铺账号',max_length=32,blank = True,null = True)
    StartTime           =   models.CharField(u'开始时间',max_length=32,blank = True,null = True)
    EndTime             =   models.CharField(u'结束时间',max_length=32,blank = True,null = True)
    Sales               =   models.CharField(u'销售额',max_length=10,blank = True,null = True)
    PaidProfits         =   models.CharField(u'实收利润',max_length=10,blank = True,null = True)
    ProfitMargins       =   models.CharField(u'利润率',max_length=10,blank = True,null = True)
    PreviouSales        =   models.CharField(u'上期销售额',max_length=10,blank = True,null = True)
    Increase            =   models.CharField(u'增长额',max_length=10,blank = True,null = True)
    GrowthRate          =   models.CharField(u'增长幅度',max_length=10,blank = True,null = True)
    Remarks             =   models.TextField(u'备注',max_length=100,blank = True,null = True)
    CreateStaffName     =   models.CharField(u'提交人',max_length=16,blank = True,null = True)
    CreateTime          =   models.DateTimeField(u'提交时间',blank = True,null = True)
    DepartmentID        =   models.CharField(u'部门编号',max_length=10,blank = True,null = True)
    
    class Meta:
        verbose_name=u'销售额利润数据汇总表'
        verbose_name_plural=verbose_name
        db_table = 't_store_summary_of_sales_profit_data'

    def __unicode__(self):
        return u'%s'%(self.id)