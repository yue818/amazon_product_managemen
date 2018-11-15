# coding=utf-8


from django.db import models


class t_product_corewords(models.Model):
    CoreWords = models.CharField(u'核心标题', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = u'核心标题'
        verbose_name_plural = verbose_name
        db_table = 't_product_corewords'

    def __unicode__(self):
        return u'id:%s' % self.id