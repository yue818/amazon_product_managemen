#-*-coding:utf-8-*-
from django.db import models
from skuapp.table.t_config_shop_alias import t_config_shop_alias

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_template_amazon_advertising_keywords_report.py
 @time: 2018/8/21 9:51
"""

def getShopName():
    return t_config_shop_alias.objects.values_list('ShopName', 'ShopName')

class t_template_amazon_advertising_keywords_report(models.Model):
    upload_file = models.FileField(u'关键词xlsx文件', blank=False, null=False)

    start_date = models.DateTimeField(u'开始日期', blank=True, null=True)
    end_date = models.DateTimeField(u'结束日期', blank=True, null=True)
    currency = models.CharField(u'货币', max_length=12, blank=True, null=True)
    advertising_group_name = models.CharField(u'广告组名称', max_length=32, blank=True, null=True)
    advertising_campaign_name = models.CharField(u'广告活动名称', max_length=200, blank=True, null=True)
    keyword = models.CharField(u'关键词', max_length=200, blank=True, null=True)
    advertising_type = models.CharField(u'广告类型', max_length=200, blank=True, null=True)
    search_words = models.CharField(u'客户搜索词', max_length=32, blank=True, null=True)
    display_count = models.IntegerField(u'曝光量', max_length=11, blank=True, null=True)
    click_count = models.IntegerField(u'点击量', max_length=11, blank=True, null=True)
    CTR = models.CharField(u'点击率(%)', max_length=32, blank=True, null=True)
    CPC = models.DecimalField(u'每次点击成本($)', max_digits=10, decimal_places=2, blank=True, null=True)
    cost = models.DecimalField(u'花费($)', max_digits=10, decimal_places=2, blank=True, null=True)
    sales_7_count = models.DecimalField(u'七天总销售额($)', max_digits=10, decimal_places=2, blank=True, null=True)
    ACoS = models.CharField(u'ACOS(%)', max_length=32, blank=True, null=True)
    RoAS = models.CharField(u'RoAS(%)', max_length=32, blank=True, null=True)
    conversion_7_rate = models.CharField(u'7天转化率(%)', max_length=32, blank=True, null=True)
    orders_7_count = models.IntegerField(u'7天总订单数', max_length=11, blank=True, null=True)
    ordered_7_count = models.IntegerField(u'7天总销量', max_length=11, blank=True, null=True)
    ordered_7_sku_in_count = models.IntegerField(u'7天内广告SKU销售量', max_length=11, blank=True, null=True)
    ordered_7_sku_out_count = models.IntegerField(u'7天内其他SKU销售量', max_length=11, blank=True, null=True)
    sales_7_sku_in_count = models.DecimalField(u'7天内广告SKU销售额($)', max_digits=10, decimal_places=2, blank=True,
                                               null=True)
    sales_7_sku_out_count = models.DecimalField(u'7天内其他SKU销售额($)', max_digits=10, decimal_places=2, blank=True,
                                                null=True)

    shopname = models.CharField(u'店铺名称', choices=getShopName(), max_length=64, blank=False, null=False)
    ShopSKU = models.CharField(u'店铺SKU/ASIN', max_length=512, blank=True, null=True)
    action_remark = models.TextField(u'操作备注', blank=True, null=True)
    remark = models.TextField(u'备注', blank=True, null=True)

    upload_time = models.DateTimeField(u'上传时间', blank=True, null=True)
    upload_user = models.CharField(u'上传人', max_length=32, blank=True, null=True)
    update_user = models.CharField(u'更新人', max_length=32, blank=True, null=True)
    update_time = models.DateTimeField(u'更新时间', blank=True, null=True)

    advertising_keyword_date = models.DateField(u'关键词时间', blank=False, null=False)
    advertising_keyword_start_date = models.DateField(u'关键词周开始时间', blank=False, null=False)
    advertising_keyword_end_date = models.DateField(u'关键词周结束时间', blank=False, null=False)


    class Meta:
        verbose_name = u'Amazon广告关键词报告表'
        verbose_name_plural = verbose_name
        db_table = 't_template_amazon_advertising_keywords_report'
        ordering = ['-id']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)