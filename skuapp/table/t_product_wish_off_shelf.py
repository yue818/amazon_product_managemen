# coding=utf-8


from django.db import models
from public import *


class t_product_wish_off_shelf(models.Model):

    ProductSKU      =   models.CharField(u'商品SKU', max_length=32, blank=True, null=True)
    ShopSKU         =   models.CharField(u'店铺SKU', max_length=256, blank=True, null=True)
    ShopName        =   models.CharField(u'店铺名', max_length=32, blank=True, null=True)
    Reason          =   models.CharField(u'操作原因', max_length=32, choices=getChoices(ChoiceOffShelfReason), blank=True, null=True)
    ExcelFile       =   models.FileField(u'文件', blank=True, null=True)
    CreateTime      =   models.DateTimeField(u'创建时间', blank=True, null=True)
    CreateStaff     =   models.CharField(u'创建人', max_length=16, blank=True, null=True)
    Result          =   models.CharField(u'操作结果', max_length=10, choices=getChoices(ChoiceOffShelfResult), blank=True, null=True)
    ErrorInfo       =   models.TextField(u'失败原因', blank=True, null=True)
    Method          =   models.TextField(u'下架方式', max_length=32, blank=True, null=True)

    class Meta:
        verbose_name = u'WISH商品下架'
        verbose_name_plural = verbose_name
        db_table = 't_product_wish_off_shelf'
        ordering = ['-id']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)
