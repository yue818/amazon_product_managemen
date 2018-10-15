#-*-coding:utf-8-*-
u"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_online_info_wish_fbw.py
 @time: 2018/9/7 9:00
"""
from django.db import models

class t_online_info_wish_fbw(models.Model):
    product_id     = models.CharField(u'产品ID', max_length=32, blank=True, null=True)
    shopsku        = models.CharField(u'店铺SKU', max_length=32, blank=True, null=True)
    warehouse_code = models.CharField(u'仓库代码', max_length=16, blank=True, null=True)
    online_stock = models.PositiveSmallIntegerField(u'在线库存', blank=True, null=True)
    demand_stock = models.PositiveSmallIntegerField(u'备货库存', blank=True, null=True)
    of_sales     = models.PositiveSmallIntegerField(u'销售数量', blank=True, null=True)
    deliver_stock= models.PositiveSmallIntegerField(u'销售数量', blank=True, null=True)

    class Meta:
        verbose_name=u'Wish(fbw)库存信息表'
        verbose_name_plural=verbose_name
        db_table = 't_online_info_wish_fbw'

    def __unicode__(self):
        return u'OrderDate:%s;OfSales:%s;warehouse_code:%s'%(self.product_id,self.shopsku,self.warehouse_code)







