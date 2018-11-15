# coding=utf-8


from t_base import *
from public import *
from django.db import models

class t_product_price_check(t_base):

    GoodsSKU        =   models.CharField(u'SKU',max_length=100,blank = True,null = True)
    GoodsCode       =   models.CharField(u'商品编码',max_length=32,blank = True,null = True)
    SQStaffName     =   models.CharField(u'申请人', max_length=30, blank=True, null=True)
    SQTime          =   models.DateTimeField(u'申请时间', blank=True, null=True)
    XGStaffName     =   models.CharField(u'修改人', max_length=30, blank=True, null=True)
    XGTime          =   models.DateTimeField(u'完成修改时间', blank=True, null=True)
    LQStaffName     =   models.CharField(u'领取人', max_length=30, blank=True, null=True)
    LQTime          =   models.DateTimeField(u'领取时间', blank=True, null=True)
    # 待修改DXG  在修改ZXG  驳回BH  完成修改WCXG
    Mstatus         =   models.CharField(u'修改状态', max_length=10, blank=True, null=True)
    OldPrice        =   models.DecimalField(u'原价', max_digits=6, decimal_places=2, blank=True, null=True)
    NowPrice        =   models.DecimalField(u'现价', max_digits=6, decimal_places=2, blank=True, null=True)
    OldSupplier     =   models.TextField(u'原供应商', max_length=64, blank=True, null=True)
    OldSupplierURL  =   models.TextField(u'原采购链接', blank=True, null=True)
    NewSupplier     =   models.TextField(u'新供应商', max_length=64, blank=True, null=True)
    NewSupplierURL  =   models.TextField(u'新采购链接', blank=True, null=True)
    remarks         =   models.CharField(u'销售备注', max_length=200,blank=True, null=True)
    XGcontext       =   models.TextField(u'备注(原链接加新链接)', blank=True, null=True)
    remarks2        =   models.CharField(u'修改备注', max_length=250, blank=True, null=True)
    OldWeight       =   models.CharField(u'原克重(g)',max_length=20,blank = True,null = True)
    NowWeight       =   models.CharField(u'现克重(g)',max_length=20,blank = True,null = True)
    PricePercent    =   models.CharField(u'百分比', max_length=8, blank=True, null=True)

    Dep1            =   models.CharField(u'一部领用人',max_length=32,blank=True,null = True)
    Dep1Date        =   models.DateField(u'一部领用日期',blank=True,null = True)
    Dep1Sta         =   models.CharField(u'一部领用状态',max_length=32,blank=True,null = True)
    Dep2            =   models.CharField(u'二部领用人',max_length=32,blank=True,null = True)
    Dep2Date        =   models.DateField(u'二部领用日期',blank=True,null = True)
    Dep2Sta         =   models.CharField(u'二部领用状态',max_length=32,blank=True,null = True)
    Dep3            =   models.CharField(u'三部领用人',max_length=32,blank=True,null = True)
    Dep3Date        =   models.DateField(u'三部领用日期',blank=True,null = True)
    Dep3Sta         =   models.CharField(u'三部领用状态',max_length=32,blank=True,null = True)
    Dep4            =   models.CharField(u'四部领用人',max_length=32,blank=True,null = True)
    Dep4Date        =   models.DateField(u'四部领用日期',blank=True,null = True)
    Dep4Sta         =   models.CharField(u'四部领用状态',max_length=32,blank=True,null = True)
    Dep5            =   models.CharField(u'五部领用人',max_length=32,blank=True,null = True)
    Dep5Date        =   models.DateField(u'五部领用日期',blank=True,null = True)
    Dep5Sta         =   models.CharField(u'五部领用状态',max_length=32,blank=True,null = True)
    HJcount         =   models.IntegerField(u'30天核价次数',blank=True,null=True)

    class Meta:
        verbose_name = u'核价信息显示'
        verbose_name_plural = verbose_name
        db_table = 't_product_price_check'

    def __unicode__(self):
        return u'id:%s'%(self.id)