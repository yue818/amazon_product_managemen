#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_Three_Grade_Classification_Of_Clothing.py
 @time: 2018-03-09 9:40
"""

from django.db import models

class t_Three_Grade_Classification_Of_Clothing(models.Model):
    CateOne       =   models.CharField(u'一类',max_length=64,blank = True,null = True)
    CateTwo       =   models.CharField(u'二类', max_length=64, blank=True, null=True)
    CateThree     =   models.CharField(u'三类', max_length=64, blank=True, null=True)
    ThePerson     =   models.CharField(u'负责人', max_length=64, blank=True, null=True)

    class Meta:
        verbose_name = u'服装三级分类对应关系表'
        verbose_name_plural = verbose_name
        db_table = 't_Three_Grade_Classification_Of_Clothing'

    def __unicode__(self):
        return u'id:%s MainSKU:%s'%(self.id,self.MainSKU)