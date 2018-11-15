# -*- coding: utf-8 -*-
from django.db import models
from skuapp.table.public import *

class t_translation(models.Model):
    Translated          =   models.FileField(u'待翻译文件',blank = True,null = True)
    FromLanguage        =   models.CharField(u'待翻译语言',choices=getChoices(ChoiceFromLanguage),max_length = 8,blank = True,null = False)
    Title               =   models.TextField(u'待翻译标题',blank = True,null = True)
    Description         =   models.TextField(u'待翻译描述',blank = True,null = True)
    Submiter            =   models.CharField(u'提交人',max_length = 31,blank = True,null = True)
    SubmitTime          =   models.DateTimeField(u'提交时间',blank = True,null = True)
    ToLanguage          =   models.CharField(u'翻译成语言',choices=getChoices(ChoiceToLanguage),max_length = 8,blank = True,null = False)
    Title_ed            =   models.TextField(u'已翻译标题',blank = True,null = True)
    Description_ed      =   models.TextField(u'已翻译描述',blank = True,null = True)
    ExportTime          =   models.DateTimeField(u'导出时间',blank = True,null = True)
    
    
    class Meta:
        verbose_name=u'小平台翻译'
        verbose_name_plural=verbose_name
        db_table = 't_translation'
        ordering = ['-id']
    def __unicode__(self):
        return u'id:%s'%(self.id)