# coding=utf-8


from skuapp.table.t_product_quality_feedback import *


class t_product_quality_feedback_submit(t_product_quality_feedback):

    class Meta:
        verbose_name = u'提交质量反馈'
        verbose_name_plural = verbose_name
        db_table = 't_product_quality_feedback_submit'
        ordering = ['-id']
        app_label = 'skuapp'