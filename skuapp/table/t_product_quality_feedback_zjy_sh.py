# coding=utf-8


from skuapp.table.t_product_quality_feedback import *


class t_product_quality_feedback_zjy_sh(t_product_quality_feedback):

    class Meta:
        verbose_name = u'质检员审核领取'
        verbose_name_plural = verbose_name
        db_table = 't_product_quality_feedback_zjy_sh'
        ordering = ['-id']
        app_label = 'skuapp'
