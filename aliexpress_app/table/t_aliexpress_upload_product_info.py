#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from skuapp.table.t_store_configuration_file import t_store_configuration_file

aliexpress_shopnames = t_store_configuration_file.objects.filter(ShopName_temp__startswith='Ali-').order_by('ShopName').values('ShopName')
ALISHOPNAMES = list()
for i in aliexpress_shopnames:
    ALISHOPNAMES.append((i['ShopName'], i['ShopName']))
ALISHOPNAMES = tuple(ALISHOPNAMES)


# 上传 Aliexpress商品信息
class t_aliexpress_upload_product_info(models.Model):

    UploadUser = models.CharField(u'上传人', max_length=255, blank=True, null=True)
    UploadDatetime = models.DateTimeField(u'上传时间', blank=True, null=True)
    SallingFile = models.FileField(u'销售中商品数据', upload_to='aliexpress_salling_product_file/%Y/%m', blank=True, null=True)
    DisableFile = models.FileField(u'下架商品数据', upload_to='aliexpress_disable_product_file/%Y/%m', blank=True, null=True)
    ImportFlag = models.BooleanField(u'是否导入完成', blank=True, default=False)
    ImportUser = models.CharField(u'导入人', max_length=255, blank=True, null=True)
    ImportDatetime = models.DateTimeField(u'导入时间', blank=True, null=True)
    ImportRes = models.TextField(u'导入结果', blank=True, null=True)
    ShopName = models.CharField(u'店铺', choices=ALISHOPNAMES, max_length=255, null=True)

    class Meta:
        verbose_name = u'Aliexpress 上传商品信息'
        verbose_name_plural = verbose_name
        db_table = 't_aliexpress_upload_product_info'
        ordering = ['-id']

    def __unicode__(self):
        return u'id:%s' % (self.id)
