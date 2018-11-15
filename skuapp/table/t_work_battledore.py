#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_work_battledore.py
 @time: 2018/6/12 19:30
"""

from django.db import models

class t_work_battledore(models.Model):
    image = models.CharField(u'图片', max_length=255,blank = True,null = True)
    urllink = models.CharField(u'产品链接', max_length=255,blank = True,null = True)
    submittime = models.DateTimeField(u'需求提交时间',blank = True,null = True)
    submiter = models.CharField(u'需求提交人', max_length=32,blank = True,null = True)
    keynote = models.CharField(u'卖点或配件', max_length=255,blank = True,null = True)
    color = models.CharField(u'需要颜色', max_length=255,blank = True,null = True)
    mainsku = models.CharField(u'主SKU', max_length=32,blank = True,null = True)
    linkali = models.CharField(u'1688链接', max_length=255,blank = True,null = True)
    checkman = models.CharField(u'核价员', max_length=32,blank = True,null = True)
    checktime =   models.DateTimeField(u'报价完成时间',blank = True,null = True)
    determinetime =   models.DateTimeField(u'确定面辅料完成时间',blank = True,null = True)
    patternman = models.CharField(u'纸样师', max_length=32,blank = True,null = True)
    patterntime =   models.DateTimeField(u'纸样样衣完成时间',blank = True,null = True)
    examinetime =   models.DateTimeField(u'审核样衣完成时间',blank = True,null = True)
    price = models.CharField(u'成本', max_length=100,blank = True,null = True)
    weight = models.CharField(u'克重', max_length=100,blank = True,null = True)
    num  = models.IntegerField(u'一条面料数量',max_length=16,blank = True,null = True)
    merchandiser = models.CharField(u'跟单员', max_length=100,blank = True,null = True)
    documentarytime  =   models.DateTimeField(u'跟单领取时间',blank = True,null = True)
    proflag  =   models.CharField(u'进度', max_length=2,blank = True,null = True)
    normalprice  =   models.CharField(u'正常售价', max_length=8,blank = True,null = True)
    aliprice  =   models.CharField(u'1688成本', max_length=8,blank = True,null = True)
    aliweight  =   models.CharField(u'1688克重', max_length=10,blank = True,null = True)
    subreamrk  =   models.CharField(u'需求备注', max_length=255,blank = True,null = True)
    pysize  =   models.CharField(u'普元尺码号', max_length=200,blank = True,null = True)
    cgperson  =   models.CharField(u'普元尺码号', max_length=32,blank = True,null = True)
    shearplate  =   models.CharField(u'剪版费用', max_length=32,blank = True,null = True)
    priceremark  =   models.CharField(u'报价备注', max_length=255,blank = True,null = True)

    class Meta:
        verbose_name=u'只打板'
        verbose_name_plural=verbose_name
        db_table = 't_work_battledore'
    def __unicode__(self):
        return u'%s,%s'%(self.id,self.mainsku)


