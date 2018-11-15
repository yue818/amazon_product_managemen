# -*- coding: utf-8 -*-
from django.db import models
from public import *
#IP资产及IP资产使用情况(专利)
"""
来源：自有，供应商			
专利类型：外观设计，发明专利，实用新型			
状态：N/A，受理，授权，失败	
"""
PatentSite1 = [(u'自有', u'自有'), (u'供应商', u'供应商')]
PatentSite2 = [(u'外观设计', u'外观设计'), (u'发明专利',u'发明专利'), (u'实用新型' , u'实用新型')]
PatentSite3 = [(u'N/A',u'N/A'),(u'受理',u'受理'),(u'授权',u'授权'),(u'失败',u'失败')]
PatentSite4 = [(u'纸质版，财务',u'纸质版，财务'),(u'纸质版，合肥人事',u'纸质版，合肥人事'), (u'N/A',u'N/A'),(u'电子版',u'电子版')]
PatentSite5 = [(u'wish',u'wish'),(u'eBay',u'eBay'), (u'亚马逊',u'亚马逊'),(u'速卖通',u'速卖通'),(u'其他',u'其他')]

class t_patents(models.Model):
    id                 =   models.AutoField(u'编码', primary_key=True, blank=False, null=False)
    Source             =   models.CharField(u'来源', max_length=16, blank=True, null=True, choices=PatentSite1)
    SKU                =   models.CharField(u'商品SKU', max_length=16, blank=True, null=True)
    PatentTitle        =   models.CharField(u'专利名称', max_length=50, blank=True, null=True)
    PatentClass        =   models.CharField(u'专利类型', max_length=16, blank=True, null=True, choices=PatentSite2)
    PatentArea         =   models.CharField(u'专利地域', max_length=32, blank=True, null=True)
    PatentOwner        =   models.CharField(u'专利权人', max_length=16, blank=True, null=True)
    Status             =   models.CharField(u'状态', max_length=16, blank=True, null=True, choices=PatentSite3)
    ApplicationDate    =   models.DateField(u'申请日期', blank=True, null=True)
    OpenDate           =   models.DateField(u'公开日期', blank=True, null=True)
    ApplicationNo      =   models.CharField(u'申请号', max_length=32, blank=True, null=True)
    OpenNo             =   models.CharField(u'公开号', max_length=32, blank=True, null=True)
    PatentType         =   models.CharField(u'证书类型和存放地', max_length=50, blank=True, null=True, choices=PatentSite4)
    RecipientsPlatform =   models.CharField(u'领用平台', max_length=50, blank=True, null=True, choices=PatentSite5)
    RecipientsShop     =   models.CharField(u'领用店铺', max_length=50, blank=True, null=True)
    RecipientsPerson   =   models.CharField(u'领用人', max_length=16, blank=True, null=True)
    RecipientsTime     =   models.DateField(u'领用时间', blank=True, null=True)
    RecipientsPurpose  =   models.TextField(u'领用用途', blank=True, null=True)
    AttachmentUrl1     =   models.FileField(u'专利请求书', upload_to='media/', blank=True, null=True)
    AttachmentUrl2     =   models.FileField(u'受理通知书', upload_to='media/', blank=True, null=True)
    AttachmentUrl3     =   models.FileField(u'授权通知书', upload_to='media/', blank=True, null=True)
    RecipientsMsg      =   models.TextField(u'领用信息', blank=True, null=True)
    class Meta:
        verbose_name=u'专利'
        verbose_name_plural=u'专利'
        db_table = 't_patents'
        ordering = ['-id']
    def __unicode__(self):
        return u'%s %s %s'%(self.id,self.SKU,self.PatentTitle)