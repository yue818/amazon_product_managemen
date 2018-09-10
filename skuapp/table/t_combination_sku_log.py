#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_combination_sku_log.py
 @time: 2018-04-26 16:21
"""
from django.db import models
from django.utils.safestring import mark_safe


class t_combination_sku_log(models.Model):
    Pro_SKU       = models.TextField(u'商品SKU合集',  blank=True, null=True)
    Com_SKU       = models.CharField(u'组合SKU', max_length=32, blank=True, null=True)
    CreateTime    = models.DateTimeField(u'组合SKU创建时间', blank=True, null=True)
    CreateName    = models.CharField(u'组合SKU创建人', max_length=32, blank=True, null=True)
    CreateStaffID = models.CharField(u'组合SKU创建人ID', max_length=32, blank=True, null=True)
    SynStatus     = models.CharField(u'是否同步到普源', max_length=16, blank=True, null=True)
    ZHName        = models.CharField(u'组合商品的名称', max_length=256, blank=True, null=True)

    class Meta:
        verbose_name = u'组合商品对应关系表'
        verbose_name_plural = verbose_name
        db_table = 't_combination_sku_log'
        ordering = ['-id']

    def __unicode__(self):
        return u'%s Com_SKU=%s ' % (self.id, self.Com_SKU,)


