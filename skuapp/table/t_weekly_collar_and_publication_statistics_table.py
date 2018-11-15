#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_weekly_collar_and_publication_statistics_table.py
 @time: 2018-04-16 13:00
"""

from django.db import models
from skuapp.table.t_sys_department import t_sys_department

def getdepID():
    return t_sys_department.objects.values_list('DepartmentID','DepartmentName').order_by('DepartmentID')

class t_weekly_collar_and_publication_statistics_table(models.Model):
    DepartmentID =   models.PositiveSmallIntegerField(u'部门编号',choices=getdepID(),blank = True,null = True)
    Week_No      =   models.CharField(u'周编号',max_length=32,blank = True,null = True)
    Seller       =   models.CharField(u'人员名称',max_length=32,blank = True,null = True)
    SellerID     =   models.CharField(u'人员工号',max_length=32,blank = True,null = True)
    Receive_No   =   models.PositiveSmallIntegerField(u'领取量',blank = True,null = True)
    PubNum       =   models.PositiveSmallIntegerField(u'及时刊登量',blank = True,null = True)
    NoPubNum     =   models.PositiveSmallIntegerField(u'未及时刊登量',blank = True,null = True)
    DepNum       =   models.PositiveSmallIntegerField(u'弃用量',blank = True,null = True)

    class Meta:
        verbose_name=u'周领用与刊登统计'
        verbose_name_plural=verbose_name
        db_table = 't_weekly_collar_and_publication_statistics_table'
        ordering =  ['-Week_No']
    def __unicode__(self):
        return u'id:%s'%(self.id)