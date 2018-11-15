# -*- coding: utf-8 -*-
from django.db import models
from public import *

        
class t_store_execution_aliexpress(models.Model):
    type_num            =    models.IntegerField(u'单识别号',blank = True,null = True)
    shopname            =    models.CharField(u'店铺名称',max_length=64,blank = True,null = True)
    productid           =    models.CharField(u'产品ID',max_length=64,blank = True,null = True)
    MainSKU             =    models.CharField(u'主SKU',max_length=64,blank = True,null = True)
    money               =    models.DecimalField(u'金额($)',max_digits=6,decimal_places=2,blank = True,null = True)
    count               =    models.IntegerField(u'数量',blank = True,null = True)
    remark              =    models.TextField(u'备注',blank = True,null = True)
    reason              =    models.CharField(u'营销原因',max_length=64,blank = True,null = True)
    createman           =    models.CharField(u'提交人',max_length=64,blank = True,null = True)
    createtime          =    models.DateTimeField(u'提交日期',blank = True,null = True)     
    ordernum            =    models.CharField(u'订单号',max_length=64,blank = True,null = True)
    tracenum            =    models.CharField(u'跟踪号',max_length=64,blank = True,null = True)
    sd_time             =    models.DateField(u'刷单时间',blank = True,null = True)
    sd_man              =    models.CharField(u'刷单人',max_length=64,blank = True,null = True)
    jd_man              =    models.CharField(u'截单人',max_length=64,blank = True,null = True)
    yx_fee              =    models.DecimalField(u'营销费用(美金)',max_digits=6,decimal_places=2,blank = True,null = True)
    route_name          =    models.CharField(u'线路名称',max_length=64,blank = True,null = True)
    ip                  =    models.CharField(u'ip地址',max_length=64,blank = True,null = True)
    buyer_account       =    models.CharField(u'买家账号',max_length=64,blank = True,null = True)   
    pay_account         =    models.CharField(u'支付卡账号',max_length=64,blank = True,null = True)
    pj_time_man         =    models.CharField(u'评价日期/评价人',max_length=64,blank = True,null = True)
    
    class Meta:
        verbose_name=u'Aliexpress营销执行结果表'
        verbose_name_plural=verbose_name
        db_table = 't_store_execution_aliexpress'
        ordering = ['-type_num']

    def __unicode__(self):
        return u'%s'%(self.id)