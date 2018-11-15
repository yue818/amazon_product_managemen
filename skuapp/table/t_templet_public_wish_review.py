# coding=utf-8

from django.db import models


class t_templet_public_wish_review(models.Model):

    MainSKU         =   models.CharField(u'主SKU', max_length=255, blank=True, null=True)
    Title           =   models.TextField(u'标题', blank=True, null=True)
    Description     =   models.TextField(u'描述', blank=True, null=True)
    Tags            =   models.TextField(u'标签', blank=True, null=True)
    MainImage       =   models.CharField(u'主图', max_length=200, blank=True, null=True)
    ExtraImages     =   models.TextField(u'副图', blank=True, null=True)
    Status          =   models.CharField(u'模板状态', max_length=32, blank=True, null=True)
    Variants        =   models.TextField(u'变种JSON', blank=True, null=True)
    CreateTime      =   models.DateTimeField(u'创建时间', blank=True, null=True)
    CreateStaff     =   models.CharField(u'创建人', max_length=16, blank=True, null=True)
    UpdateTime      =   models.DateTimeField(u'更新时间', blank=True, null=True)
    UpdateStaff     =   models.CharField(u'更新人', max_length=16, blank=True, null=True)
    CoreWords       =   models.CharField(u'核心词', max_length=200, blank=True, null=True)
    CoreTags        =   models.CharField(u'核心标签', max_length=200, blank=True, null=True)
    SrcProductID    =   models.CharField(u'来源', max_length=32, blank=True, null=True)
    ReviewState     =   models.IntegerField(u'审核状态', max_length=10, blank=True, null=True)
    SkuState        =   models.TextField(u'普源商品状态', blank=True, null=True)
    PlateForm       =   models.CharField(u'来源平台', max_length=16, blank=True, null=True)
    Remarks         =   models.TextField(u'备注', blank=True, null=True)
    ReviewTime      =   models.DateTimeField(u'审核时间', blank=True, null=True)
    ReviewStaff     =   models.CharField(u'审核人', max_length=16, blank=True, null=True)


    class Meta:
        verbose_name = u'WISH铺货模板审核'
        verbose_name_plural = verbose_name
        db_table = 't_templet_public_wish_review'
        ordering = ['-id']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)
