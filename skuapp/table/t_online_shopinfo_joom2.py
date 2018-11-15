# -*- coding: utf-8 -*-
from django.db import models


class t_online_shopinfo_joom2(models.Model):
    product_id                   =   models.CharField(u'product_id',max_length=64,blank = True,null = True)
    name                         =   models.TextField(u'name',max_length=200,blank = True,null = True)
    description                  =   models.TextField(u'description',max_length=200,blank = True,null = True)
    parent_sku                   =   models.CharField(u'parent_sku',max_length=16,blank = True,null = True)
    number_sold                  =   models.IntegerField(u'number_sold',blank = True,null = True)
    number_saves                 =   models.IntegerField(u'number_saves',blank = True,null = True)
    number_orders                =   models.IntegerField(u'number_orders',blank = True,null = True)
    number_refunds               =   models.IntegerField(u'number_refunds',blank = True,null = True)
    refund_rate                  =   models.IntegerField(u'refund_rate',blank = True,null = True)
    review_status                =   models.CharField(u'review_status',max_length=16,blank = True,null = True)
    main_image                   =   models.CharField(u'main_image',max_length=250,blank = True,null = True)
    extra_images                 =   models.CharField(u'extra_images',max_length=250,blank = True,null = True)
    original_image_url           =   models.CharField(u'original_image_url',max_length=250,blank = True,null = True)
    tags                         =   models.CharField(u'tags',max_length=32,blank = True,null = True)
    is_promoted                  =   models.CharField(u'is_promoted',max_length=10,blank = True,null = True)
    VariantSKU                   =   models.CharField(u'VariantSKU',max_length=64,blank = True,null = True)
    #sku                          =   models.CharField(u'sku',max_length=16,blank = True,null = True)
    price                        =   models.DecimalField(u'price',max_digits=5,decimal_places=2,blank = True,null = True)
    shipping                     =   models.CharField(u'shipping',max_length=10,blank = True,null = True)
    msrp                         =   models.CharField(u'msrp',max_length=10,blank = True,null = True)
    inventory                    =   models.CharField(u'inventory',max_length=16,blank = True,null = True)
    shipping_time                =   models.DateTimeField(u'shipping_time',blank = True,null = True)
    size                         =   models.IntegerField(u'size',blank = True,null = True)
    #Variant_enabled              =   models.CharField(u'Variant_enabled',max_length=64,blank = True,null = True)
    date_uploaded                =   models.DateTimeField(u'date_uploaded',blank = True,null = True)
    product_enabled              =   models.CharField(u'product_enabled',max_length=16,blank = True,null = True)
    
    
    class Meta:
        verbose_name=u'Joom2在线商品信息'
        verbose_name_plural=verbose_name
        db_table = 't_online_shopinfo_joom2'
        
    def __unicode__(self):
        return u'%s'%(self.id)
