# -*- coding: utf-8 -*-
from django.db import models


class t_online_info_15day_amazon(models.Model):
    item_name                    =   models.TextField(u'item_name',max_length=64,blank = True,null = True)
    item_description             =   models.TextField(u'item_description',max_length=64,blank = True,null = True)
    listing_id                   =   models.CharField(u'listing_id',max_length=64,blank = True,null = True)
    seller_sku                   =   models.CharField(u'seller_sku',max_length=128,blank = True,null = True)
    price                        =   models.CharField(u'price',max_length=64,blank = True,null = True)
    quantity                     =   models.CharField(u'quantity',max_length=31,blank = True,null = True)
    open_date                    =   models.DateTimeField(u'open_date(PDT)',blank = True,null = True)
    image_url                    =   models.TextField(u'image_url',max_length=100,blank = True,null = True)
    item_is_marketplace          =   models.CharField(u'item_is_marketplace',max_length=64,blank = True,null = True)
    product_id_type              =   models.CharField(u'product_id_type',max_length=64,blank = True,null = True)
    zshop_shipping_fee           =   models.CharField(u'zshop_shipping_fee',max_length=64,blank = True,null = True)
    item_note                    =   models.CharField(u'item_note',max_length=64,blank = True,null = True)
    item_condition               =   models.CharField(u'item_condition',max_length=64,blank = True,null = True)
    zshop_category1              =   models.CharField(u'zshop_category1',max_length=31,blank = True,null = True)
    zshop_browse_path            =   models.CharField(u'zshop_browse_path',max_length=64,blank = True,null = True)
    zshop_storefront_feature     =   models.CharField(u'zshop_storefront_feature',max_length=64,blank = True,null = True)
    asin1                        =   models.CharField(u'asin1',max_length=64,blank = True,null = True)
    asin2                        =   models.CharField(u'asin2',max_length=64,blank = True,null = True)
    asin3                        =   models.CharField(u'asin3',max_length=64,blank = True,null = True)
    will_ship_internationally    =   models.CharField(u'will_ship_internationally',max_length=64,blank = True,null = True)
    expedited_shipping           =   models.CharField(u'expedited_shipping',max_length=64,blank = True,null = True)
    zshop_boldface               =   models.CharField(u'zshop_boldface',max_length=31,blank = True,null = True)
    product_id                   =   models.CharField(u'product_id',max_length=64,blank = True,null = True)
    bid_for_featured_placement   =   models.CharField(u'bid_for_featured_placement',max_length=64,blank = True,null = True)
    add_delete                   =   models.CharField(u'add_delete',max_length=64,blank = True,null = True)
    pending_quantity             =   models.CharField(u'pending_quantity',max_length=64,blank = True,null = True)
    fulfillment_channel          =   models.CharField(u'fulfillment_channel',max_length=64,blank = True,null = True)
    merchant_shipping_group      =   models.CharField(u'merchant_shipping_group',max_length=64,blank = True,null = True)
    ShopName                     =   models.FileField(u'ShopName',max_length=64,blank = True,null = True)
    SKU                          =   models.CharField(u'SKU',max_length=31,blank = True,null = True)
    UpdateTime                   =   models.DateTimeField(u'UpdateTime',blank = True,null = True)
    order7days  = models.IntegerField(u'7天销量',max_length=10,blank = True,null = True )
    orderydays  = models.IntegerField(u'昨日销量',max_length=10,blank = True,null = True )
    ordertdays  = models.IntegerField(u'今日销量',max_length=10,blank = True,null = True )
    ordercdays  = models.IntegerField(u'销量差值',max_length=10,blank = True,null = True )
    allorder    = models.IntegerField(u'总销量',max_length=10,blank = True,null = True )
    
    class Meta:
        verbose_name=u'AMA-15天爆款'
        verbose_name_plural=verbose_name
        db_table = 't_online_info_amazon'
        
    def __unicode__(self):
        return u'%s'%(self.id)
