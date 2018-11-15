# -*- coding: utf-8 -*-
from django.db import models
from skuapp.table.public import *

class t_small_platform_translation(models.Model):
    Waiting_for_translation          =   models.FileField(u'待翻译文件',blank = True,null = True)
    FromLanguage                     =   models.CharField(u'待翻译语言',choices=getChoices(ChoiceFromLanguage),max_length = 8,blank = True,null = False)
    ToLanguage                       =   models.CharField(u'翻译成语言',choices=getChoices(ChoiceToLanguage),max_length = 8,blank = True,null = False)
    Has_been_translated              =   models.CharField(u'已翻译文件',max_length = 32,blank = True,null = True)
    Submiter                         =   models.CharField(u'提交人',max_length = 32,blank = True,null = True)
    SubmitTime                       =   models.DateTimeField(u'提交时间',blank = True,null = True)
    StartTime                        =   models.DateTimeField(u'翻译开始时间',blank = True,null = True)
    ExportTime                       =   models.DateTimeField(u'翻译完成时间',blank = True,null = True)
    Process                          =   models.CharField(u'翻译进程',choices=getChoices(ChoiceProcess),max_length = 8,blank = True,null = True)
    
    class Meta:
        verbose_name=u'平台语言翻译'
        verbose_name_plural=verbose_name
        db_table = 't_small_platform_translation'
        ordering = ['-id']
    def __unicode__(self):
        return u'id:%s'%(self.id)