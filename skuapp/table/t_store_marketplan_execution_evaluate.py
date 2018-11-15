# -*- coding: utf-8 -*-
from django.db import models
from public import *
#from skuapp.table.t_store_marketplan_execution_log import *
 
evaluate_choices = (
            ('yes',u'已留评'),
            ('no',u'未留评'),
    )

class t_store_marketplan_execution_evaluate(models.Model):
    BuyerAccount                 =   models.CharField(u'买家账号',max_length=32,blank = True,null = True)
    ProductID                    =   models.CharField(u'产品ID',max_length=32,blank = True,null = True)
    Status                       =   models.CharField(u'状态',max_length=10,blank = True,null = True)
    Exetime                      =   models.DateTimeField(u'执行时间',auto_now_add=True,blank = True,null = True)
    ShopName                     =   models.CharField(u'卖家简称',max_length=32,blank = True,null = True) 
    ShopSKU                      =   models.CharField(u'店铺SKU',max_length=32,blank = True,null = True)
    SKU                          =   models.CharField(u'商品SKU',max_length=32,blank = True,null = True)
    StaffId                      =   models.CharField(u'员工ID',max_length=32,blank = True,null = True)
    Price                        =   models.DecimalField(u'商品价格',max_digits=6,decimal_places=2,blank=False,null=False)
    Price2                       =   models.DecimalField(u'实际刷单金额',max_digits=6,decimal_places=2,blank=False,null=False)
    Result                       =   models.CharField(u'执行结果',choices=getChoices(ChoiceResult),max_length=32)
    Remark                       =   models.CharField(u'备注',blank = True,null = True,max_length=32)
    PicURL                       =   models.CharField(u'图片地址',max_length=32,blank = True,null = True)
    Pid                          =   models.IntegerField(u'Pid',blank = True,null = True)
    Product_evaluate             =   models.CharField(u'是否留评',max_length=11,choices=evaluate_choices,blank=True,null=True)

    class Meta:
        verbose_name=u'7天待留评产品表'
        verbose_name_plural=verbose_name
        db_table = 't_store_marketplan_execution_evaluate'

    def __unicode__(self):
        return u'%s'%(self.id)