# coding=utf-8


from django.db import models
# from skuapp.table.t_product_price_check import *


class t_product_price_check_recycle(models.Model):

    GoodsSKU = models.CharField(u'SKU', max_length=100, blank=True, null=True)
    GoodsCode = models.CharField(u'商品编码', max_length=32, blank=True, null=True)
    SQStaffName = models.CharField(u'申请人', max_length=30, blank=True, null=True)
    SQTime = models.DateTimeField(u'申请时间', blank=True, null=True)
    XGStaffName = models.CharField(u'修改人', max_length=30, blank=True, null=True)
    XGTime = models.DateTimeField(u'完成修改时间', blank=True, null=True)
    LQStaffName = models.CharField(u'领取人', max_length=30, blank=True, null=True)
    LQTime = models.DateTimeField(u'领取时间', blank=True, null=True)
    # 待修改DXG  在修改ZXG  驳回BH  完成修改WCXG
    Mstatus = models.CharField(u'修改状态', max_length=10, blank=True, null=True)
    OldPrice = models.DecimalField(u'原价', max_digits=6, decimal_places=2, blank=True, null=True)
    NowPrice = models.DecimalField(u'现价', max_digits=6, decimal_places=2, blank=True, null=True)
    OldSupplier = models.TextField(u'原供应商', max_length=64, blank=True, null=True)
    OldSupplierURL = models.TextField(u'原采购链接', blank=True, null=True)
    NewSupplier = models.TextField(u'新供应商', max_length=64, blank=True, null=True)
    NewSupplierURL = models.TextField(u'新采购链接', blank=True, null=True)
    remarks = models.CharField(u'销售备注', max_length=200, blank=True, null=True)
    XGcontext = models.TextField(u'备注', blank=True, null=True)
    remarks2 = models.CharField(u'修改备注', max_length=250, blank=True, null=True)
    RecycleTime = models.DateTimeField(u'回收时间', blank=True, null=True)
    RecycleStaffName = models.CharField(u'回收人', max_length=30, blank=True, null=True)

    class Meta:
        verbose_name = u'核价信息回收站'
        verbose_name_plural = verbose_name
        db_table = 't_product_price_check_recycle'

    def __unicode__(self):
        return u'id:%s'%(self.id)