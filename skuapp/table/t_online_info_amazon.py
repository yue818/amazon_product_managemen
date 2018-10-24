# -*- coding: utf-8 -*-
from django.db import models


class t_online_info_amazon(models.Model):
    item_name = models.TextField(u'商品标题',  max_length=1000,  blank=True,  null=True)
    item_description = models.TextField(u'商品描述',  max_length=2000,  blank=True,  null=True)
    listing_id = models.CharField(u'listing_id', max_length=64, blank=True, null=True)
    seller_sku = models.CharField(u'店铺SKU', max_length=128, blank=True, null=True)
    price = models.FloatField(u'售价', max_length=64, blank=True, null=True)
    quantity = models.IntCharFieldegerField(u'库存', max_length=32, blank=True, null=True)
    open_date = models.DateTimeField(u'open_date(PDT)', blank=True, null=True)
    image_url = models.TextField(u'图片', max_length=100, blank=True, null=True)
    item_is_marketplace = models.CharField(u'item_is_marketplace', max_length=64, blank=True, null=True)
    product_id_type = models.CharField(u'商品编码类型', max_length=64, blank=True, null=True)
    item_condition = models.CharField(u'商品状态编码', max_length=64, blank=True, null=True)
    asin1 = models.CharField(u'ASIN', max_length=64, blank=True, null=True)
    expedited_shipping = models.CharField(u'expedited_shipping', max_length=64, blank=True, null=True)
    product_id = models.CharField(u'商品编码', max_length=64, blank=True, null=True)
    add_delete = models.CharField(u'add_delete', max_length=64, blank=True, null=True)
    pending_quantity = models.CharField(u'等待购买量', max_length=64, blank=True, null=True)
    fulfillment_channel = models.CharField(u'配送方式', max_length=64, blank=True, null=True)
    merchant_shipping_group = models.CharField(u'merchant_shipping_group', max_length=64, blank=True, null=True)
    ShopName = models.CharField(u'店铺名', max_length=64, blank=True, null=True)
    SKU = models.CharField(u'SKU', max_length=31, blank=True, null=True)
    UpdateTime = models.DateTimeField(u'更新时间', blank=True, null=True)
    order7days = models.IntegerField(u'7天销量', max_length=10, blank=True, null=True )
    orderydays = models.IntegerField(u'昨日销量', max_length=10, blank=True, null=True )
    ordertdays = models.IntegerField(u'今日销量', max_length=10, blank=True, null=True )
    ordercdays = models.IntegerField(u'销量差值', max_length=10, blank=True, null=True )
    allorder = models.IntegerField(u'总销量', max_length=10, blank=True, null=True )
    is_fba = models.IntegerField(u'是否FBA',  max_length=1,  blank=True,  null=True)
    orders_7days = models.IntegerField(u'7天订单量',  max_length=5,  blank=True,  null=True)
    orders_15days = models.IntegerField(u'15天订单量',  max_length=10,  blank=True,  null=True)
    orders_30days = models.IntegerField(u'30天订单量',  max_length=10,  blank=True,  null=True)
    orders_total = models.IntegerField(u'总订单量',  max_length=10,  blank=True,  null=True)
    orders_refund_total = models.IntegerField(u'退款订单数',  max_length=10,  blank=True,  null=True)
    refund_rate = models.FloatField(u'退款率',  max_length=5,  blank=True,  null=True)
    afn_listing_exists = models.CharField(u'FBA链接',  max_length=32,  blank=True,  null=True)
    afn_warehouse_quantity = models.IntegerField(u'FBA库存',  max_length=32,  blank=True,  null=True)

    deal_action = models.CharField(u'操作',  max_length=64,  blank=True,  null=True)
    deal_result = models.CharField(u'处理结果',  max_length=128,  blank=True,  null=True)
    deal_result_info = models.CharField(u'处理结果详情',  max_length=128,  blank=True,  null=True)
    ShopSite = models.FileField(u'ShopSite',  max_length=64,  blank=True,  null=True)
    Status = models.FileField(u'状态',  max_length=32,  blank=True,  null=True)
    Parent_asin = models.CharField(u'Parent_asin', max_length=64, blank=True, null=True)
    product_type = models.IntegerField(u'product_type', max_length=10,  blank=True, null=True)

    product_description = models.TextField(u'产品描述',  blank=True,  null=True)
    bullet_point1 = models.CharField(u'商品描述1',  max_length=248,  blank=True,  null=True)
    bullet_point2 = models.CharField(u'商品描述2',  max_length=248,  blank=True,  null=True)
    bullet_point3 = models.CharField(u'商品描述3',  max_length=248,  blank=True,  null=True)
    bullet_point4 = models.CharField(u'商品描述4',  max_length=248,  blank=True,  null=True)
    bullet_point5 = models.CharField(u'商品描述5',  max_length=248,  blank=True,  null=True)
    generic_keywords1 = models.CharField(u'关键词1',  max_length=48,  blank=True,  null=True)
    generic_keywords2 = models.CharField(u'关键词2',  max_length=48,  blank=True,  null=True)
    generic_keywords3 = models.CharField(u'关键词3',  max_length=48,  blank=True,  null=True)
    generic_keywords4 = models.CharField(u'关键词4',  max_length=48,  blank=True,  null=True)
    generic_keywords5 = models.CharField(u'关键词5',  max_length=48,  blank=True,  null=True)
    sale_price = models.DecimalField(u'促销价格',  max_digits=10, decimal_places=2, blank=True,  null=True)
    sale_from_date = models.DateTimeField(u'促销开始时间',  blank=True,  null=True)
    sale_end_date = models.DateTimeField(u'促销结束时间',  blank=True,  null=True)
    inventory_received_date = models.DateTimeField(u'到货时间',  blank=True,  null=True)
    shipping_price = models.FloatField(u'运费',  max_length=10,  blank=True,  null=True)
    last_price = models.FloatField(u'历史价格',  max_length=10,  blank=True,  null=True)
    last_price_time = models.DateTimeField(u'历史价格日期',  blank=True,  null=True)
    estimated_fee = models.FloatField(u'历史价格',  max_length=10,  blank=True,  null=True)
    refresh_status = models.IntegerField(u'刷新状态',  max_length=1,  blank=True,  null=True)
    refresh_remark = models.CharField(u'刷新备注',  max_length=255,  blank=True,  null=True)
    shop_status = models.IntegerField(u'店铺状态',  max_length=1,  blank=True,  null=True)

    action_remark = models.CharField(u'操作备注',  max_length=255,  blank=True,  null=True)
    upload_time = models.DateTimeField(u'刊登时间',  blank=True,  null=True)
    seller = models.CharField(u'店长/销售员',  max_length=64,  blank=True,  null=True)
    product_status = models.CharField(u'商品状态',  max_length=32,  blank=True,  null=True)

    com_pro_sku = models.CharField(u'商品sku合集',  max_length=2000,  blank=True,  null=True)
    product_size_tier = models.CharField(u'商品尺寸分段',  max_length=32,  blank=True,  null=True)
    sale_rank = models.CharField(u'销售排名',  max_length=32,  blank=True,  null=True)

    class Meta:
        verbose_name = u'AMA商品信息'
        verbose_name_plural = verbose_name
        db_table = 't_online_info_amazon'
        
    def __unicode__(self):
        return u'%s' % self.id
