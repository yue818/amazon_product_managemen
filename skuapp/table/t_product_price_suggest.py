#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_product_price_suggest.py
 @time: 2018-08-08 13:50
"""

from django.db import models

class t_product_price_suggest(models.Model):
    id = models.AutoField(u'流水号', primary_key=True)

    SKU             = models.CharField(u'商品SKU', max_length=50, blank=True, null=True)
    GoodsStatus     = models.CharField(u'商品状态', max_length=20, blank=True, null=True)
    StoreName       = models.CharField(u'仓库', max_length=50, blank=True, null=True)
    GoodsName       = models.CharField(u'商品名称', max_length=100, blank=True, null=True)
    SupplierName    = models.CharField(u'供应商', max_length=100, blank=True, null=True)
    SalerName2      = models.CharField(u'业绩归属人', max_length=16, blank=True, null=True)
    Purchaser       = models.CharField(u'采购员', max_length=16, blank=True, null=True)
    Number          = models.IntegerField(u'库存',  blank=True, null=True)
    SellCount1      = models.IntegerField(u'7天销量', blank=True, null=True)
    SellCount2      = models.IntegerField(u'15天销量', blank=True, null=True)
    SellCount3      = models.IntegerField(u'30天销量', blank=True, null=True)
    UseNumber       = models.IntegerField(u'可用库存', blank=True, null=True)
    CostPrice       = models.DecimalField(u'当前单价', max_digits=10, decimal_places=2, blank=True, null=True)
    CreateDate      = models.DateField(u'创建日期', blank=True, null=True)
    LinkUrl         = models.CharField(u'图片地址', max_length=500, blank=True, null=True)
    Updatetime      = models.DateTimeField(u'更新时间',)

    class Meta:
        verbose_name = u'建议核价清单'
        verbose_name_plural = verbose_name
        db_table = 't_product_price_suggest'
        ordering = ['-SellCount1']

    def __unicode__(self):
        return u'%s' % (self.SKU)