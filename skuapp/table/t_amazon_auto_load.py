# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: t_amazon_auto_load.py
 @time: 2018/11/2 15:35
"""
from django.db import models


class t_amazon_auto_load(models.Model):
    batch_id = models.CharField(u'批次号', max_length=64, blank=True, null=True)
    shop_name = models.CharField(u'店铺', max_length=32, blank=True, null=True)
    seller_sku = models.CharField(u'店铺SKU', max_length=255, blank=True, null=True)
    sku = models.CharField(u'商品SKU', max_length=255, blank=True, null=True)
    sku_type = models.CharField(u'SKU类型', max_length=255, blank=True, null=True)
    com_pro_sku = models.CharField(u'组合SKU值', max_length=500, blank=True, null=True)
    status = models.CharField(u'链接状态', max_length=32, blank=True, null=True)
    product_status_detail = models.CharField(u'商品状态明细', max_length=1024, blank=True, null=True)
    product_sku_status = models.CharField(u'商品状态', max_length=2, blank=True, null=True)
    quantity = models.CharField(u'商品库存', max_length=10, blank=True, null=True)
    insert_time = models.DateTimeField(u'数据插入时间', blank=True, null=True)
    deal_type = models.CharField(u'处理类型', max_length=32, blank=True, null=True)
    deal_user = models.CharField(u'操作人', max_length=64, blank=True, null=True)
    deal_result = models.CharField(u'处理结果', max_length=32, blank=True, null=True)
    deal_remark = models.CharField(u'处理备注', max_length=32, blank=True, null=True)
    deal_time = models.DateTimeField(u'处理时间', blank=True, null=True)

    class Meta:
        verbose_name = u'亚马逊自动上下架记录'
        verbose_name_plural = verbose_name
        db_table = 't_amazon_auto_load'

    def __unicode__(self):
        return u'%s' % self.id