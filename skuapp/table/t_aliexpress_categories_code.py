# coding=utf-8


from django.db import models

class t_aliexpress_categories_code(models.Model):
    ShopName        =   models.CharField(u'店铺名', max_length=64, blank=True, null=True)
    Classification  =   models.CharField(u'类目ID', max_length=16, blank=True, null=True)
    ProductCate     =   models.CharField(u'分类名称', max_length=64, blank=True, null=True)
    BandsCode       =   models.CharField(u'品牌ID', max_length=16, blank=True, null=True)
    BandsName       =   models.CharField(u'品牌名', max_length=16, blank=True, null=True)
    GroupCode       =   models.CharField(u'分组编码', max_length=16, blank=True, null=True)

    class Meta:
        verbose_name = u'AliExpress店铺分类'
        verbose_name_plural = verbose_name
        db_table = 't_aliexpress_categories_code'
        ordering = ['-id']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)