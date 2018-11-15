# -*- coding: utf-8 -*-
from django.db import models
from public import *
#IP资产及IP资产使用情况(版权)
"""
1、状态（单选项）：已填报；已登记
2、证书类型和存放地(单选项）：纸质版，合肥人事；纸质版，财务
3、默认显示列：编码，sku，作品名称，作品类型，状态，登记号，证书存放地，领用平台，第一次提醒，第二次提醒，附件
"""
CopyrightSite1 = [(u'已填报',u'已填报'),(u'已受理',u'已受理'),(u'已登记',u'已登记'),(u'失败',u'失败')]
CopyrightSite2 = [(u'纸质版，财务',u'纸质版，财务'),(u'纸质版，合肥人事',u'纸质版，合肥人事'),(u'N/A',u'N/A'),(u'电子版',u'电子版')]
CopyrightSite3 = [(u'wish',u'wish'),(u'eBay',u'eBay'), (u'亚马逊',u'亚马逊'),(u'速卖通',u'速卖通'),(u'其他',u'其他')]

class t_copyright(models.Model):
    id                 =   models.AutoField(u'编码', primary_key=True, blank=False, null=False)
    Source             =   models.CharField(u'来源', max_length=16, blank=True, null=True)
    SKU                =   models.CharField(u'商品SKU', max_length=16, blank=True, null=True)
    WorkTitle          =   models.CharField(u'作品名称', max_length=50, blank=True, null=True)
    WorkClass          =   models.CharField(u'作品类型', max_length=16, blank=True, null=True)
    CopyrightArea      =   models.CharField(u'版权地域', max_length=32, blank=True, null=True)
    CopyrightOwner     =   models.CharField(u'著作权人', max_length=16, blank=True, null=True)
    CompletionDate     =   models.DateField(u'创作完成日期', blank=True, null=True)
    CommitDate         =   models.DateField(u'提交日期', blank=True, null=True)
    Status             =   models.CharField(u'状态', max_length=16, blank=True, null=True, choices=CopyrightSite1)
    RegistrationNo     =   models.CharField(u'登记号', max_length=50, blank=True, null=True)
    RegistrationDate   =   models.DateField(u'登记日期', blank=True, null=True)
    CertificateType    =   models.CharField(u'证书类型和存放地', max_length=50, blank=True, null=True, choices=CopyrightSite2)
    RecipientsPlatform =   models.CharField(u'领用平台', max_length=50, blank=True, null=True, choices=CopyrightSite3)
    RecipientsShop     =   models.CharField(u'领用店铺', max_length=50, blank=True, null=True)
    RecipientsPerson   =   models.CharField(u'领用人', max_length=16, blank=True, null=True)
    RecipientsTime     =   models.DateField(u'领用时间', blank=True, null=True)
    RecipientsPurpose  =   models.TextField(u'领用用途', blank=True, null=True)
    Inputer            =   models.CharField(u'操作人', max_length=16, blank=True, null=True)
    AttachmentUrl1     =   models.FileField(u'证书及作品样本', upload_to='media/', blank=True, null=True)
    AttachmentUrl2     =   models.FileField(u'盖章作品样本页', upload_to='media/', blank=True, null=True)
    RecipientsMsg      =   models.TextField(u'领用信息', blank=True, null=True)
    class Meta:
        verbose_name=u'版权'
        verbose_name_plural=u'版权'
        db_table = 't_copyright'
        ordering = ['-id']
    def __unicode__(self):
        return u'%s %s %s'%(self.id,self.SKU,self.WorkTitle)