# -*- coding: utf-8 -*-
from django.db import models
from public import *

        
class t_store_marketplan_execution_amazon(models.Model):

    shopaccount         =    models.CharField(u'卖家账号',max_length=64,blank = True,null = True)
    country             =    models.CharField(u'国家',max_length=64,blank = True,null = True)
    SKU                 =    models.CharField(u'物品SKU',max_length=64,blank = True,null = True)
    ProductTitle        =    models.TextField(u'产品标题',blank = True,null = True)
    money               =    models.DecimalField(u'单笔金额+',max_digits=6,decimal_places=2,blank = True,null = True)
    colorsize           =    models.CharField(u'颜色尺寸',max_length=64,blank = True,null = True)
    evaluate_type       =    models.CharField(u'留评类型',max_length=64,blank = True,null = True)
    count               =    models.CharField(u'数量',max_length=64,blank = True,null = True)
    createman           =    models.CharField(u'填写人',max_length=64,blank = True,null = True)
    createtime          =    models.DateField(u'提交日期',blank = True,null = True)
    buyer_machine       =    models.CharField(u'买家账号本地机器信息',max_length=64,blank = True,null = True)
    ip                  =    models.CharField(u'IP地址',max_length=64,blank = True,null = True)
    buyer_account       =    models.CharField(u'对应买家账号',max_length=64,blank = True,null = True)
    shopnumber          =    models.CharField(u'店铺单号',max_length=64,blank = True,null = True)
    sd_man              =    models.CharField(u'刷单人员',max_length=64,blank = True,null = True)
    sd_time             =    models.DateField(u'刷单时间',blank = True,null = True)
    jd_man              =    models.CharField(u'截单人员',max_length=64,blank = True,null = True)
    mark1               =    models.TextField(u'备注1',blank = True,null = True)
    mark2               =    models.TextField(u'备注2',blank = True,null = True)
    wl_tracenumber      =    models.CharField(u'物流和跟踪号',max_length=64,blank = True,null = True)
    lp_info             =    models.CharField(u'确认收货/留评',max_length=64,blank = True,null = True)
    cs_refund           =    models.CharField(u'测试单退款',max_length=64,blank = True,null = True)
    
    class Meta:
        verbose_name=u'Amazon营销计划执行表'
        verbose_name_plural=verbose_name
        db_table = 't_store_marketplan_execution_amazon'

    def __unicode__(self):
        return u'%s'%(self.id)