# -*- coding: utf-8 -*-
from django.db import models
from public import *
#IP资产及IP资产使用情况(商标)
"""
1、商标国别（单选项）：中国，美国，欧盟，英国
商标状态（单选项）：空白选项，注册，注册公告，pending，被驳回，等待受理
证书存放地（单选项）：纸质版，财务；纸质版，合肥人事，电子版
领用平台（多选项）：亚马逊，速卖通，eBay，wish
2、附件是受理通知书和商标证书
3、默认显示列：序号，品牌名称，商标国别，品类，商标状态，申请号，领用平台，第一次提醒，第二次提醒，第三次提醒，附件
"""
TrademarkSite1 = [(u'中国',u'中国'),(u'美国',u'美国'),(u'欧盟',u'欧盟'),(u'英国',u'英国')]
TrademarkSite2 = [(u'N/A',u'N/A'),(u'pending',u'pending'),(u'注册',u'注册'),(u'失败',u'失败')]
TrademarkSite3 = [(u'纸质版，财务',u'纸质版，财务'),(u'纸质版，合肥人事',u'纸质版，合肥人事'),(u'N/A',u'N/A'),(u'电子版',u'电子版')]
TrademarkSite4 = [(u'wish',u'wish'),(u'eBay',u'eBay'), (u'亚马逊',u'亚马逊'),(u'速卖通',u'速卖通'),(u'其他',u'其他')]

class t_trademark(models.Model):
    id                  =   models.AutoField(u'序号', primary_key=True, blank=False, null=False)
    BrandName           =   models.CharField(u'品牌名称', max_length=50, blank=True, null=True)
    TrademarkCountry    =   models.CharField(u'商标国别', max_length=16, blank=True, null=True, choices=TrademarkSite1)
    Register            =   models.CharField(u'注册人', max_length=50, blank=True, null=True)
    Category            =   models.CharField(u'品类', max_length=16,  blank=True, null=True)
    SecondaryGroup      =   models.TextField(u'二级组', blank=True, null=True)
    TrademarkStatus     =   models.CharField(u'商标状态', max_length=16, blank=True, null=True, choices=TrademarkSite2)
    CertificateID       =   models.CharField(u'证书号', max_length=32, blank=True, null=True)
    ApplicationID       =   models.CharField(u'申请号', max_length=32, blank=True, null=True)
    CertificateType     =   models.CharField(u'证书类型和存放地', max_length=50, blank=True, null=True, choices=TrademarkSite3)
    ApplicationDate     =   models.DateField(u'申请日期', blank=True, null=True)
    Remark              =   models.CharField(u'备注', max_length=500, blank=True, null=True)
    RecipientsPlatform  =   models.CharField(u'领用平台', max_length=50, blank=True, null=True, choices=TrademarkSite4)
    RecipientsShop      =   models.CharField(u'领用店铺', max_length=50, blank=True, null=True)
    RecipientsPerson    =   models.CharField(u'领用人', max_length=16, blank=True, null=True)
    RecipientsTime      =   models.DateField(u'领用时间', blank=True, null=True)
    RecipientsPurpose   =   models.TextField(u'领用用途', blank=True, null=True)
    AttachmentUrl1      =   models.FileField(u'受理通知书', upload_to='media/', blank=True, null=True)
    AttachmentUrl2      =   models.FileField(u'注册证书', upload_to='media/', blank=True, null=True)
    Agency              =   models.CharField(u'代理公司', max_length=50, blank=True, null=True)
    RecipientsMsg      =   models.TextField(u'领用信息', blank=True, null=True)
    class Meta:
        verbose_name=u'商标'
        verbose_name_plural=u'商标'
        db_table = 't_trademark'
        ordering =  ['-id']
    def __unicode__(self):
        return u'%s %s %s'%(self.id,self.BrandName,self.TrademarkCountry)