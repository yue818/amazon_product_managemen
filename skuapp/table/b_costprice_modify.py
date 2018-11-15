# -*- coding: utf-8 -*-

from django.db import models

class b_costprice_modify(models.Model):
    NID          =   models.AutoField(u'NID',primary_key=True)
    SKU          =   models.CharField(u'商品SKU',max_length=32,blank=True,null=False)
    oriPrice     =   models.DecimalField(u'修改前价格',max_digits=8,decimal_places=2,blank=True,null=True)
    curPrice     =   models.DecimalField(u'修改后的价格',max_digits=8,decimal_places=2,blank=True,null=True)
    applyMan     =   models.CharField(u'申请人',max_length=64,blank=True,null=True)
    supplierID   =   models.CharField(u'供应商ID',max_length=128,blank=True,null=True)
    modifyTime   =   models.DateTimeField(u'修改时间',blank=True,null=True)
    modifyMan    =   models.CharField(u'修改人',max_length=64,blank=True,null=True)
    remark       =   models.TextField(u'备注',blank=True,null=True)

    class Meta:
        verbose_name = u'价格变动'
        verbose_name_plural = verbose_name
        db_table = 'b_costprice_modify'
        ordering = ['-NID']

    def __unicode__(self):
        return u'%s' % (self.id)