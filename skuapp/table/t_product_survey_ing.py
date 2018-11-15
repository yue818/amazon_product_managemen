# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models
#1) 正在调研表 t_product_survey_ing
class t_product_survey_ing(t_base):
    #selectpic        =   models.ImageField(u'选择图片',upload_to='media/',blank=True, null=True)
    SourceURL0       =   models.CharField(u'上次抓取的URL',max_length=200,blank = True,null = True) #作为判断是否URL变化用
    class Meta:
        verbose_name=u'开始调研'
        verbose_name_plural=u' 步骤 01---开始调研'
        app_label = 'skuapp'
        db_table = 't_product_survey_ing'
        ordering =  ['CreateTime']
    def __unicode__(self):
        return u'id:%s MainSKU:%s'%(self.id,self.MainSKU)
