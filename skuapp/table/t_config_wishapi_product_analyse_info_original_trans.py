# -*- coding: utf-8 -*-
"""
 @desc:
 @author: wangzhiyang
 @site:
 @software: PyCharm
 @file: t_config_wishapi_product_analyse_info_original_trans.py
 @time: 2018/6/15 8:53
"""
from django.db import models
#API指令执行计划完成表
class t_config_wishapi_product_analyse_info_original_trans(models.Model):
    id = models.AutoField(u'业务流水号', primary_key=True)
    product_id = models.CharField(u'产品ID', max_length=200, primary_key=True)
    Name = models.CharField(u'Title', max_length=1024, blank=True, null=True)
    mid = models.CharField(u'供应商id', max_length=255, blank=True, null=True)
    mname = models.CharField(u'供应商名称', max_length=255, blank=True, null=True)
    SourcePicPath = models.CharField(u'图片', max_length=255, blank=True, null=True)
    approved_date = models.DateTimeField(u'店铺开张时间', blank=True, null=True)
    is_promo = models.CharField(u'是否加钻促销', max_length=12, blank=True, null=True)
    is_verified = models.CharField(u'是否wish认证', max_length=12, blank=True, null=True)
    is_HWC = models.CharField(u'是否海外仓', max_length=12, blank=True, null=True)
    num_rating = models.PositiveSmallIntegerField(u'rating_num', max_length=11, blank=True, null=True)
    rating = models.DecimalField(u'ratings', max_digits=11, decimal_places=1, blank=True, null=True)
    o_price = models.DecimalField(u'商家定价', max_digits=11, decimal_places=1, blank=True, null=True)
    o_shipping = models.DecimalField(u'商家运费', max_digits=11, decimal_places=1, blank=True, null=True)
    shipping = models.DecimalField(u'运费', max_digits=11, decimal_places=1, blank=True, null=True)
    NumBought = models.PositiveSmallIntegerField(u'NumBought', max_length=11, blank=True, null=True)
    ShelveDay = models.DateField(u'上架时间', blank=True, null=True)
    UnitPrice = models.DecimalField(u'售价', max_digits=11, decimal_places=1, blank=True, null=True)
    OrdersLast7Days = models.PositiveSmallIntegerField(u'前1~7天销量', max_length=11, blank=True, null=True)
    OrdersLast7to14Days = models.PositiveSmallIntegerField(u'前8~14天销量', max_length=11, blank=True, null=True)
    totalprice = models.DecimalField(u'商品总价', max_digits=11, decimal_places=1, blank=True, null=True)
    dailybought = models.DecimalField(u'昨天的销售件数', max_digits=11, decimal_places=1, blank=True, null=True)
    SupplierID = models.CharField(u'是否有供应商', max_length=100, blank=True, null=True)
    c_ids = models.TextField(u'商品所属类目', blank=True, null=True)
    DealName = models.CharField(u'调研状态', max_length=100, blank=True, null=True)
    DealTime = models.DateTimeField(u'DealTime', blank=True, null=True)
    YNDone = models.CharField(u'YNDone', max_length=12, blank=True, null=True)
    Remarks = models.CharField(u'备注', max_length=255, blank=True, null=True)
    salesgrowth = models.DecimalField(u'销售增长率', max_digits=11, decimal_places=1, blank=True, null=True)
    Op_time = models.DateTimeField(u'抓取时间', max_length=20, blank=True, null=True)
    Collar = models.CharField(u'Collar', max_length=20, blank=True, null=True)
    getboughtinfo = models.CharField(u'取Boughtthis状态', max_length=64, blank=True, null=True)
    boughtthis = models.PositiveSmallIntegerField(u'Boughtthis', max_length=11, blank=True, null=True)
    op_flag = models.PositiveSmallIntegerField(u'操作标志', max_length=11, blank=True, null=True)
    boughtthis_flag = models.PositiveSmallIntegerField(u'boughtthis_flag', max_length=11, blank=True, null=True)
    delete_falg = models.PositiveSmallIntegerField(u'删除标志', max_length=11, blank=True, null=True)
    boughtthis_time = models.DateTimeField(u'购买时间', blank=True, null=True)
    viewdata = models.DecimalField(u'小火苗', max_digits=11, decimal_places=2, blank=True, null=True)
    class Meta:
        verbose_name=u'wish小火苗月榜单'
        verbose_name_plural=verbose_name
        db_table = 't_config_wishapi_product_analyse_info_original_trans'
        ordering =  ['-ShelveDay','-viewdata']
    def __unicode__(self):
        return u'id:%s'%(self.id)