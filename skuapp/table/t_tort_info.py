#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_tort_info.py
 @time: 2018-05-05 9:26
"""
from django.db import models
from public import *

class t_tort_info(models.Model):
    ID             = models.AutoField(u'侵权流水号', primary_key=True)
    Account        = models.CharField(u'店铺账号', max_length=32, blank=True, null=True)
    AccountStaffID = models.CharField(u'账号所有人', max_length=255, blank=True, null=True)
    StaffID        = models.CharField(u'申请人', max_length=32, blank=True, null=True)
    UpdateTime     = models.DateTimeField(u'申请时间', auto_now_add=True, blank=True, null=True)

    Site           = models.CharField(u'侵权站点', max_length=64, choices=getChoices(ChoiceSite))
    MainSKU        = models.CharField(u'主SKU', max_length=32)
    ProductPicUrl  = models.ImageField(u'产品图片', upload_to='media/', blank=True, null=True)
    ProductTitle   = models.CharField(u'产品名称(中文)', max_length=128, blank=True, null=True)
    ProductID      = models.CharField(u'产品ID', max_length=32, blank=True, null=True)
    ScoreDeducting = models.CharField(u'扣分情况', max_length=32, blank=True, null=True)

    Complainant    = models.CharField(u'投诉人', max_length=32, blank=True, null=True)
    Intellectual   = models.CharField(u'侵权类型', choices=getChoices(ChoiceTortLevel), max_length=64)
    IntellectualCode = models.CharField(u'知识产权编号', max_length=32, blank=True, null=True)
    Trademark      = models.CharField(u'产品商标', max_length=32, blank=True, null=True)
    ComplainReason = models.CharField(u'投诉理由', max_length=255, blank=True, null=True)
    Remark         = models.TextField(u'备注', blank=True, null=True)
    ListingTitle   = models.CharField(u'Listing标题', max_length=128, blank=True, null=True)

    ContactWay     = models.TextField(u'联系方式', blank=True, null=True)
    ComplainID     = models.CharField(u'投诉单号', max_length=32, blank=True, null=True)
    EmailText      = models.TextField(u'邮件内容', blank=True, null=True)
    AcceptTime     = models.DateField(u'投诉受理时间', blank=False, null=True)

    SalerName2     = models.CharField(u'业绩归属人2', max_length=32, blank=True, null=True)
    Purchaser      = models.CharField(u'采购员', max_length=32, blank=True, null=True)

    AttachmentUrl1 = models.FileField(u'附件一', upload_to='media/', blank=False, null=True)
    AttachmentUrl2 = models.FileField(u'附件二', upload_to='media/', blank=True, null=True)
    AttachmentUrl3 = models.FileField(u'附件三', upload_to='media/', blank=True, null=True)
    AttachmentUrl4 = models.FileField(u'附件四', upload_to='media/', blank=True, null=True)
    AttachmentUrl5 = models.FileField(u'附件五', upload_to='media/', blank=True, null=True)
    AttachmentUrl6 = models.FileField(u'附件六', upload_to='media/', blank=True, null=True)

    IPRange        = models.CharField(u'IP范围', max_length=255, blank=True, null=True)
    IPForbiddenSite= models.CharField(u'IP禁用平台', max_length=255, blank=True, null=True)
    SourceUrl      = models.TextField(u'源头网站', blank=True, null=True)

    Step           = models.SmallIntegerField(u'操作步骤')

    Suggestion     = models.TextField(u'侵权处理意见', blank=True, null=True)
    AttacheID      = models.CharField(u'知识产权专员', max_length=32, blank=True, null=True)
    DealTime1      = models.DateTimeField(u'审核时间', blank=True, null=True)

    ReceiveDetail  = models.CharField(u'领用详细信息', max_length=500, blank=True, null=True)

    SyncStaffID    = models.CharField(u'同步信息人', max_length=32, blank=True, null=True)
    SyncTime       = models.DateTimeField(u'同步信息时间', blank=True, null=True)

    CancelReason   = models.CharField(u'侵权撤消原因', max_length=255, blank=True, null=True)
    CancelStaffID  = models.CharField(u'侵权撤消人', max_length=32, blank=True, null=True)
    CancelTime     = models.DateTimeField(u'侵权撤消时间', blank=True, null=True)

    OperationState = models.CharField(u'侵权处理结果', max_length=10, blank=True, null=True)
    EnglishName    = models.CharField(u'英文申报名', max_length=200, blank=True, null=True)
    KeyWord  =  models.CharField(u'侵权词', max_length=200, blank=True, null=True)
    WordCategory  =  models.CharField(u'尼斯分类', max_length=200, blank=True, null=True)
    
    class Meta:
        verbose_name = u'侵权申请'
        verbose_name_plural = u'侵权申请'
        db_table = 't_tort_info'
        ordering = ['-ID']
        
    def __unicode__(self):
        return u'%s %s %s' % (self.ID, self.Site, self.MainSKU )

