# coding=utf-8

from django.db import models

class Add(models.Model):
    task_id = models.CharField(max_length=128)
    first = models.IntegerField()
    second = models.IntegerField()
    log_date = models.DateTimeField()


class djcelery_crontabschedule(models.Model):
    minute          =   models.CharField(u'秒', max_length=64)
    hour            =   models.CharField(u'时', max_length=64)
    day_of_week     =   models.CharField(u'周几(0-6分别代表周日-周六)', max_length=64)
    day_of_month    =   models.CharField(u'每月几号(1-31)', max_length=64)
    month_of_year   =   models.CharField(u'月份(1-12)', max_length=64)

    class Meta:
        verbose_name = u'crontab配置表'
        verbose_name_plural = verbose_name
        db_table = 'djcelery_crontabschedule'
        app_label = 'app_djcelery'
        ordering = ['-id']

    def __unicode__(self):
        return u'%s' % self.id

ChoicePeriod = (
    ('seconds', u'秒'),
    ('minutes', u'分'),
    ('hours', u'时'),
    ('days', u'天')
)

class djcelery_intervalschedule(models.Model):
    every       =   models.IntegerField(u'间隔')
    period      =   models.CharField(u'周期', max_length=24)

    class Meta:
        verbose_name = u'interval配置表'
        verbose_name_plural = verbose_name
        db_table = 'djcelery_intervalschedule'
        app_label = 'app_djcelery'
        ordering = ['-id']

    def __unicode__(self):
        return u'%s' % self.id


class djcelery_tasktype(models.Model):
    task_type    =  models.CharField(u'任务类型', max_length=32)

    class Meta:
        verbose_name = u'celery定时任务类型'
        verbose_name_plural = verbose_name
        db_table = 'djcelery_tasktype'
        app_label = 'app_djcelery'
        ordering = ['-id']

    def __unicode__(self):
        return u'%s' % self.task_type


ChoiceEnabled = (
    (0, u'停用'),
    (1, u'启用')
)

ChoiceTaskType = (
    ('real_time', u'定时任务'),
    ('timing', u'实时任务'),
    ('fc', u'函数计算'),
    ('crontab', u'Crontab')
)

class djcelery_periodictask(models.Model):
    name                =   models.CharField(u'任务名', max_length=200)
    task                =   models.CharField(u'任务路径', max_length=200, blank=False, null=True)
    args                =   models.CharField(u'args', max_length=128, blank=True, null=True)
    kwargs              =   models.CharField(u'kwargs', max_length=128, blank=True, null=True)
    queue               =   models.CharField(u'queue', max_length=200, blank=True, null=True)
    exchange            =   models.CharField(u'exchange', max_length=200, blank=True, null=True)
    routing_key         =   models.CharField(u'routing_key', max_length=200, blank=True, null=True)
    expires             =   models.DateTimeField(u'到期时间', blank=True, null=True)
    enabled             =   models.IntegerField(u'启用状态', blank=False, null=True, choices=ChoiceEnabled)
    last_run_at         =   models.DateTimeField(u'上次运行时间', blank=True, null=True)
    total_run_count     =   models.IntegerField(u'已运行次数', blank=True, null=True)
    date_changed        =   models.DateTimeField(u'记录更新时间', blank=True, null=True)
    description         =   models.TextField(u'描述', blank=True, null=True)
    # crontab_id          =   models.IntegerField(u'定时执行', blank=False, null=False)
    # interval_id         =   models.IntegerField(u'时间间隔执行', blank=False, null=False)
    crontab             =   models.ForeignKey('djcelery_crontabschedule', blank=True, null=True, verbose_name=u'定时执行')
    interval            =   models.ForeignKey('djcelery_intervalschedule', blank=True, null=True, verbose_name=u'时间间隔执行')
    tasktype            =   models.ForeignKey('djcelery_tasktype', blank=False, null=True, verbose_name=u'任务类型')
    developer           =   models.CharField(u'开发人', max_length=32, blank=True, null=True)

    class Meta:
        verbose_name = u'celery定时任务配置表'
        verbose_name_plural = verbose_name
        db_table = 'djcelery_periodictask'
        app_label = 'app_djcelery'
        ordering = ['-id']

    def __unicode__(self):
        return u'%s' % self.name