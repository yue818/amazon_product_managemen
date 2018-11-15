#-*-coding:utf-8-*-
from django.db import models
from skuapp.table.t_config_shop_alias import t_config_shop_alias
"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_template_amazon_business_report.py
 @time: 2018/8/16 10:49
"""
def getShopName():
    return t_config_shop_alias.objects.values_list('ShopName', 'ShopName')

class t_template_amazon_business_report(models.Model):
    upload_file                     = models.FileField(U'Excel文件', blank=True, null=True)
    parent_ASIN                     = models.CharField(u'(父） ASIN', max_length=32, blank=True, null=True)
    child_ASIN                      = models.CharField(u'（子）ASIN', max_length=32, blank=True, null=True)
    item_name                       = models.CharField(u'商品名称', max_length=256, blank=True, null=True)
    ShopSKU                         = models.CharField(u'店铺SKU', max_length=512, blank=True, null=True)
    visit_count                     = models.IntegerField(u'买家访问次数',max_length=11,blank = True,null = True)
    visit_percent                   = models.CharField(u'买家访问次数百分比', max_length=32, blank=True, null=True)
    viewed_count                    = models.IntegerField(u'页面浏览次数',max_length=11,blank = True,null = True)
    viewed_percent                  = models.CharField(u'页面浏览次数百分比', max_length=32, blank=True, null=True)
    buyed_button_percent            = models.CharField(u'购买按钮赢得率', max_length=32, blank=True, null=True)
    ordered_count                   = models.IntegerField(u'已订购商品数量',max_length=11,blank = True,null = True)
    ordered_count_Conversion_rate   = models.CharField(u'订单商品数量转化率', max_length=32, blank=True, null=True)
    ordered_sales                   = models.DecimalField(u'已订购商品销售额', max_digits=10, decimal_places=2, blank=True, null=True)
    ordered_types                   = models.IntegerField(u'订单商品种类数',max_length=11,blank = True,null = True)
    upload_time                     = models.DateTimeField(u'上传时间', blank=True, null=True)
    upload_user                     = models.CharField(u'上传人', max_length=32, blank=True, null=True)
    update_user                     = models.CharField(u'更新人', max_length=32, blank=True, null=True)
    update_time                     = models.DateTimeField(u'更新时间', blank=True, null=True)
    shopname                        = models.CharField(u'店铺名称', choices=getShopName(), max_length=64, blank=True, null=True)
    business_date                   = models.DateField(u'业务时间', blank=True, null=True)

    class Meta:
        verbose_name = u'Amazon业务报告表'
        verbose_name_plural = verbose_name
        db_table = 't_template_amazon_business_report'
        ordering = ['-id']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)