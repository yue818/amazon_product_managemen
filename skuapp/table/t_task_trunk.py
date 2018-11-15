# -*- coding: utf-8 -*-
from t_base import t_base
from django.db import models
from public import *
from django.contrib.auth.models import User
    
ChoiceResult = (
            ('success',u'通过'),
            ('fail',u'不通过'),
    )
ChoiceResult2 = (
            ('success',u'全部通过'),
            ('fail',u'不通过'),
    )


def getAllUser():
    userobjs = User.objects.values('username','first_name')
    usertmp = []
    for userobj in userobjs:
        usertmp.append([userobj['username'],u'%s/%s'%(userobj['username'],userobj['first_name'])])
    return usertmp

class t_task_trunk(models.Model):
    Original_number          =   models.AutoField(u'ID',max_length=12,primary_key=True, blank=False, null=False)
    Flow_Status              =   models.CharField(u'流程进度',choices=getChoices(ChoiceFlow),max_length=10,blank=True, null=True)
    Flow_type                =   models.CharField(u'类型', choices=getChoices(ChoiceDemand), max_length=32)

    Demand_name              =   models.CharField(u'问题名称', max_length=100)
    Demand_description       =   models.TextField(u'问题备注')
    AttachmentUrl1           =   models.FileField(u'附件一',blank = True,null = True)
    AttachmentUrl2           =   models.FileField(u'附件二',blank = True,null = True)
    AttachmentUrl3           =   models.FileField(u'附件三',blank = True,null = True)
    Create_man               =   models.CharField(u'创建人', max_length=32, blank=True, null=True)
    Create_time              =   models.DateTimeField(u'创建时间')
    Hope_time                =   models.DateField(u'期望解决时间',blank=True, null=True)


    Check_result             =   models.CharField(u'审核结果',max_length=10,choices=ChoiceResult, blank=True, null=True)
    Check_info               =   models.TextField(u'审核备注', blank=True, null=True)
    Check_man                =   models.CharField(u'下一步:审核人', max_length=32, choices=getChoices(ChoiceCheck),default='bianyong',blank=True,null=True)
    Check_time               =   models.DateTimeField(u'审核通过时间', blank=True, null=True)
    Ask_time                 =   models.DateField(u'要求解决时间',blank=True, null=True)


    Task_name_original       =   models.CharField(u'任务名称', max_length=32, blank=True, null=True)
    Task_status              =   models.CharField(u'处理状态',choices=getChoices(ChoiceTaskOperation),max_length=32, blank=True, null=True)
    Task_info                =   models.TextField(u'处理备注',blank=True, null=True)
    Task_handler_review      =   models.CharField(u'处理复核人',choices=getAllUser(),max_length=32,blank=True,null=True)
    Task_handler             =   models.CharField(u'下一步:处理人', max_length=32,choices=getAllUser(), blank=True, null=True)
    Task_handler_time        =   models.DateField(u'处理结束时间',blank=True, null=True)
    
    Pre_Identifier           =   models.CharField(u'指定业务验证人', max_length=32,choices=getAllUser(), blank=True, null=True)
    Identifier               =   models.CharField(u'下一步:业务验证人', max_length=32,choices=getAllUser(), blank=True, null=True)
    Identifier_info          =   models.TextField(u'验证备注', blank=True, null=True)
    In_Identifier            =   models.CharField(u'IT自验证总负责人',max_length=32,choices=getAllUser(), blank=True, null=True)
    Identifier_In_result     =   models.CharField(u'IT自验证结果',max_length=64,choices=ChoiceResult2, blank=True, null=True)
    Identifier_result        =   models.CharField(u'验证结果',max_length=10,choices=ChoiceResult, blank=True, null=True)
    Identifier_time          =   models.DateTimeField(u'验证时间', blank=True, null=True)

    Current_chargeman        =   models.CharField(u'当前责任人', max_length=32, blank=True, null=True)
    Update_time              =   models.DateTimeField(u'最后更新时间', auto_now=True)

                             

    class Meta:
        verbose_name=u'任务主线表'
        verbose_name_plural=u'任务主线表'
        db_table = 't_task_trunk'
        ordering =  ['-Update_time']
    def __unicode__(self):
        return u'Original_number:%s'%(self.Original_number)