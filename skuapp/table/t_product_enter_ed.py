# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models
#11)    录入完成 t_product_enter_ed
class t_product_enter_ed(t_base):
    onebuOperation = models.CharField(u'1部领用',max_length=10,default=0,null = True)
    twobuOperation = models.CharField(u'2部领用', max_length=10, default=0, null=True)
    threebuOperation = models.CharField(u'3部领用', max_length=10,default=0, null=True)
    fourbuOperation = models.CharField(u'4部领用', max_length=10, default=0, null=True)
    fivebuOperation = models.CharField(u'5部领用', max_length=10, default=0, null=True)
    sixbuOperation = models.CharField(u'6部领用', max_length=10, default=0, null=True)
    sevenbuOperation = models.CharField(u'7部领用', max_length=10, default=0, null=True)
    eightbuOperation = models.CharField(u'8部领用', max_length=10, default=0, null=True)
    ninebuOperation = models.CharField(u'9部领用', max_length=10, default=0, null=True)
    tenbuOperation = models.CharField(u'10部领用', max_length=10, default=0, null=True)
    elevenbuOperation = models.CharField(u'11部领用', max_length=10, default=0, null=True)
    twelvebuOperation = models.CharField(u'12部领用', max_length=10, default=0, null=True)
    thirteenbuOperation = models.CharField(u'13部领用', max_length=10, default=0, null=True)
    Wish_count = models.IntegerField(u'刊登次数', blank=True, null=True)
    Amazon_count = models.IntegerField(u'刊登次数', blank=True, null=True)
    eBay_count = models.IntegerField(u'刊登次数', blank=True, null=True)
    class Meta:
        verbose_name=u'录入完成及部门领用'
        verbose_name_plural=u' 步骤11--录入完成及刊登信息'
        db_table = 't_product_enter_ed'
        ordering =  ['-id']
    def __unicode__(self):
        return u'id:%s MainSKU:%s'%(self.id,self.MainSKU)