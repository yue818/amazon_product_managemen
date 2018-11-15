#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_sku_weight_examine.py
 @time: 2018/7/11 15:17
"""


from django.db import models
from public import getChoices, Choice_examine_status


class t_sku_weight_examine(models.Model):
    product_lcate       =   models.CharField(u'大类名称',max_length=64,blank = True,null = True)
    product_scate       =   models.CharField(u'小类代码',max_length=32,blank = True,null = True)
    product_image       =   models.CharField(u'商品图片',max_length=255,blank = True,null = True)
    product_name        =   models.CharField(u'商品名称',max_length=255,blank = True,null = True)
    product_mainsku     =   models.CharField(u'检索SKU',max_length=32,blank = True,null = True)
    product_sku         =   models.CharField(u'商品SKU',max_length=32,blank = True,null = True)
    product_price       =   models.DecimalField(u'商品价格', max_digits=6, decimal_places=2, blank=True, null=True)
    create_person       =   models.CharField(u'审核申请人',max_length=16,blank = True,null = True)
    create_time         =   models.DateTimeField(u'审核申请时间', blank=True, null=True)
    survey_weight       =   models.PositiveSmallIntegerField(u'调研克重(g)',blank = True,null = True)
    packinfo_weight     =   models.PositiveSmallIntegerField(u'包装克重(g)',blank = True,null = True)
    examine_weight      =   models.PositiveSmallIntegerField(u'真实克重(g)',blank = True,null = True)
    examine_status      =   models.CharField(u'审核状态',choices = getChoices(Choice_examine_status),max_length=1,blank = True,null = True)
    auditor             =   models.CharField(u'审核人',max_length=16,blank = True,null = True)
    examine_time        =   models.DateTimeField(u'审核时间',blank = True,null = True)
    supplier_name       =   models.CharField(u'供应商名称', max_length=255, blank=True, null=True)
    canuse_num          =   models.PositiveSmallIntegerField(u'可用数量', blank=True, null=True)

    class Meta:
        verbose_name=u'精准调研克重审核'
        verbose_name_plural=verbose_name
        db_table = 't_sku_weight_examine'

    def __unicode__(self):
        return u'%s'%(self.id)