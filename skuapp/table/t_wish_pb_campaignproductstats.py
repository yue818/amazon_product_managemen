#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: changyang 
 @site: 
 @software: PyCharm
 @file: t_wish_pb_campaignproductstats.py
 @time: 2018-05-25 10:09
"""
from django.db import models
from public import *
import datetime

def get_max_budget():
    x = getChoices(wish_pb_max_budget)
    if len(x) == 0:
        return 9.0
    else:
        return x[0][0]

def get_start_time():
    x = datetime.datetime.now().strftime('%H:%M:%S')
    if x >= '15:00:00':
        stime = datetime.date.today() + datetime.timedelta(days=2)
    else:
        stime = datetime.date.today() + datetime.timedelta(days=1)
    return stime.strftime("%Y-%m-%d")

def get_end_time():
    x = datetime.datetime.now().strftime('%H:%M:%S')
    if x >= '15:00:00':
        etime = datetime.date.today() + datetime.timedelta(days=9)
    else:
        etime = datetime.date.today() + datetime.timedelta(days=8)
    return etime.strftime("%Y-%m-%d")

# 千分位
class thousandSeparatorField(models.CharField):
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if not value:
            return value
        try:
            return format(value, ',')
        except Exception:
            return value
    def get_prep_value(self, value):
        if not value:
            return value
        try:
            return int(value.replace(',', ''))
        except Exception:
            return value

warehouseType = [(u'非海外仓',u'非海外仓'), (u'海外仓',u'海外仓')]

class t_wish_pb_campaignproductstats(models.Model):

    id					= models.AutoField(u'流水号', primary_key=True)
    shopname			= models.CharField(u'店铺', max_length=50, blank=True, null=True, help_text=u'店铺简称,新品创建广告时必填.')
    campaign_id			= models.CharField(u'活动ID', max_length=25, blank=True, null=True)
    campaign_name       = models.CharField(u'活动名称', max_length=100, blank=True, null=True)
    product_id			= models.CharField(u'产品ID', max_length=25, blank=False, help_text=u'不能存在于其它未结束的活动中.')
    product_name		= models.CharField(u'产品名称', max_length=500, blank=True, null=True)
    paid_impressions	= thousandSeparatorField(u'付费曝光量', max_length=20, blank=True, null=True)
    spend				= models.DecimalField(u'花费', max_digits=6, decimal_places=2)
    sales				= models.IntegerField(u'订单数')
    gmv					= models.DecimalField(u'销售额', max_digits=8, decimal_places=2)
    last_updated_time	= models.CharField(u'API更新时间', max_length=20, blank=True, null=True)
    keywords			= models.TextField(u'关键词', blank=False, help_text=u'关键词请用英文逗号隔开.')
    bid					= models.DecimalField(u'竞价', max_digits=6, decimal_places=2, blank=False, default=0.3, help_text=u'竞价金额最少0.3$最多10$.')
    max_budget			= models.DecimalField(u'预算', max_digits=6, decimal_places=2, blank=False, default=get_max_budget, help_text=u'此活动准备花费的最大金额.')
    start_time			= models.DateField(u'PB开始时间', blank=False, default=get_start_time, help_text=u'活动开始时间(太平洋标准时间).')
    end_time			= models.DateField(u'PB结束时间', blank=False, default=get_end_time, help_text=u'活动结束时间(太平洋标准时间).')
    auto_renew			= models.CharField(u'是否重复', max_length=10, blank=False, choices=getChoices(ChoiceAutoRenew), default='True', help_text=u'此活动是否重复运行.')
    campaign_state		= models.CharField(u'活动状态', max_length=20, choices=getChoices(ChoiceCampaignState))
    sku					= models.CharField(u'商品SKU', max_length=255, blank=True, null=True)
    publish_date		= models.DateField(u'刊登日期', blank=True, null=True)
    sales_price			= models.CharField(u'售价', max_length=20, blank=True, null=True)
    survey_remark		= models.TextField(u'调研备注', blank=True, null=True)
    operation_remark	= models.TextField(u'操作备注', blank=True, null=True)
    dataflag			= models.SmallIntegerField(u'广告类型标识')
    StaffID             = models.CharField(u'操作人员', max_length=20, blank=True, null=True)
    spend_gmv           = models.DecimalField(u'AS(%)', max_digits=8, decimal_places=2, blank=True, null=True)
    sales_paid          = models.DecimalField(u'曝光转化率(%)', max_digits=8, decimal_places=3, blank=True, null=True)
    seller              = models.CharField(u'店长/销售员', max_length=20, blank=True, null=True)
    CreateUser          = models.CharField(u'广告创建人', max_length=20, blank=True, null=True)

    LargeCategory       = models.CharField(u'大类名称', max_length=32, blank=True, null=True)
    ClothingSystem1     = models.CharField(u'服装一级分类', max_length=255, blank=True, null=True)
    ClothingSystem2     = models.CharField(u'服装二级分类', max_length=255, blank=True, null=True)
    ClothingSystem3     = models.CharField(u'服装三级分类', max_length=255, blank=True, null=True)

    StoreName           = models.CharField(u'仓库类别', max_length=50, blank=False, choices=warehouseType, default='非海外仓', help_text=u'此活动针对的发货仓类别.')

    Automated           = models.CharField(u'自动广告标识', max_length=10, blank=True, default='False')

    updatetime			= models.DateTimeField(u'更新时间',)

    class Meta:
        verbose_name = u'Wish广告'
        verbose_name_plural = u'Wish广告'
        db_table = 't_wish_pb_campaignproductstats'
        ordering = ['product_id', '-start_time']

    def __unicode__(self):
        return u'%s' % (self.product_id, )