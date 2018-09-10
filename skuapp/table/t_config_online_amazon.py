# -*- coding: utf-8 -*-
from django.db import models
from public import *
#amazon在线配置
class t_config_online_amazon(models.Model):
    IP             =   models.CharField(u'店铺IP',max_length=32,blank = True,null = True)
    Name           =   models.CharField(u'店铺名称',max_length=32,blank = True,null = True)
    #K              =   models.CharField(u'Key',max_length=32,blank = True,null = True)
    K              =   models.CharField(u'Key',choices=getChoices(ChoiceK),max_length=20,null = True)
    V              =   models.CharField(u'Value',max_length=64, blank=True,null = True)
    shop_name =  models.CharField(u'店铺',max_length=64, blank=True,null = True)
    site = models.CharField(u'站点', choices=getChoices(ChoiceSiteconfiguration), max_length=32, blank=True, null=True)
    class Meta:
        verbose_name=u'amazon在线配置'
        verbose_name_plural=u'amazon在线配置'
        db_table = 't_config_online_amazon'
        ordering =  ['IP','Name']
    def __unicode__(self):
        return u'%s'%(self.id)