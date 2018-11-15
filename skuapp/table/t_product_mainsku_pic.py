# coding=utf-8

from django.db import models


class t_product_mainsku_pic(models.Model):
    MainSKU         =   models.CharField(u'主SKU', max_length=32, blank=True, null=True)
    pic             =   models.CharField(u'图片地址', max_length=200, blank=True, null=True)
    WishPic         =   models.CharField(u'WISH图片地址', max_length=200, blank=True, null=True)
    HashStr         =   models.TextField(u'图片Hsah', blank=True, null=True)
    Flag            =   models.IntegerField(u'主图标识(WISH)', blank=True, null=True)
    NewFlag         =   models.IntegerField(u'新图标识(WISH)', blank=True, null=True)
    FlagJoom        =   models.IntegerField(u'主图标识(JOOM)', max_length=2, blank=True, null=True)
    NewFlagJoom     =   models.IntegerField(u'新图标识(JOOM)', max_length=2, blank=True, null=True)
    UpdateTime      =   models.DateTimeField(u'更新时间', blank=True, null=True)

    class Meta:
        verbose_name = u'主SKU-图片表'
        verbose_name_plural = verbose_name
        db_table = 't_product_mainsku_pic'

    def __unicode__(self):
        return u'id:%s' % self.id