# -*- coding: utf-8 -*-
from django.db import models
from public import *

        
class t_store_marketplan_execution_joom(models.Model):

    shopname            =    models.CharField(u'店铺名称',max_length=64,blank = True,null = True)
    productid           =    models.CharField(u'产品ID',max_length=64,blank = True,null = True)
    ParentSKU           =    models.CharField(u'ParentSKU',max_length=64,blank = True,null = True)
    pySKU               =    models.CharField(u'普源SKU',max_length=64,blank = True,null = True)
    money               =    models.DecimalField(u'价格($)',max_digits=6,decimal_places=2,blank = True,null = True)
    colorsize           =    models.CharField(u'颜色/尺码',max_length=64,blank = True,null = True)
    remark              =    models.TextField(u'备注',blank = True,null = True)
    createman           =    models.CharField(u'提交人',max_length=64,blank = True,null = True)
    createtime          =    models.DateField(u'提交日期',blank = True,null = True) 
    lp_time             =    models.DateField(u'留评时间',blank = True,null = True)
    price               =    models.DecimalField(u'金额($)',max_digits=6,decimal_places=2,blank = True,null = True)
    route_name          =    models.CharField(u'线路名称',max_length=64,blank = True,null = True)
    vpn                 =    models.CharField(u'VPN信息',max_length=64,blank = True,null = True)
    buyer_account       =    models.CharField(u'买家账号(facebook)',max_length=64,blank = True,null = True)
    buyer_id            =    models.CharField(u'买家ID',max_length=64,blank = True,null = True)
    pp_account          =    models.CharField(u'PP账号',max_length=64,blank = True,null = True)
    yx_man_time         =    models.CharField(u'营销人/营销时间',max_length=64,blank = True,null = True)   
    tracenumber         =    models.CharField(u'跟踪号',max_length=64,blank = True,null = True)
    order_id            =    models.CharField(u'Order ID',max_length=64,blank = True,null = True)
    jd_status           =    models.CharField(u'是否截单',max_length=11,blank = True,null = True)
    
    class Meta:
        verbose_name=u'Joom营销计划执行表'
        verbose_name_plural=verbose_name
        db_table = 't_store_marketplan_execution_joom'

    def __unicode__(self):
        return u'%s'%(self.id)