# -*- coding: utf-8 -*-
from django.db import models


class b_goods_sales_count(models.Model):
    id = models.IntegerField(primary_key=True)
    sku = models.CharField(u'商品sku', max_length=100, blank=True, null=True)
    goodsname = models.CharField(u'商品名称', max_length=300, blank=True, null=True)
    goodsstatus = models.CharField(u'商品状态', max_length=100, blank=True, null=True)
    devdate = models.CharField(u'开发时间', max_length=100, blank=True, null=True)
    salername = models.CharField(u'销售员', max_length=255, blank=True, null=True)
    purchaser = models.CharField(u'采购员', max_length=255, blank=True, null=True)
    inter_val = models.CharField(u'iter_val', max_length=255, blank=True, null=True)


    class Meta:
        verbose_name = u'SKU销量统计'
        verbose_name_plural = verbose_name
        db_table = 'b_goods_sales_count'
        ordering = ['id']