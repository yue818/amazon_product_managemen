# coding=utf-8

from django.db import models

class t_templet_wish_wait_upload(models.Model):
    """WISH待铺货表"""
    MainSKU         =   models.CharField(u'主SKU', max_length=255, blank=True, null=True)
    Title           =   models.TextField(u'标题', blank=True, null=True)
    Description     =   models.TextField(u'描述', blank=True, null=True)
    Tags            =   models.TextField(u'标签', blank=True, null=True)
    MainImage       =   models.CharField(u'主图', max_length=200, blank=True, null=True)
    ExtraImages     =   models.TextField(u'副图', blank=True, null=True)
    Status          =   models.CharField(u'模板状态', max_length=32, blank=True, null=True)
    Variants        =   models.TextField(u'变种JSON', blank=True, null=True)
    ShopSets        =   models.TextField(u'待铺货店铺', blank=True, null=True)
    TimePlan        =   models.TextField(u'时间计划JSON', blank=True, null=True)
    PostTime        =   models.DateTimeField(u'提交时间', blank=True, null=True)
    CreateTime      =   models.DateTimeField(u'创建时间', blank=True, null=True)
    CreateStaff     =   models.CharField(u'创建人', max_length=16, blank=True, null=True)
    UpdateTime      =   models.DateTimeField(u'更新时间', blank=True, null=True)
    UpdateStaff     =   models.CharField(u'更新人', max_length=16, blank=True, null=True)
    CoreWords       =   models.CharField(u'核心词', max_length=200, blank=True, null=True)
    CoreTags        =   models.CharField(u'核心标签', max_length=200, blank=True, null=True)
    SrcProductID    =   models.CharField(u'来源', max_length=32, blank=True, null=True)
    PlateForm       =   models.CharField(u'来源平台', max_length=16, blank=True, null=True)
    PostStaff       =   models.CharField(u'提交人', max_length=16, blank=True, null=True)


    class Meta:
        verbose_name = u'WISH定时铺货'
        verbose_name_plural = verbose_name
        db_table = 't_templet_wish_wait_upload'
        ordering = ['-id']

    def __unicode__(self):
        return u'%s' % (self.id)



