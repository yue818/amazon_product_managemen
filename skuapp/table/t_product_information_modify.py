# -*- coding: utf-8 -*-
from t_base import t_base
from public import *
from django.db import models
from django.utils.safestring import mark_safe
class t_product_information_modify(t_base):
    InputBox                   =   models.TextField(u'输入框',blank = True,null = True)
    DevDate                    =   models.DateTimeField(u'开发时间',blank = True,null = True)
    SQTimeing                  =   models.DateField(u'申请时间',blank = True,null = True)
    SQStaffNameing             =   models.CharField(u'申请人',max_length=32,blank = True,null = True)
    XGTime                     =   models.DateField(u'修改时间',blank = True,null = True)
    XGStaffName                =   models.CharField(u'修改人',max_length=32,blank = True,null = True)
    SHTime                     =   models.DateField(u'审核时间',blank = True,null = True)
    SHStaffName                =   models.CharField(u'审核人',max_length=32,blank = True,null = True)
    LQTime                     =   models.DateField(u'领取时间',blank = True,null = True)
    LQStaffName                =   models.CharField(u'领取人',max_length=32,blank = True,null = True)
    Select                     =   models.CharField(u'修改类型',choices=getChoices(ChoiceSelectModifyFields),max_length=6,default='3',blank = True,null = True)
    XGcontext                  =   models.TextField(u'修改描述',blank = True,null = True)
    NowPrice                   =   models.DecimalField(u'现价', max_digits=6, decimal_places=2, blank=True, null=True)
    oldvalue                   =   models.CharField(u'旧值',max_length=64,blank = True,null = True)
    newvalue                   =   models.CharField(u'新值',max_length=64,blank = True,null = True)
    Mstatus                    =   models.CharField(u'修改状态',choices=getChoices(ChoiceState),max_length=6,blank = True,null = True)
    Source                     =   models.CharField(u'数据来源',max_length=32,blank = True,null = True)
    remarks                    =   models.CharField(u'销售备注',max_length=200,null = True)
    BHRemark                   =   models.CharField(u'驳回备注',max_length=255,null = True)
    Dep1                       =   models.CharField(u'一部领用人',max_length=32,null = True)
    Dep1Date                   =   models.DateField(u'一部领用日期',null = True)
    Dep1Sta                    =   models.CharField(u'一部领用状态',max_length=32,null = True)
    Dep2                       =   models.CharField(u'二部领用人',max_length=32,null = True)
    Dep2Date                   =   models.DateField(u'二部领用日期',null = True)
    Dep2Sta                    =   models.CharField(u'二部领用状态',max_length=32,null = True)
    Dep3                       =   models.CharField(u'三部领用人',max_length=32,null = True)
    Dep3Date                   =   models.DateField(u'三部领用日期',null = True)
    Dep3Sta                    =   models.CharField(u'三部领用状态',max_length=32,null = True)
    Dep4                       =   models.CharField(u'四部领用人',max_length=32,null = True)
    Dep4Date                   =   models.DateField(u'四部领用日期',null = True)
    Dep4Sta                    =   models.CharField(u'四部领用状态',max_length=32,null = True)
    Dep5                       =   models.CharField(u'五部领用人',max_length=32,null = True)
    Dep5Date                   =   models.DateField(u'五部领用日期',null = True)
    Dep5Sta                    =   models.CharField(u'五部领用状态',max_length=32,null = True)
    Details                    =   models.TextField(u'详情', blank=True, null=True)
    CostReduction              =   models.TextField(u'降价', blank=True, null=True)
    PackFlag                   =   models.IntegerField(u'是否修改包装', blank=True, null=True)

    class Meta:
        verbose_name=u'商品信息修改'
        verbose_name_plural=verbose_name
        db_table = 't_product_information_modify'
        #proxy = True
    def __unicode__(self):
        return u'id:%s'%(self.id)
