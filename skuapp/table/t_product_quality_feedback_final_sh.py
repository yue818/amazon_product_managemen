# coding=utf-8


from skuapp.table.t_product_quality_feedback import *


class t_product_quality_feedback_final_sh(t_product_quality_feedback):
    ZJY_Pic         = models.TextField(u'质检图片', blank=True, null=True)
    Last_Source     =   models.CharField(u'上一步来源页面', max_length=32, blank=True, null=True)


    class Meta:
        verbose_name = u'质检最终审核'
        verbose_name_plural = verbose_name
        db_table = 't_product_quality_feedback_final_sh'
        ordering = ['-id']
        app_label = 'skuapp'