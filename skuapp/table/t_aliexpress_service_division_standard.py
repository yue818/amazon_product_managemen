# coding=utf-8
from django.db import models


class t_aliexpress_service_division_standard(models.Model):
    Check_level = models.SmallIntegerField(u'考核行业级别', blank=True, null=True)
    Primary_category = models.CharField(u'一级类目', max_length=64, blank=True, null=True)
    Second_category = models.CharField(u'二级类目', max_length=64, blank=True, null=True)
    Third_category = models.CharField(u'三级类目', max_length=64, blank=True, null=True)
    Fourth_category = models.CharField(u'四级类目', max_length=64, blank=True, null=True)
    DSR_description = models.FloatField(u'DSR商品描述', max_length=8,blank=True, null=True)
    Disputes_rate = models.FloatField(u'货不对版纠纷提起率(%)', max_length=8,blank=True, null=True)
    DSR_increase = models.FloatField(u'DSR商品描述提升值',default=0.2, max_length=8,blank=True, null=True)
    Dis_decrease = models.FloatField(u'货不对版纠纷提起率减小值',default=0.2, max_length=8,blank=True, null=True)
    Importdatetime = models.DateTimeField(u'提交时间', blank=True, null=True)

    id = models.AutoField(u'ID',primary_key=True)


    class Meta:
        verbose_name = u'速卖通服务分标准分'
        verbose_name_plural = verbose_name
        db_table = 't_aliexpress_service_division_standard'
        ordering = ['-Importdatetime','Primary_category']
        app_label = 'skuapp'

    def __unicode__(self):
        return u'%s' % (self.id)