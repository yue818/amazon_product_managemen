# coding=utf-8

from django.db import models

ChoicePostStatus = (
    ('UNSUBMITTED', u'未提交'),
    ('SUBMITTED', u'已提交')
)

ChoiceReviewStatus = (
    ('UNREVIEW', u'未审核'),
    ('PASS', u'审核通过'),
    ('FAILE', u'审核不通过')
)


class t_templet_wish_upload_review(models.Model):

    MainSKU         =   models.CharField(u'主SKU', max_length=255, blank=True, null=True)
    ParentSKU       =   models.CharField(u'父SKU', max_length=32, blank=True, null=True)
    Title           =   models.TextField(u'标题', blank=True, null=True)
    Description     =   models.TextField(u'描述', blank=True, null=True)
    Tags            =   models.TextField(u'标签', blank=True, null=True)
    MainImage       =   models.CharField(u'主图', max_length=200, blank=True, null=True)
    ExtraImages     =   models.TextField(u'副图', blank=True, null=True)
    Variants        =   models.TextField(u'变种JSON', blank=True, null=True)
    ShopName        =   models.CharField(u'铺货店铺', max_length=32, blank=True, null=True)
    Schedule        =   models.DateTimeField(u'预计铺货时间', blank=True, null=True)
    CoreWords       =   models.CharField(u'核心词', max_length=200, blank=True, null=True)
    CreateStaff     =   models.CharField(u'创建人', max_length=16, blank=True, null=True)
    CreateTime      =   models.DateTimeField(u'创建时间', blank=True, null=True)
    PostStatus      =   models.CharField(u'提交状态', max_length=32, blank=True, null=True)
    PostTime        =   models.DateTimeField(u'提交时间', blank=True, null=True)
    ReviewStaff     =   models.CharField(u'审核人', max_length=16, blank=True, null=True)
    ReviewTime      =   models.DateTimeField(u'审核时间', blank=True, null=True)
    ReviewStatus    =   models.CharField(u'审核状态', max_length=32, blank=True, null=True)
    PlateForm       =   models.CharField(u'来源平台', max_length=16, blank=True, null=True)
    Remarks         =   models.TextField(u'备注', blank=True, null=True)

    class Meta:
        verbose_name = u'WISH铺货审核'
        verbose_name_plural = verbose_name
        db_table = 't_templet_wish_upload_review'
        ordering = ['-id']

    def __unicode__(self):
        return u'%s' % (self.id)