# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models
from public import getChoices,ChoicePZRemake
LQStateChoices = (
        (u'n', u'未领取'),
        (u'y', u'已领取'),
    )
SelectWaysChoices = (
        (u'y', u'精确查询'),
        (u'n', u'模糊查询'),
    )
#拍照取样
class t_product_saler_requirement_photograph(t_base):
    PZRemake = models.CharField(u'拍照类型', choices=getChoices(ChoicePZRemake), default=1, max_length=2, null=True)
    PZTimeing = models.DateTimeField(u'拍照申请时间', blank=True, null=True)
    PZStaffNameing = models.CharField(u'销售申请人', max_length=16, blank=True, null=True)
    SampleState = models.CharField(u'样品状态',default='未取样', max_length=16, blank=True, null=True)
    #SampleState = models.CharField(u'样品状态',choices=getChoices(ChoiceSampleState), max_length=16, blank=True, null=True)
    pid = models.IntegerField(u'业务流水号', null=True, db_index=True)
    ##销售员实拍需求比t_product_photograph新增
    LQTimeing = models.DateTimeField(u'领取时间', blank=True, null=True)
    LQStaffNameing = models.CharField(u'领取人', max_length=16, blank=True, null=True)
    LQState = models.CharField(u'领取状态', choices=LQStateChoices, default='n', max_length=16,blank=True, null=True)
    SelectWays = models.CharField(u'查询方式', choices=SelectWaysChoices, default='y', max_length=16, blank=True, null=True)
    class Meta:
        verbose_name = u'销售员实拍需求'
        verbose_name_plural = verbose_name
        db_table = 't_product_saler_requirement_photograph'
        ordering =  ['-PZTimeing']
    def __unicode__(self):
        return u'id:%s MainSKU:%s'%(self.id,self.MainSKU)