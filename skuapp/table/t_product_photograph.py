# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models
from public import getChoices,ChoicePZRemake,ChoiceSampleState
#拍照取样
class t_product_photograph(t_base):
    SalesApplicant=models.CharField(u'销售申请人', max_length=16, blank=True, null=True)
    Entertime=models.DateTimeField(u'进入本步骤时间',blank=True, null=True)
    PZRemake = models.CharField(u'拍照类型', choices=getChoices(ChoicePZRemake), max_length=2, null=True)
    PZTimeing = models.DateTimeField(u'拍照申请时间', blank=True, null=True)
    PZStaffNameing = models.CharField(u'拍照申请人', max_length=16, blank=True, null=True)
    SampleState = models.CharField(u'样品状态',choices=getChoices(ChoiceSampleState),default='notyet', max_length=16, blank=True, null=True)
    #SampleState = models.CharField(u'样品状态',choices=getChoices(ChoiceSampleState), max_length=16, blank=True, null=True)
    pid = models.IntegerField(u'业务流水号', null=True, db_index=True)
    class Meta:
        verbose_name = u'拍照取样'
        verbose_name_plural = verbose_name
        db_table = 't_product_photograph'
        ordering =  ['-id']
    def __unicode__(self):
        return u'id:%s MainSKU:%s'%(self.id,self.MainSKU)