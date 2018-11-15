# -*- coding: utf-8 -*-


from django.db import models

ChoiceIsAvailable = (
    (1, u'可铺货'),
    (0, u'不可铺货')
)


class t_upload_shopname(models.Model):
    ShopName = models.CharField(u'卖家简称', max_length=32, null=True)
    uploader = models.CharField(u'铺货人', max_length=32, null=True)
    LastOrderNumber = models.IntegerField(u'上周订单数', max_length=6, blank=True, null=True)
    LastSalesVolume = models.FloatField(u'上周销售额', blank=True, null=True)
    AllOrderNumber = models.TextField(u'历史订单数集合', blank=True, null=True)
    AllSalesVolume = models.TextField(u'历史销售额集合', blank=True, null=True)
    LastWeekStart = models.CharField(u'上次统计周开始日期（UTC）', max_length=16, blank=True, null=True)
    UpdateTime = models.DateTimeField(u'最近更新时间', blank=True, null=True)
    IsAvailable = models.IntegerField(u'是否可铺货', choices=ChoiceIsAvailable, null=True)

    class Meta:
        verbose_name = u'铺货店铺表'
        verbose_name_plural = verbose_name
        db_table = 't_upload_shopname'
        ordering = ['-id']

    def __unicode__(self):
        return u'id:%s' % (self.id)
