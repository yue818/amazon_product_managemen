# coding=utf-8

"""
每日铺货统计 MODEL
"""

from django.db import models

class t_wish_distribution_result_statistics_everyday(models.Model):

    d_date                      =   models.DateField(u'铺货日期', blank=True, null=True)
    d_collect_num               =   models.IntegerField(u'铺货采集数', max_length=11, blank=True, null=True)
    d_make_templet_num          =   models.IntegerField(u'制作模板数', max_length=11, blank=True, null=True)
    d_to_wait_upload_num        =   models.IntegerField(u'转待铺货数', max_length=11, blank=True, null=True)
    d_post_upload_num           =   models.IntegerField(u'提交铺货模板数', max_length=11, blank=True, null=True)
    d_to_upload_num             =   models.IntegerField(u'执行定时铺货数', max_length=11, blank=True, null=True)
    d_success_upload_num        =   models.IntegerField(u'铺货成功数', max_length=11, blank=True, null=True)
    d_wait_upload_num           =   models.IntegerField(u'铺货待执行数', max_length=11, blank=True, null=True)
    d_shop_num                  =   models.IntegerField(u'铺货店铺数', max_length=4, blank=True, null=True)
    d_shop_average_num          =   models.IntegerField(u'店铺平均铺货数', max_length=11, blank=True, null=True)
    d_templet_average_num       =   models.IntegerField(u'模板平均铺货数', max_length=11, blank=True, null=True)
    d_today_success_num         =   models.IntegerField(u'今日铺货成功数', max_length=11, blank=True, null=True)

    class Meta:
        verbose_name = u'每日铺货统计'
        verbose_name_plural = verbose_name
        ordering = ['-d_date']
        db_table = 't_wish_distribution_result_statistics_everyday'
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)
