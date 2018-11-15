# -*- coding: utf-8 -*-
from django.db import models
from public import *
from django.db import transaction,connection
from skuapp.table.t_sys_department import *

shop_st = (
    (1,'是'),
    (2,'否'),
)

clean_st = (
    (1,'已清理'),
    (2,'未清理'),
)

def getDepartmentID():
    return t_sys_department.objects.values_list('DepartmentID','DepartmentName').all().order_by('id') 
class t_config_mstscfinance(models.Model):
    IP                      =   models.CharField(u'店铺IP',max_length=32,blank = True,null = True)
    out_ip                  =   models.CharField(u'外网IP',max_length=32,blank = True,null = True)
    ShopName                =   models.CharField(u'店铺名称',max_length=32,blank = True,null = True)
    seller                  =   models.CharField(u'销售员',max_length=32,blank = True,null = True)
    PlatformName            =   models.CharField(u'平台名称',choices=getChoices(ChoicePlatformName),max_length=16,blank = True,null = True)
    UserName                =   models.CharField(u'用户名',max_length=64,blank = True,null = True)
    Password                =   models.CharField(u'密码(明文)',max_length=64,blank = True,null = True)
    #StaffID                 =   models.CharField(u'工号',max_length=31,blank = True,null = True)
    #Status          =   models.CharField(u'状态',choices=getChoices(ChoiceStatus_mstsc),max_length=16,blank = True,null = True)
    
    DepartmentName          =   models.CharField(u'归属部门',choices=getDepartmentID(),max_length=128)
    InstanceId                =   models.CharField(u'主机编号',max_length=64,blank = True,null = True)
    RegionId                 =   models.CharField(u'主机所在地区',choices=getChoices(ChoiceRegionId),max_length=20,blank = True,null = True)
    remarks                 =   models.CharField(u'备注',max_length=255,blank = True,null = True)
    CloudName                 =   models.CharField(u'主机平台',choices=getChoices(ChoiceCloudName),max_length=255,blank = True,null = True)
    kvmName                =   models.CharField(u'虚拟机名称',max_length=64,blank=True,null=True)
    hostip                 =   models.CharField(u'主机IP',max_length=64,blank=True,null=True)
    shop_status                =   models.IntegerField(u'店铺存活状态',choices=shop_st,max_length=64,blank=True,null=True)
    clean_status             =   models.IntegerField(u'清理状态',choices=clean_st,max_length=64,blank=True,null=True)
    
    class Meta:
        verbose_name=u'远程桌面登录配置'
        verbose_name_plural=u'远程桌面登录配置'
        db_table = 't_config_mstsc'
        ordering =  ['PlatformName','ShopName']
    def __unicode__(self):
        return u'%s'%(self.id)