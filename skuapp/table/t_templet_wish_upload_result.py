# coding=utf-8


from django.db import models

class t_templet_wish_upload_result(models.Model):

    MainSKU         =   models.CharField(u'主SKU', max_length=255, blank=True, null=True)
    Title           =   models.TextField(u'标题', blank=True, null=True)
    Description     =   models.TextField(u'描述', blank=True, null=True)
    Tags            =   models.TextField(u'标签', blank=True, null=True)
    MainImage       =   models.CharField(u'主图', max_length=200, blank=True, null=True)
    ExtraImages     =   models.TextField(u'副图', blank=True, null=True)
    Status          =   models.CharField(u'铺货状态', max_length=32, blank=True, null=True)
    Variants        =   models.TextField(u'变种JSON', blank=True, null=True)
    ShopName        =   models.CharField(u'目标店铺', max_length=32, blank=True, null=True)
    InsertTime      =   models.DateTimeField(u'发布时间', blank=True, null=True)
    Schedule        =   models.DateTimeField(u'时间表', blank=True, null=True)
    BeginTime       =   models.DateTimeField(u'开始时间', blank=True, null=True)
    EndTime         =   models.DateTimeField(u'结束时间', blank=True, null=True)
    ParentSKU       =   models.CharField(u'父SKU', max_length=32, blank=True, null=True)
    Submitter       =   models.CharField(u'发布人', max_length=32, blank=True, null=True)
    PID             =   models.IntegerField(u'发布ID', max_length=20, blank=True, null=True)
    ErrorMessage    =   models.TextField(u'错误信息', blank=True, null=True)

    class Meta:
        verbose_name = u'WISH铺货结果'
        verbose_name_plural = verbose_name
        db_table = 't_templet_wish_upload_result'
        ordering = ['-id']

    def __unicode__(self):
        return u'%s' % (self.id)