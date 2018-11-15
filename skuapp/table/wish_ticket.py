# encoding: utf-8
'''
@author: zhangyu
@contact: 292724306@qq.com
@software: pycharm
@file: wish_ticket.py
@time: 2018-06-11 13:29
'''
from django.db import models


class wish_ticket(models.Model):
    id = models.IntegerField(primary_key=True)
    shopName = models.CharField(u'店铺名称', max_length=255, blank=True, null=True)
    updateTime = models.DateTimeField(u'同步时间', auto_now=True, blank=True, null=True)
    Operators = models.CharField(u'运营', max_length=50, blank=True, null=True)
    label = models.CharField(u'标签', max_length=255, blank=True, null=True)
    sublabel = models.CharField(max_length=255, blank=True, null=True)
    open_date = models.CharField(u'创建时间', max_length=255, blank=True, null=True)
    state = models.CharField(u'状态', max_length=255, blank=True, null=True)
    UserInfo_locale = models.CharField(max_length=255, blank=True, null=True)
    UserInfo_joined_date = models.CharField(max_length=255, blank=True, null=True)
    UserInfo_id = models.CharField(max_length=255, blank=True, null=True)
    UserInfo_name = models.CharField(max_length=255, blank=True, null=True)
    last_update_date = models.CharField(u'最新回复时间', max_length=255, blank=True, null=True)
    state_id = models.CharField(max_length=255, blank=True, null=True)
    default_refund_reason = models.CharField(max_length=255, blank=True, null=True)
    merchant_id = models.CharField(max_length=255, blank=True, null=True)
    photo_proof = models.CharField(max_length=255, blank=True, null=True)
    ticket_id = models.CharField(max_length=255, blank=True, null=True)
    ticket_transaction_id = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(u'标题', max_length=255, blank=True, null=True)
    product_id = models.CharField(u'产品ID',max_length=255, blank=True, null=True)
    order_id = models.CharField(u'订单ID',max_length=255, blank=True, null=True)
    product_name = models.CharField(u'商品名称', max_length=255, blank=True, null=True)
    product_image_url = models.CharField(u'商品图片', max_length=255, blank=True, null=True)
    replies = models.TextField(u'回复', max_length=25500, blank=True, null=True)
    class Meta:
        verbose_name = u'Wish Tickets'
        verbose_name_plural = verbose_name
        db_table = 'wish_ticket'
        ordering = ['id']
