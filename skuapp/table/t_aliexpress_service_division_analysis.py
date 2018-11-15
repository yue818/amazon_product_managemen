# coding=utf-8
from django.db import models
from django.forms import ModelForm,forms
from django.utils.html import format_html

hanler_status=((True,u'已处理'),(False,u'未处理'))

class t_aliexpress_service_division_analysis(models.Model):
    id=models.AutoField(u'ID',primary_key=True)
    Productid = models.CharField(u'产品ID', max_length=32, blank=False, null=False)
    Category = models.CharField(u'类目', max_length=64, blank=True, null=False)
    Disputes_rate = models.FloatField(u'货不对版纠纷提起率', blank=True, null=True)
    DSR_description = models.FloatField(u'DSR商品描述', blank=True, null=True)
    Inputdatetime = models.DateTimeField(u'提交时间', blank=True, null=True)
    Status= models.BooleanField(u'状态',blank=True, null=False,default=False)
    Importuser= models.CharField(u'导入人', max_length=32, blank=True, null=False)
    Handler_status=models.BooleanField(u'处理状态',blank=True, null=False,choices=hanler_status,default=False)
    Seller_Name=models.CharField(u'卖家',max_length=64, blank=True, null=False)
    DSR_description_standard = models.FloatField(u'DSR商品描述考核值(>=)', max_length=8,blank=True, null=True)
    Disputes_rate_standard = models.FloatField(u'货不对版纠纷提起率(%)考核值(<)', max_length=8,blank=True, null=True)
    Remark = models.TextField(u'备注',max_length=255,blank=True,null=True)


    class Meta:
        verbose_name = u'速卖通服务分分析及异常信息'
        verbose_name_plural = verbose_name
        db_table = 't_aliexpress_service_division_analysis'
        ordering = ['-Inputdatetime','Category','Seller_Name']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.Category)

    def Discolored(self):
        if self.Disputes_rate < self.Disputes_rate_standard:
            color_code=u'green'
        else:
            color_code=u'red'
        return format_html(
            '<span style="color :{};">{}</span>',
            color_code,
            self.Disputes_rate
                           )

    Discolored.short_description = u"货不对版纠纷提起率(%)"

    def DSRcolored(self):
        if self.DSR_description >=self.DSR_description_standard:
            color_code=u'green'
        else:
            color_code=u'red'
        return format_html(
            '<span style="color :{};">{}</span>',
            color_code,
            self.DSR_description
                           )

    DSRcolored.short_description=u"DSR商品描述"