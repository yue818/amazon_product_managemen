# -*- coding: utf-8 -*-
from django.db import models
#库存预警信息
class t_store_plan_warning(models.Model):
    SKU            =   models.CharField(u'子SKU',max_length=16,db_index = True,blank = True,null = True)
    Name           =   models.CharField(u'品名',max_length=64,blank = True,null = True)
    NID            =   models.IntegerField(u'库存预警ID')
    StoreID        =   models.IntegerField(u'仓库NID',blank = True,null = True)
    GoodsID        =   models.IntegerField(u'商品NID',blank = True,null = True)
    GoodsSKUID     =   models.IntegerField(u'商品细表NID',blank = True,null = True)
    Number         =   models.DecimalField(u'库存数量',max_digits=18,decimal_places=4,null = True)
    Money          =   models.DecimalField(u'库存金额',max_digits=18,decimal_places=4,null = True)
    Price          =   models.DecimalField(u'平均单价',max_digits=18,decimal_places=4,null = True)
    ReservationNum =   models.DecimalField(u'占用数量',max_digits=18,decimal_places=4,null = True)
    OutCode        =   models.CharField(u'外部编码',max_length=50,blank = True,null = True)
    WarningCats    =   models.CharField(u'库存预警类别',max_length=50,blank = True,null = True)
    SaleDate       =   models.DateTimeField(u'SaleDate',blank = True,null = True)
    KcMaxNum       =   models.DecimalField(u'库存上限',max_digits=10,decimal_places=4,null = True)
    KcMinNum       =   models.DecimalField(u'库存下限',max_digits=10,decimal_places=4,null = True)
    SellCount1     =   models.IntegerField(u'5天销量',blank = True,null = True)
    SellCount2     =   models.IntegerField(u'15天销量',blank = True,null = True)
    SellCount3     =   models.IntegerField(u'30天销量',blank = True,null = True)
    SellDays       =   models.IntegerField(u'预警销售天数',blank = True,null = True)
    StockDays      =   models.IntegerField(u'采购到货天数',blank = True,null = True)
    SellCount      =   models.IntegerField(u'SellCount',blank = True,null = True)
    pid            =   models.IntegerField(u'计划ID',db_index = True,blank = True,null = True)
    StaffID        =  models.CharField(u'工号',max_length=16,blank = True,null = True)
    UpdateTime     =  models.DateTimeField(u'更新时间',auto_now=True,blank = True,null = True)
    class Meta:
        verbose_name=u'库存预警信息'
        verbose_name_plural=u'库存预警信息'
        db_table = 't_store_plan_warning'
        ordering =  ['SKU']
    def __unicode__(self):
        return u'%s %s %s %s'%(self.id,self.SKU,self.Name,self.pid)