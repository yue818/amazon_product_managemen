# -*- coding: utf-8 -*-
from django.db import models

class t_upload_statistics_table(models.Model):
    UplLoad_nub            =   models.IntegerField(u'铺货数',max_length=11,blank = True,null = False)
    Upload_suc_nub         =   models.IntegerField(u'铺货成功数',max_length=11,blank = True,null = False)
    Shop_nub               =   models.IntegerField(u'铺货店铺数',max_length=11,blank = True,null = False)
    ShopName               =   models.TextField(u'所有店铺',blank = True,null = False)
    SKU_nub                =   models.IntegerField(u'铺货SKU数',max_length=11,blank = True,null = False)
    online_nub             =   models.IntegerField(u'铺货在线数',max_length=11,blank = True,null = False)
    order_nub              =   models.IntegerField(u'出单链接数',max_length=11,blank = True,null = False)
    order_rate             =   models.FloatField(u'出单链接率',max_length=11,blank = True,null = False)
    staTime                =   models.DateField(u'统计日',blank = True,null = False)
    orderofeday            =   models.IntegerField(u'当日订单数',max_length=11,blank = True,null = False)
    orders                 =   models.IntegerField(u'当日链接订单数',max_length=11,blank = True,null = False)
    soldofeay              =   models.IntegerField(u'当日销售金额',max_length=11,blank = True,null = False)
    sold                   =   models.IntegerField(u'当日链接销售金额',max_length=11,blank = True,null = False)
    Integrity_nub          =   models.IntegerField(u'诚信店铺数',max_length=11,blank = True,null = False)
    
    class Meta:
        verbose_name=u'铺货统计'
        verbose_name_plural=verbose_name
        db_table = 't_upload_statistics_table'
        ordering = ['-staTime']
    def __unicode__(self):
        return u'id:%s'%(self.id)