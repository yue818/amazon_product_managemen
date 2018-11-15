#-*-coding:utf-8-*-
from django.db import models

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_product_upc_id_amazon.py
 @time: 2018/3/26 17:30
"""
class t_product_upc_id_amazon(models.Model):
    external_product_id         = models.CharField(u'Amazon标识码', max_length=64, blank=True, null=True)
    external_product_id_type    = models.CharField(u'标识码类型', max_length=64, blank=True, null=True)
    use_status                  = models.CharField(u'使用状态', max_length=32, blank=True, null=True)
    createUser                  = models.CharField(u'创建人', max_length=64, blank=True, null=True)
    createTime                  = models.DateTimeField(u'创建时间', blank=True, null=True)
    updateUser                  = models.CharField(u'更新人', max_length=64, blank=True, null=True)
    updateTime                  = models.DateTimeField(u'更新时间', blank=True, null=True)

    class Meta:
        verbose_name = u'Amazon标识码表'
        verbose_name_plural = verbose_name
        db_table = 't_product_upc_id_amazon'
        ordering = ['-id']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)
