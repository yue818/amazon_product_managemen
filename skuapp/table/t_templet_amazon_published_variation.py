#-*-coding:utf-8-*-
from django.db import models
from .public import *

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_templet_amazon_published_variation.py
 @time: 2017/12/20 15:08
"""
class t_templet_amazon_published_variation(models.Model):
    publishedID         = models.PositiveSmallIntegerField(u'刊登商品ID',blank = True,null = True)
    relationship_type   = models.CharField(u'关系类型', max_length=32, blank=True, null=True)
    variation_theme     = models.CharField(u'变体分辨类型', max_length=32, choices=getChoices(AmazonVariationTheme), blank=True, null=True)
    parent_sku          = models.CharField(u'父店铺SKU', max_length=32, blank=True, null=True)
    child_sku           = models.CharField(u'子店铺SKU', max_length=32, blank=True, null=True)
    price               = models.DecimalField(u'变体价格', max_digits=10, decimal_places=2)
    main_image_url      = models.ImageField(u'主图', max_length=1000, blank=True, null=True)
    other_image_url1    = models.ImageField(u'附图1', max_length=1000, blank=True, null=True)
    other_image_url2    = models.ImageField(u'附图2', max_length=1000, blank=True, null=True)
    other_image_url3    = models.ImageField(u'附图3', max_length=1000, blank=True, null=True)
    other_image_url4    = models.ImageField(u'附图4', max_length=1000, blank=True, null=True)
    other_image_url5    = models.ImageField(u'附图5', max_length=1000, blank=True, null=True)
    other_image_url6    = models.ImageField(u'附图6', max_length=1000, blank=True, null=True)
    other_image_url7    = models.ImageField(u'附图7', max_length=1000, blank=True, null=True)
    other_image_url8    = models.ImageField(u'附图8', max_length=1000, blank=True, null=True)
    parent_item_sku     = models.CharField(u'父商品SKU', max_length=200, blank=True, null=True)
    productSKU          = models.CharField(u'商品SKU', max_length=200, blank=True, null=True)
    parent_child        = models.CharField(u'主从类型', max_length=64, blank=True, null=True)
    color_name          = models.CharField(u'颜色名称', max_length=32, blank=True, null=True)
    MetalType           = models.CharField(u'材质', max_length=32, blank=True, null=True)
    color_map           = models.CharField(u'颜色', max_length=32, choices=getChoices(ColorMap), blank=True, null=True)
    size_name           = models.CharField(u'尺寸名称', max_length=32, blank=True, null=True)
    size_map            = models.CharField(u'尺寸', max_length=32, choices=getChoices(SizeMap), blank=True, null=True)
    createUser          = models.CharField(u'创建人', max_length=32, blank=True, null=True)
    createTime          = models.DateTimeField(u'创建时间', blank=True, null=True)
    updateUser          = models.CharField(u'更新人', max_length=32, blank=True, null=True)
    updateTime          = models.DateTimeField(u'更新时间', blank=True, null=True)
    external_product_id = models.CharField(u'产品ID', max_length=64, blank=True, null=True)
    prodcut_variation_id= models.CharField(u'主从关系',max_length=32,blank=True,null=True)
    item_quantity       = models.CharField(u'包装数', max_length=12, default=u'1',blank=False, null=False)

    fit_type            = models.CharField(u'合身类型', max_length=32, blank=True, null=True)
    sleeve_type         = models.CharField(u'袖筒类型', max_length=32, blank=True, null=True)

    class Meta:
        verbose_name = u'Amazon待刊登商品变体信息'
        verbose_name_plural = verbose_name
        db_table = 't_templet_amazon_published_variation'
        ordering = ['-id']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)