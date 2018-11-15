# coding=utf-8


from skuapp.table.t_product_quality_feedback import *


class t_product_quality_feedback_final_result(t_product_quality_feedback):
    ZJY_Pic = models.TextField(u'质检员图片', blank=True, null=True)

    class Meta:
        verbose_name = u'总结果反馈'
        verbose_name_plural = verbose_name
        db_table = 't_product_quality_feedback_final_result'
        ordering = ['-id']
        app_label = 'skuapp'