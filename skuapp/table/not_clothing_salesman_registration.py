# -*- coding: utf-8 -*-
from django.db import models
from .public import *


class not_clothing_salesman_registration(models.Model):
    
    Category = models.CharField(u'类目',choices=getChoices(ChoiceCategory),max_length=16,blank = False,null = True)
    Department = models.CharField(u'部门', max_length=20, blank=False, null=False)
    GroupLeader = models.CharField(u'小组长', max_length=16, blank=False, null=False)
    Salesperson = models.CharField(u'销售员', max_length=16, blank=False, null=False)
    FirstDay   =  models.IntegerField(u'1号', max_length=16, blank=True, null=False)
    SecondDay = models.IntegerField(u'2号', max_length=16, blank=True, null=False)
    ThirdDay = models.IntegerField(u'3号', max_length=16, blank=True, null=False)
    FourthDay = models.IntegerField(u'4号', max_length=16, blank=True, null=False)
    FifthDay = models.IntegerField(u'5号', max_length=16, blank=True, null=False)
    SixthDay = models.IntegerField(u'6号', max_length=16, blank=True, null=False)
    SeventhDay = models.IntegerField(u'7号', max_length=16, blank=True, null=False)
    SumofFirstWeek = models.IntegerField(u'第一周<br>小计', max_length=16, blank=True, null=False)
    EighthDay = models.IntegerField(u'8号', max_length=16, blank=True, null=False)
    NinthDay = models.IntegerField(u'9号', max_length=16, blank=True, null=False)
    TenthDay = models.IntegerField(u'10号', max_length=16, blank=True, null=False)
    EleventhDay = models.IntegerField(u'11号', max_length=16, blank=True, null=False)
    TwelfthDay = models.IntegerField(u'12号', max_length=16, blank=True, null=False)
    ThirteenthDay = models.IntegerField(u'13号', max_length=16, blank=True, null=False)
    FourteenthDay = models.IntegerField(u'14号', max_length=16, blank=True, null=False)
    SumofSecondWeek = models.IntegerField(u'第二周<br>小计', max_length=16, blank=True, null=False)
    FifteenthDay = models.IntegerField(u'15号', max_length=16, blank=True, null=False)
    SixteenthDay = models.IntegerField(u'16号', max_length=16, blank=True, null=False)
    SeventeenthDay = models.IntegerField(u'17号', max_length=16, blank=True, null=False)
    EighteenthDay = models.IntegerField(u'18号', max_length=16, blank=True, null=False)
    NineteenthDay = models.IntegerField(u'19号', max_length=16, blank=True, null=False)
    TwentiethDay = models.IntegerField(u'20号', max_length=16, blank=True, null=False)
    TwentyFirstDay = models.IntegerField(u'21号', max_length=16, blank=True, null=False)
    SumofThirdWeek = models.IntegerField(u'第三周<br>小计', max_length=16, blank=True, null=False)
    TwentySecondDay = models.IntegerField(u'22号', max_length=16, blank=True, null=False)
    TwentyThirdDay = models.IntegerField(u'23号', max_length=16, blank=True, null=False)
    TwentyFourthDay = models.IntegerField(u'24号', max_length=16, blank=True, null=False)
    TwentyFifthDay = models.IntegerField(u'25号', max_length=16, blank=True, null=False)
    TwentySixthDay = models.IntegerField(u'26号', max_length=16, blank=True, null=False)
    TwentySeventhDay = models.IntegerField(u'27号', max_length=16, blank=True, null=False)
    TwentyEighthDay = models.IntegerField(u'28号', max_length=16, blank=True, null=False)
    SumofFourthWeek = models.IntegerField(u'第四周<br>小计', max_length=16, blank=True, null=False)
    TwentyNinthDay = models.IntegerField(u'29号', max_length=16, blank=True, null=False)
    ThirtiethDay = models.IntegerField(u'30号', max_length=16, blank=True, null=False)
    ThirtiethFirstDay = models.IntegerField(u'31号', max_length=16, blank=True, null=False)
    SumofMonth = models.IntegerField(u'月总和', max_length=16, blank=True, null=False)
    CompletionDegree = models.DecimalField(u'完成度<br>(%)',max_digits=11,decimal_places=2,blank = True,null = True)
    UnfinishedCause = models.TextField(u'未完成原因', max_length=16, blank=True, null=False)
    LatestRevisionTime = models.DateTimeField(u'更新时间',auto_now=True)
    ThisYear = models.CharField(u'年', max_length=16, blank=False, null=False)
    ThisMonth = models.CharField(u'月', max_length=16, blank=False, null=False)



    class Meta:
        verbose_name=u'非服装销售员登记表'
        verbose_name_plural=u'非服装销售员登记表'
        db_table = 'not_clothing_salesman_registration'
        ordering =  ['-ThisYear','-ThisMonth','Department','GroupLeader','Salesperson']
    def __unicode__(self):
        return u'id:%s'%(self.id)

