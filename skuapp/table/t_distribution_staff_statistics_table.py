# -*- coding: utf-8 -*-

from django.db import models
from public import *
class t_distribution_staff_statistics_table(models.Model):
    SubmitTime        = models.DateTimeField(u'铺货时间',auto_now_add=True,blank=True,null = False)
    Submitter         = models.CharField(u'铺货人',max_length=15,db_index=True,blank=True,null = False)
    SKU_nub           = models.IntegerField(u'铺货sku数',max_length=6,db_index=True,blank=True,null = False)
    Shop_nub          = models.IntegerField(u'铺货店铺数',max_length=6,db_index=True,blank=True,null = False)
    Links_nub         = models.IntegerField(u'铺货链接总数',max_length=6,db_index=True,blank=True,null = False)
    Succ_nub          = models.IntegerField(u'铺货成功',max_length=6,db_index=True,blank=True,null = False)
    Error_nub         = models.IntegerField(u'铺货失败',max_length=6,db_index=True,blank=True,null = False)
    Already_nub       = models.IntegerField(u'已有数据铺货',max_length=6,db_index=True,blank=True,null = False)
    Manual_nub        = models.IntegerField(u'手动刊登铺货',max_length=6,db_index=True,blank=True,null = False)
    SKUdis_nub        = models.IntegerField(u'sku铺货',max_length=6,db_index=True,blank=True,null = False)
    Orders_nub        = models.IntegerField(u'铺货链接出单',max_length=6,db_index=True,blank=True,null = False)

    class Meta:
        ordering            = ['id']
        verbose_name        = u'sku铺货信息统计'
        verbose_name_plural = u'sku铺货信息统计'
        db_table            = 't_distribution_staff_statistics_table'
    def __unicode__(self):
        return self.id