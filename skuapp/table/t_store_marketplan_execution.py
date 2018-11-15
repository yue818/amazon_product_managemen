# -*- coding: utf-8 -*-
from django.db import models
from public import *

        
class t_store_marketplan_execution(models.Model):
    ShopName                     =   models.CharField(u'卖家简称',max_length=32,blank = True,null = True)
    ShopAccount                  =   models.CharField(u'店铺账号',max_length=32,blank = True,null = True)
    ProductID                    =   models.CharField(u'产品ID',max_length=32,blank = True,null = True)
    ParentSKU                    =   models.CharField(u'ParentSKU',max_length=32,blank = True,null = True)
    Price                        =   models.DecimalField(u'商品价格($)',max_digits=6,decimal_places=2,blank=False,null=False)
    Demand                       =   models.IntegerField(u'总需求量')
    Quantity                     =   models.IntegerField(u'营销数量',default=0,blank=True,null=True)
    Tracking                     =   models.CharField(u'跟踪单号',max_length=32,blank = True,null = True)
    Remarks                      =   models.TextField(u'备注',max_length=100,blank = True,null = True)
    BuyerAccountLocalmachineinfo =   models.CharField(u'买家账号本地机器信息',max_length=32,blank = True,null = True)
    VpnInfo                      =   models.CharField(u'vpn信息',max_length=32,blank = True,null = True)
    BuyerAccount                 =   models.CharField(u'买家账号',max_length=32,blank = True,null = True)
    ShopNumber                   =   models.CharField(u'店铺单号',max_length=32,blank = True,null = True)
    BrushPerson                  =   models.CharField(u'营销人员',max_length=32,blank = True,null = True)
    BrushTime                    =   models.CharField(u'营销时间',max_length=32,blank = True,null = True) 
    CutPerson                    =   models.CharField(u'截单人员',max_length=16,blank = True,null = True)
    CutTime                      =   models.CharField(u'截单时间',max_length=32,blank = True,null = True)
    CreateStaffName              =   models.CharField(u'提交人',max_length=16,blank = True,null = True)
    DepartmentID                 =   models.CharField(u'部门编号',max_length=10,blank = True,null = True)
    CreateTime                   =   models.DateTimeField(u'提交时间',auto_now_add=True,blank = True,null = True)
    
    class Meta:
        verbose_name=u'营销计划表'
        verbose_name_plural=verbose_name
        db_table = 't_store_marketplan_execution'

    def __unicode__(self):
        return u'%s'%(self.id)