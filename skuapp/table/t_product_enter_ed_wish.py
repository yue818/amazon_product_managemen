# -*- coding: utf-8 -*-
# from t_base import t_base
from skuapp.table.t_base import t_base
from django.db import models

Aliexpress_PL_choice = (
    ('电脑网络&办公文教',u'电脑网络&办公文教'),
    ('服装服饰',u'服装服饰'),
    ('珠宝饰品及配件',u'珠宝饰品及配件'),
    ('箱包鞋类',u'箱包鞋类'),
    ('家居&家具',u'家居&家具'),
    ('家装&灯具&工具',u'家装&灯具&工具'),
    ('安防',u'安防'),
    ('美容健康',u'美容健康'),
    ('母婴&玩具',u'母婴&玩具'),
    ('汽摩配',u'汽摩配'),
    ('消费电子',u'消费电子'),
    ('手机配件',u'手机配件'),
    ('电子烟',u'电子烟'),
    ('运动鞋服包/户外配附',u'运动鞋服包/户外配附')
)

class t_product_enter_ed_wish(t_base):
    Aliexpress_PL = models.CharField(u'速卖通品类',max_length=255,choices=Aliexpress_PL_choice,default=0,null = True)
    publish_count  = models.IntegerField(u'刊登次数',blank=True,null = True)
    onebuOperation = models.CharField(u'1部领用',max_length=10,default=0,null = True)
    twobuOperation = models.CharField(u'2部领用', max_length=10, default=0, null=True)
    threebuOperation = models.CharField(u'3部领用', max_length=10,default=0, null=True)
    fourbuOperation = models.CharField(u'4部领用', max_length=10, default=0, null=True)
    fivebuOperation = models.CharField(u'5部领用', max_length=10, default=0, null=True)
    sixbuOperation = models.CharField(u'6部领用', max_length=10, default=0, null=True)
    sevenbuOperation = models.CharField(u'7部领用', max_length=10, default=0, null=True)
    eightbuOperation = models.CharField(u'8部领用', max_length=10, default=0, null=True)
    ninebuOperation = models.CharField(u'9部领用', max_length=10, default=0, null=True)
    tenbuOperation = models.CharField(u'10部领用', max_length=10, default=0, null=True)
    elevenbuOperation = models.CharField(u'11部领用', max_length=10, default=0, null=True)
    twelvebuOperation = models.CharField(u'12部领用', max_length=10, default=0, null=True)
    thirteenbuOperation = models.CharField(u'13部领用', max_length=10, default=0, null=True)
    Wish_count = models.IntegerField(u'刊登次数', blank=True, null=True)
    Amazon_count = models.IntegerField(u'刊登次数', blank=True, null=True)
    eBay_count = models.IntegerField(u'刊登次数', blank=True, null=True)
    class Meta:
        verbose_name=u'wish刊登信息'
        verbose_name_plural=u'wish刊登信息'
        db_table = 't_product_enter_ed'
        ordering =  ['-id']
    def __unicode__(self):
        return u'id:%s MainSKU:%s'%(self.id,self.MainSKU)