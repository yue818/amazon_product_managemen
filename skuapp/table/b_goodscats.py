#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-03-01 11:17
# @Author  : Zhangyu
# @Site    : 
# @File    : b_goodscats.py
# @Software: PyCharm
from django.db import models


class b_goodscats(models.Model):
    NID                  =         models.IntegerField(u'NID', blank = True,primary_key=True)
    CategoryLevel        =         models.IntegerField(u'种类等级',max_length=10,blank = True,null = True)
    CategoryName         =         models.CharField(u'种类名称',max_length=255,blank = True,null = True)
    CategoryParentID     =         models.IntegerField(u'父ID',max_length=10,blank = True,null = True)
    CategoryParentName   =         models.CharField(u'父名称',max_length=255,blank = True,null = True)
    CategoryOrder        =         models.IntegerField(u'CategoryOrder',max_length=255,blank = True,null = True)
    CategoryCode         =         models.CharField(u'CategoryCode',max_length=255,blank = True,null = True)
    GoodsCount           =         models.IntegerField(u'GoodsCount',max_length=10,blank = True,null = True)

    class Meta:
        verbose_name=u'种类表'
        verbose_name_plural=verbose_name
        db_table = 'b_goodscats'
    def __unicode__(self):
        return u'%s %s'%(self.NID,self.CategoryName)