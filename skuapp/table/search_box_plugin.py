# -*-coding=utf-8-*-
from django.db import models

class search_box_plugin(models.Model):
    id_name         = models.CharField(u'列名',max_length=64,blank = True,null = True)
    descri          = models.CharField(u'描述', max_length=100, blank=True, null=True)
    urlname1        = models.CharField(u'地址名1', max_length=100, blank=True, null=True)
    defult_value1   = models.TextField(u'默认值1', blank=True, null=True)
    value1          = models.CharField(u'值1', max_length=100, blank=True, null=True)
    urlname2        = models.CharField(u'地址名2', max_length=100, blank=True, null=True)
    defult_value2   = models.TextField(u'默认值2', blank=True, null=True)
    value2          = models.CharField(u'值2', max_length=100, blank=True, null=True)
    selection       = models.PositiveSmallIntegerField(u'选择', max_length=10, blank=True, null=True)
    isDate          = models.PositiveSmallIntegerField(u'日期', max_length=10, blank=True, null=True)
    startNum        = models.PositiveSmallIntegerField(u'tr起始数', max_length=10, blank=True, null=True)
    endNum          = models.PositiveSmallIntegerField(u'tr终止值', max_length=10, blank=True, null=True)
    model_name      = models.CharField(u'模块名', max_length=100, blank=True, null=True)
    inputs          = models.PositiveSmallIntegerField(u'多输入框', max_length=10, blank=True, null=True)

    class Meta:
        verbose_name=u'查询框参数'
        verbose_name_plural=verbose_name
        db_table = 'search_box_plugin'
    def __unicode__(self):
        return u'id:%s'%(self.id)