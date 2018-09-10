#-*-coding:utf-8-*-
from django.db import models
from skuapp.table.t_config_shop_alias import t_config_shop_alias

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_config_amazon_template.py
 @time: 2018/7/25 15:16
"""
def getShopName():
    return t_config_shop_alias.objects.values_list('ShopName', 'ShopName')

class t_config_amazon_template(models.Model):
    template_name       = models.CharField(u'运费模板名称', max_length=32, blank=False, null=False)
    shopName            = models.CharField(u'店铺名称', choices=getShopName(), max_length=32, blank=False, null=False)
    CreateTime          = models.DateTimeField(u'创建时间', blank=True, null=True)
    CreateName          = models.CharField(u'创建人', max_length=32, blank=True, null=True)
    freight             = models.DecimalField(u'运费', max_digits=10, decimal_places=2, blank=False, null=False)

    class Meta:
        verbose_name = u'Amazon运费模板配置表'
        verbose_name_plural = verbose_name
        db_table = 't_config_amazon_template'
        ordering = ['-id']

    def __unicode__(self):
        return u'id:%s'% (self.id)