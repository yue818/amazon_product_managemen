# -*- coding: utf-8 -*-
from django.db import models
from public import *


class t_online_amazon_fba_inventory(models.Model):
    sku                               =   models.CharField(u'店铺SKU',max_length=32,blank = True,null = True)
    fnsku                             =   models.CharField (u'fnsku',max_length=32,blank = True,null = True)
    asin                              =   models.CharField(u'asin',max_length=32,blank = True,null = True)
    product_name                      =   models.CharField(u'product_name',max_length=120,blank = True,null = True)
    condition_a                       =   models.CharField(u'状态',max_length=32,blank = True,null = True)
    your_price                        =   models.CharField(u'价格',max_length=32,blank = True,null = True)
    mfn_listing_exists                =   models.CharField(u'FBM链接',max_length=32,blank = True,null = True)
    mfn_fulfillable_quantity          =   models.IntegerField(u'FBM库存',max_length=32,blank = True,null = True)
    afn_listing_exists                =   models.CharField(u'FBA链接',max_length=32,blank = True,null = True)
    afn_warehouse_quantity            =   models.IntegerField(u'FBA库存数',max_length=32,blank = True,null = True)
    afn_fulfillable_quantity          =   models.IntegerField(u'可售数',max_length=32,blank = True,null = True)
    afn_unsellable_quantity           =   models.IntegerField(u'不可售数',max_length=32,blank = True,null = True)
    afn_reserved_quantity             =   models.IntegerField(u'预留数',max_length=31,blank = True,null = True)
    afn_total_quantity                =   models.IntegerField(u'总数量',max_length=32,blank = True,null = True)
    per_unit_volume                   =   models.CharField(u'单位体积',max_length=32,blank = True,null = True)
    afn_inbound_working_quantity      =   models.IntegerField(u'待入库数',max_length=32,blank = True,null = True)
    afn_inbound_shipped_quantity      =   models.IntegerField(u'在途数',max_length=32,blank = True,null = True)
    afn_inbound_receiving_quantity    =   models.IntegerField(u'正在接收数',max_length=32,blank = True,null = True)
    RefreshTime                       =   models.DateTimeField(u'刷新时间',blank = True,null = True)
    ShopName                          =   models.CharField(u'店铺名称',max_length=32,blank = True,null = True)
    order3days                        =   models.IntegerField(u'三天销量',max_length=32,blank = True,null = True)
    order7days                        =   models.IntegerField(u'七天销量',max_length=32,blank = True,null = True)
    selltime                          =   models.DateTimeField(u'可售时间',blank = True,null = True)
    
    class Meta:
        verbose_name=u'Amazon库存管理'
        verbose_name_plural=verbose_name
        db_table = 't_online_amazon_fba_inventory'
    def __unicode__(self):
        return u'%s'%(self.id)