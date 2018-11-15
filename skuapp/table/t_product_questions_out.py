# -*- coding: utf-8 -*-
from django.db import models
from public import *
class t_product_questions_out(models.Model):
    PTitle        =  models.CharField(u'标题',max_length=16,blank = True,null = True)
    Priority      =  models.CharField(u'优先级',max_length=16,choices=getChoices(ChoicePriority),blank = True,null = True)
    Status        =  models.CharField(u'状态',max_length=16,choices=getChoices(ChoiceStatus),blank = True,null = True)
    SubmitDay   =  models.DateField(u'问题提交时间日期',max_length=16,blank = True,null = True)
    ExpectedDay   =  models.DateField(u'期望解决日期',max_length=16,blank = True,null = True)
    StaffIDSubmit =  models.CharField(u'问题提交人',max_length=16,blank = True,null = True)
    StaffIDHandle =  models.CharField(u'问题处理人',max_length=16,blank = True,null = True)
    StaffID       =  models.CharField(u'工号',max_length=16,blank = True,null = True)
    Description   =  models.TextField(u'问题描述',blank = True,null = True)
    UpdateTime    =  models.DateTimeField(u'更新时间',auto_now=True,blank = True,null = True)
    Type          =  models.CharField(u'问题类型',max_length=16,choices=getChoices(ChoiceType),blank = True,null = True)
    LevelNumber   =  models.CharField(u'紧急程度',max_length=16,blank = True,null = True);
    
    ExecutedDay   =  models.DateField(u'计划解决日期',max_length=16,blank = True,null = True)
    StaffIDCheck =  models.CharField(u'问题审核人',max_length=16,blank = True,null = True)
    Remark         =   models.TextField(u'备注',blank = True,null = True)
    AttachmentUrl1 =   models.FileField(u'附件一',upload_to='media/',blank = True,null = True)
    AttachmentUrl2 =   models.FileField(u'附件二',upload_to='media/',blank = True,null = True)
    AttachmentUrl3 =   models.FileField(u'附件三',upload_to='media/',blank = True,null = True)
    AttachmentUrl4 =   models.FileField(u'附件四',upload_to='media/',blank = True,null = True)
    AttachmentUrl5 =   models.FileField(u'附件五',upload_to='media/',blank = True,null = True)
    AttachmentUrl6 =   models.FileField(u'附件六',upload_to='media/',blank = True,null = True)
    IT_IN_OUT =   models.CharField(u'IN/OUT',max_length=16,blank = True,null = True,default='OUT')
    class Meta:
        verbose_name=u'软件需求跟踪单'
        verbose_name_plural=u'软件需求跟踪单'
        db_table = 't_product_questions'
        ordering =  ['-LevelNumber','UpdateTime']
    def __unicode__(self):
        return self.PTitle