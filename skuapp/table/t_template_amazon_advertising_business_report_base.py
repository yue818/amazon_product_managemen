#-*-coding:utf-8-*-
from django.db import models
from skuapp.table.t_config_shop_alias import t_config_shop_alias

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_template_amazon_advertising_business_report_base.py
 @time: 2018/8/21 9:51
"""

def getShopName():
    return t_config_shop_alias.objects.values_list('ShopName', 'ShopName')

class t_template_amazon_advertising_business_report_base(models.Model):
    upload_advertising_file     = models.FileField(u'广告CSV文件', blank=False, null=False)
    upload_business_file        = models.FileField(u'业务CSV文件', blank=False, null=False)

    start_date                  = models.DateTimeField(u'开始日期', blank=True, null=True)
    end_date                    = models.DateTimeField(u'结束日期', blank=True, null=True)
    advertising_status          = models.CharField(u'广告状态', max_length=12, blank=True, null=True)
    advertising_campaign_name   = models.CharField(u'广告活动名称', max_length=200, blank=True, null=True)
    advertising_cost_status     = models.CharField(u'广告花费状态', max_length=200, blank=True, null=True)
    advertising_type            = models.CharField(u'广告类型', max_length=200, blank=True, null=True)
    serving                     = models.CharField(u'投放', max_length=32, blank=True, null=True)
    CNY                         = models.IntegerField(u'预算($)', max_length=11, blank=True, null=True)
    display_count               = models.IntegerField(u'曝光量', max_length=11, blank=True, null=True)
    click_count                 = models.IntegerField(u'点击量', max_length=11, blank=True, null=True)
    CTR                         = models.CharField(u'点击率(%)', max_length=32, blank=True, null=True)
    CPC                         = models.DecimalField(u'每次点击成本($)', max_digits=10, decimal_places=2, blank=True, null=True)
    cost                        = models.DecimalField(u'花费($)', max_digits=10, decimal_places=2, blank=True, null=True)
    ACoS                        = models.CharField(u'ACOS(%)', max_length=32, blank=True, null=True)
    orders_count                = models.IntegerField(u'广告订单数', max_length=11, blank=True, null=True)
    sales_count                 = models.DecimalField(u'广告销售额($)', max_digits=10, decimal_places=2, blank=True, null=True)

    parent_ASIN                 = models.CharField(u'(父） ASIN', max_length=32, blank=True, null=True)
    child_ASIN                  = models.CharField(u'（子）ASIN', max_length=32, blank=True, null=True)
    item_name                   = models.CharField(u'商品名称', max_length=256, blank=True, null=True)
    ShopSKU                     = models.CharField(u'店铺SKU', max_length=512, blank=True, null=True)
    visit_count                 = models.IntegerField(u'买家访问次数', max_length=11, blank=True, null=True)
    visit_percent               = models.CharField(u'买家访问次数百分比(%)', max_length=32, blank=True, null=True)
    viewed_count                = models.IntegerField(u'页面浏览次数', max_length=11, blank=True, null=True)
    viewed_percent              = models.CharField(u'页面浏览次数百分比(%)', max_length=32, blank=True, null=True)
    buyed_button_percent        = models.CharField(u'购买按钮赢得率', max_length=32, blank=True, null=True)
    ordered_count               = models.IntegerField(u'已订购商品数量', max_length=11, blank=True, null=True)
    ordered_count_Conversion_rate = models.CharField(u'订单商品数量转化率(%)', max_length=32, blank=True, null=True)
    ordered_sales               = models.DecimalField(u'已订购商品销售额($)', max_digits=10, decimal_places=2, blank=True, null=True)
    ordered_types               = models.IntegerField(u'订单商品种类数', max_length=11, blank=True, null=True)

    AS_amazon                   = models.CharField(u'AS(%)', max_length=12, blank=True, null=True)
    AT_amazon                   = models.CharField(u'AT(%)', max_length=12, blank=True, null=True)
    shopname                    = models.CharField(u'店铺名称',choices=getShopName(), max_length=64, blank=False, null=False)
    action_remark               = models.TextField(u'操作备注', blank=True, null=True)
    remark                      = models.TextField(u'备注', blank=True, null=True)

    upload_time                 = models.DateTimeField(u'上传时间', blank=True, null=True)
    upload_user                 = models.CharField(u'上传人', max_length=32, blank=True, null=True)
    update_user                 = models.CharField(u'更新人', max_length=32, blank=True, null=True)
    update_time                 = models.DateTimeField(u'更新时间', blank=True, null=True)

    advertising_business_date   = models.DateField(u'业务广告时间', blank=False, null=False)
    image_url                   = models.CharField(u'图片', max_length=128, blank=True, null=True)
    business_more               = models.CharField(u'多业务', max_length=12, blank=True, null=True)
    advertising_more            = models.CharField(u'多广告', max_length=12, blank=True, null=True)

    class Meta:
        app_label = 'skuapp'
        abstract = True
    def __unicode__(self):
        return u'id:%s'% (self.id)