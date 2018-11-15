#-*-coding:utf-8-*-
from django.db import models
from skuapp.table.t_config_shop_alias import t_config_shop_alias

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_template_amazon_advertising_report.py
 @time: 2018/8/16 9:59
"""
def getShopName():
    return t_config_shop_alias.objects.values_list('ShopName', 'ShopName')

class t_template_amazon_advertising_report(models.Model):
    upload_file                 = models.FileField(U'Excel文件', blank=True, null=True)
    start_date                  = models.DateTimeField(u'开始日期', blank=True, null=True)
    end_date                    = models.DateTimeField(u'结束日期', blank=True, null=True)
    advertising_status          = models.CharField(u'广告状态', max_length=12, blank=True, null=True)
    advertising_campaign_name   = models.CharField(u'广告活动名称', max_length=200, blank=True, null=True)
    advertising_cost_status     = models.CharField(u'广告花费状态', max_length=200, blank=True, null=True)
    advertising_type            = models.CharField(u'广告类型', max_length=200, blank=True, null=True)
    serving                     = models.CharField(u'投放', max_length=32, blank=True, null=True)
    CNY                         = models.IntegerField(u'预算',max_length=11,blank = True,null = True)
    display_count               = models.IntegerField(u'曝光量',max_length=11,blank = True,null = True)
    click_count                 = models.IntegerField(u'点击量',max_length=11,blank = True,null = True)
    CTR                         = models.CharField(u'点击率', max_length=32, blank=True, null=True)
    CPC                         = models.DecimalField(u'每次点击成本', max_digits=10, decimal_places=2, blank=True, null=True)
    cost                        = models.DecimalField(u'花费', max_digits=10, decimal_places=2, blank=True, null=True)
    ACoS                        = models.CharField(u'投入产出比', max_length=32, blank=True, null=True)
    orders_count                = models.IntegerField(u'订单数',max_length=11,blank = True,null = True)
    sales_count                 = models.DecimalField(u'销售量', max_digits=10, decimal_places=2, blank=True, null=True)
    shopname                    = models.CharField(u'店铺名称', choices=getShopName(), max_length=64, blank=True, null=True)
    upload_time                 = models.DateTimeField(u'上传时间', blank=True, null=True)
    upload_user                 = models.CharField(u'上传人', max_length=32, blank=True, null=True)
    update_user                 = models.CharField(u'更新人', max_length=32, blank=True, null=True)
    update_time                 = models.DateTimeField(u'更新时间', blank=True, null=True)

    ShopSKU                     = models.CharField(u'店铺SKU', max_length=512, blank=True, null=True)
    advertising_data            = models.DateField(u'广告时间', blank=True, null=True)

    class Meta:
        verbose_name = u'Amazon产品广告报告表'
        verbose_name_plural = verbose_name
        db_table = 't_template_amazon_advertising_report'
        ordering = ['-id']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)