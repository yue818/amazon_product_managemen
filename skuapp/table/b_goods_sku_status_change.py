# coding=utf-8


from django.db import models


class b_goods_sku_status_change(models.Model):
    SKU                 =   models.CharField(u'SKU', max_length=128, blank=True, null=True)
    LastGoodsStatus     =   models.CharField(u'上次商品状态', max_length=32, blank=True, null=True)
    NowGoodsStatus      =   models.CharField(u'当前商品状态', max_length=32, blank=True, null=True)
    ChangeStatusTime    =   models.DateTimeField(u'状态改变时间', blank=True, null=True)
    DisplayFlag         =   models.IntegerField(u'显示标识', max_length=2, blank=True, null=True)
    OperationFlag       =   models.IntegerField(u'操作标识', max_length=2, blank=True, null=True)
    LastOperator        =   models.CharField(u'最后操作人', max_length=64, blank=True, null=True)
    LastOperateTime     =   models.DateTimeField(u'最后操作时间', blank=True, null=True)
    UpdateTime          =   models.DateTimeField(u'同步刷新时间', blank=True, null=True)

    class Meta:
        verbose_name = u'商品状态变更表'
        verbose_name_plural = verbose_name
        db_table = 'b_goods_sku_status_change'
        ordering = ['-id']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)