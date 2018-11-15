# coding=utf-8


from django.db import models

class t_online_info_joom_shopSKU(models.Model):
    title       =   models.CharField(u'开头', max_length=10, blank=True, null=True)
    index       =   models.IntegerField(u'序号', blank=True, null=True)
    plateform   =   models.CharField(u'平台', max_length=20, blank=True, null=True)


    class Meta:
        verbose_name = u'JOOM全平台店铺SKU'
        verbose_name_plural = verbose_name
        db_table = 't_online_info_joom_shopSKU'

    def __unicode__(self):
        return u'id:%s'%(self.id)