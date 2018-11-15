# coding:utf8
from __future__ import unicode_literals

from django.db import models


# Create your models here.


class clothing_salesman_registration(models.Model):
    """
    职员销量统计
    """

    choice = [
        ('反向开发', '反向开发'),
        ('体系开发', '体系开发'),
        ('工厂款领取落地', '工厂款领取落地'),
        ('店铺上新', '店铺上新'),
    ]
    choice1 = [
        ('办公室', '办公室'),
        ('平台事业部一部', '平台事业部一部'),
        ('平台事业部二部', '平台事业部二部'),
        ('平台事业部三部', '平台事业部三部'),
        ('平台事业部四部', '平台事业部四部'),
        ('平台事业部五部', '平台事业部五部'),
        ('营销执行', '营销执行'),
        ('开发采购部', '开发采购部'),
        ('服装开发部', '服装开发部'),
        ('产品开发部', '产品开发部'),
        ('资源部', '资源部'),
        ('小平台', '小平台'),
        ('仓储物流', '仓储物流'),

    ]
    month_choice = [

        ('一月', '一月'),
        ('二月', '二月'),
        ('三月', '三月'),
        ('四月', '四月'),
        ('五月', '五月'),
        ('六月', '六月'),
        ('七月', '七月'),
        ('八月', '八月'),
        ('九月', '九月'),
        ('十月', '十月'),
        ('十一月', '十一月'),
        ('十二月', '十二月'),

    ]


    name = models.CharField(max_length=60, blank=True, choices=choice, verbose_name='类目名称')
    staff_name = models.CharField(max_length=60, blank=True, verbose_name='销售员')
    department = models.CharField(max_length=60, choices=choice1, blank=True, verbose_name='部门')
    day01 = models.IntegerField(blank=True, default=0, verbose_name='01号')
    day02 = models.IntegerField(blank=True, default=0, verbose_name='02号')
    day03 = models.IntegerField(blank=True, default=0, verbose_name='03号')
    day04 = models.IntegerField(blank=True, default=0, verbose_name='04号')
    day05 = models.IntegerField(blank=True, default=0, verbose_name='05号')
    day06 = models.IntegerField(blank=True, default=0, verbose_name='06号')
    day07 = models.IntegerField(blank=True, default=0, verbose_name='07号')
    
    day08 = models.IntegerField(blank=True, default=0, verbose_name='08号')
    day09 = models.IntegerField(blank=True, default=0, verbose_name='09号')
    day10 = models.IntegerField(blank=True, default=0, verbose_name='10号')
    day11 = models.IntegerField(blank=True, default=0, verbose_name='11号')
    day12 = models.IntegerField(blank=True, default=0, verbose_name='12号')
    day13 = models.IntegerField(blank=True, default=0, verbose_name='13号')
    day14 = models.IntegerField(blank=True, default=0, verbose_name='14号')
    
    day15 = models.IntegerField(blank=True, default=0, verbose_name='15号')
    day16 = models.IntegerField(blank=True, default=0, verbose_name='16号')
    day17 = models.IntegerField(blank=True, default=0, verbose_name='17号')
    day18 = models.IntegerField(blank=True, default=0, verbose_name='18号')
    day19 = models.IntegerField(blank=True, default=0, verbose_name='19号')
    day20 = models.IntegerField(blank=True, default=0, verbose_name='20号')
    day21 = models.IntegerField(blank=True, default=0, verbose_name='21号')
    
    day22 = models.IntegerField(blank=True, default=0, verbose_name='22号')
    day23 = models.IntegerField(blank=True, default=0, verbose_name='23号')
    day24 = models.IntegerField(blank=True, default=0, verbose_name='24号')
    day25 = models.IntegerField(blank=True, default=0, verbose_name='25号')
    day26 = models.IntegerField(blank=True, default=0, verbose_name='26号')
    day27 = models.IntegerField(blank=True, default=0, verbose_name='27号')
    day28 = models.IntegerField(blank=True, default=0, verbose_name='28号')
    
    day29 = models.IntegerField(blank=True, default=0, verbose_name='29号')
    day30 = models.IntegerField(blank=True, default=0, verbose_name='30号')
    day31 = models.IntegerField(blank=True, default=0, verbose_name='31号')
    the_month = models.CharField(max_length=60, blank=True, choices=month_choice, verbose_name='月份')
    complate=models.IntegerField(blank=True, default=0, verbose_name='完成度(%)')
    reson=models.TextField(blank=True,default='',verbose_name='未完成原因')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')
    
    
    class Meta:
        verbose_name = '职员销量统计'
        verbose_name_plural = '职员销量统计'
        
    
    
    def week1(self, ):
        self.sum1 = self.day01 + self.day02 + self.day03 + self.day04 + self.day05 + self.day06 + self.day07
        return str(self.sum1)
    
    
    week1.short_description = '周统计'
    
    
    # week1.is_column = True
    # week1.allow_tags = True
    
    
    
    def week2(self, ):
        self.sum2 = self.day08 + self.day09 + self.day10 + self.day11 + self.day12 + self.day13 + self.day14
        return str(self.sum2)
    
    
    week2.short_description = '周统计'
    
    
    # week2.is_column = True
    # week2.allow_tags = True
    
    
    
    def week3(self, ):
        self.sum3 = self.day15 + self.day16 + self.day17 + self.day18 + self.day19 + self.day20 + self.day21
    
        return str(self.sum3)
    
    
    week3.short_description = '周统计'
    
    
    # week3.is_column = True
    # week3.allow_tags = True
    
    def week4(self, ):
        self.sum4 = self.day22 + self.day23 + self.day24 + self.day25 + self.day26 + self.day27 + self.day28
        return str(self.sum4)
    
    
    week4.short_description = '周统计'
    
    
    def week5(self, ):
        self.sum5 = self.day29 + self.day30 + self.day31
        return str(self.sum5)
    
    
    week5.short_description = '周统计'
    
    
    def month(self):
        self.month = self.sum1 + self.sum2 + self.sum3 + self.sum4 + self.sum5
        return str(self.month)
    
    
    month.short_description = '月统计'
    
    
    def __unicode__(self):
        return self.name
