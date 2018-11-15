# coding: utf-8
from django.db import models

ChoiceUpdateImageFlag = (
    (0, u'无更新'),
    (1, u'有更新')
)

class t_product_image_modify(models.Model):
    MainSKU             =   models.CharField(u'主SKU', max_length=32, blank=True, null=True)
    UpdateFlag          =   models.IntegerField(u'更新标志(WISH)', choices=ChoiceUpdateImageFlag, blank=True, null=True)
    UpdateFlagJoom      =   models.IntegerField(u'更新标志(JOOM)', choices=ChoiceUpdateImageFlag, blank=True, null=True)

    class Meta:
        verbose_name = u'主SKU对应图片修改'
        verbose_name_plural = verbose_name
        db_table = 't_product_image_modify'

    def __unicode__(self):
        return u'id:%s' % self.id
