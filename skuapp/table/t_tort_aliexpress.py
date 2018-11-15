# -*- coding: utf-8 -*-
from django.db import models
from public import *
#平台侵权统计-速卖通
"""
SKU，商品名称，商品图片，登记时间，登记人，所在账号。备注
一、alirexpres 段xiaodi
投诉单号，备注，投诉受理日期
我方： 账号，账号所有人（同登记人），登记时间（发现侵权的时间），SKU，产品图片，输入图片URL，扣分情况 ，产品标题
对方： 投诉人，知识产权类型（外观专利，商标权，平台抽检，审核不通过），产品商标，投诉理由，附件URL5-10，对方联系方式
amazon:孙诗   ebay：任育苗  wish：刘华详
"""
class t_tort_aliexpress(models.Model):
    id             =   models.AutoField(u'侵权流水号',primary_key=True)
    Account        =   models.CharField(u'账号',max_length=32,blank = True,null = True)
    StaffID        =   models.CharField(u'工号',max_length=32,blank = True,null = True)
    AccountStaffID =   models.CharField(u'账号所有人',max_length=32,blank = True,null = True)
    UpdateTime     =   models.DateTimeField(u'登记时间',auto_now=True,blank = True,null = True)
    SKU            =   models.CharField(u'SKU',max_length=16,blank = True,null = True)
    ProductID      =   models.CharField(u'ProductID',max_length=32,blank = True,null = True)
    ProductPicUrl  =   models.ImageField(u'产品图片',upload_to='media/',blank=True, null=True)
    ListingTitle   =   models.CharField(u'listing标题',max_length=128,blank = True,null = True)
    ScoreDeducting =   models.CharField(u'扣分情况',max_length=32,blank = True,null = True)
    ProductTitle   =   models.CharField(u'产品名称(中文)',max_length=128,blank = True,null = True)
    Complainant    =   models.CharField(u'投诉人',max_length=32,blank = True,null = True)
    Intellectual   =   models.CharField(u'知识产权类型',choices=getChoices(ChoiceIntellectual),max_length=64,null = True)
    Trademark      =   models.CharField(u'产品商标',max_length=32,blank = True,null = True)
    ComplainReason =   models.CharField(u'投诉理由',max_length=64,blank = True,null = True)
    IntellectualCode =   models.CharField(u'知识产权编号',max_length=32,blank = True,null = True)
    Remark         =   models.TextField(u'备注',blank = True,null = True)
    Describe       =   models.TextField(u'侵权分析措施描述',blank = True,null = True)
    EmailTest      =   models.TextField(u'emai内容',blank = True,null = True)
    Site           =   models.CharField(u'侵权站点',max_length=64,blank = True,null = True,choices=getChoices(ChoiceSite))
    AttachmentUrl1 =   models.FileField(u'附件一',upload_to='media/',blank = True,null = True)
    AttachmentUrl2 =   models.FileField(u'附件二',upload_to='media/',blank = True,null = True)
    AttachmentUrl3 =   models.FileField(u'附件三',upload_to='media/',blank = True,null = True)
    AttachmentUrl4 =   models.FileField(u'附件四',upload_to='media/',blank = True,null = True)
    AttachmentUrl5 =   models.FileField(u'附件五',upload_to='media/',blank = True,null = True)
    AttachmentUrl6 =   models.FileField(u'附件六',upload_to='media/',blank = True,null = True)
    ContactWay     =   models.TextField(u'对方联系方式',blank = True,null = True)
    ComplainID     =   models.CharField(u'投诉单号',max_length=32,blank = True,null = True)
    AcceptTime     =   models.DateField(u'投诉受理时间',blank = True,null = True)
    DealStaffID    =   models.CharField(u'操作人员',max_length=32,blank=True,null=True)
    DealStatus     =   models.CharField(u'处理状态',choices=getChoices(ChoiceTortDealstatus),max_length=32,blank=True,null=True)
    DealTime       =   models.CharField(u'处理时间',max_length=32,blank=True,null=True)
    MainSKU        =   models.CharField(u'主SKU',max_length=16,blank=True,null=True)
    SalerName2          =   models.CharField(u'业绩归属人2',max_length=16,blank = True,null = True)
    Purchaser           =   models.CharField(u'采购员',max_length=16,blank = True,null = True)
    OperationState =   models.CharField(u'操作状态',choices=getChoices(ChoiceExportState),max_length=16,blank=True,null=True)
    class Meta:
        verbose_name=u'侵权统计'
        verbose_name_plural=u'侵权统计'
        db_table = 't_tort_aliexpress'
        ordering =  ['-id']
    def __unicode__(self):
        return u'%s %s %s'%(self.id,self.Account,self.StaffID)