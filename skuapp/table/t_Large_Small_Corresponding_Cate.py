#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_Large_Small_Corresponding_Cate.py
 @time: 2018-03-08 13:35
"""

from django.db import models

class t_Large_Small_Corresponding_Cate(models.Model):
    LCode            =   models.CharField(u'大类代码',max_length=64,blank = True,null = True)
    LargeClass       =   models.CharField(u'大类',max_length=64,blank = True,null = True)
    SCode            =   models.CharField(u'小类代码', max_length=64, blank=True, null=True)
    SmallClass       =   models.CharField(u'小类', max_length=64, blank=True, null=True)

    class Meta:
        verbose_name = u'大小类对应关系表'
        verbose_name_plural = verbose_name
        db_table = 't_Large_Small_Corresponding_Cate'

    def __unicode__(self):
        return u'id:%s MainSKU:%s'%(self.id,self.MainSKU)




















