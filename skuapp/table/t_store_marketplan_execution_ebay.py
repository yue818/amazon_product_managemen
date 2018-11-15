# -*- coding: utf-8 -*-
from django.db import models
from public import *

        
class t_store_marketplan_execution_ebay(models.Model):

    platform           =    models.CharField(u'平台名称',max_length=64,blank = True,null = True)
    product_code       =    models.CharField(u'物品编号',max_length=64,blank = True,null = True)
    product_sku        =    models.CharField(u'物品SKU',max_length=64,blank = True,null = True)
    execution_count    =    models.IntegerField(u'营销数量',blank = True,null = True)
    shop_account       =    models.CharField(u'卖家账号',max_length=64,blank = True,null = True)
    createman          =    models.CharField(u'提交人',max_length=64,blank = True,null = True)
    create_time        =    models.DateField(u'提交时间',blank = True,null = True)
    buyer_machine      =    models.CharField(u'买家账号本地机器',max_length=64,blank = True,null = True)
    vpn                =    models.CharField(u'vpn信息',max_length=64,blank = True,null = True)
    buyer_account      =    models.CharField(u'对应买家账号',max_length=64,blank = True,null = True)
    status             =    models.CharField(u'完成进度',max_length=64,blank = True,null = True)
    execution_man      =    models.CharField(u'营销人员',max_length=64,blank = True,null = True)
    execution_time     =    models.DateField(u'营销时间',blank = True,null = True)
    execution_money    =    models.DecimalField(u'执行金额($)',max_digits=6,decimal_places=2,blank = True,null = True)
    jd_status          =    models.CharField(u'是否已截单',max_length=64,blank = True,null = True)
    jd_man             =    models.CharField(u'截单人',max_length=64,blank = True,null = True)
    lp_man             =    models.CharField(u'留评人',max_length=64,blank = True,null = True)
    lp_time            =    models.DateField(u'留评时间',blank = True,null = True)
    remark             =    models.TextField(u'备注',blank = True,null = True)
    
    class Meta:
        verbose_name=u'Ebay营销计划执行表'
        verbose_name_plural=verbose_name
        db_table = 't_store_marketplan_execution_ebay'

    def __unicode__(self):
        return u'%s'%(self.id)