# -*- coding: utf-8 -*-
from t_base import t_base

#2) 调研完成-待审核 t_product_survey_ed
class t_product_survey_ed(t_base):

    class Meta:
        verbose_name=u'调研审核'
        verbose_name_plural=u' 步骤 02---调研审核'
        db_table = 't_product_survey_ed'
        ordering =  ['CreateTime']
    def __unicode__(self):
        return u'id:%s MainSKU:%s'%(self.id,self.MainSKU)