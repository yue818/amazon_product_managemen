# coding=utf-8


import xadmin
from django.utils.safestring import mark_safe
import datetime
from xadmin.layout import Fieldset, Row
from app_djcelery.models import djcelery_periodictask, djcelery_crontabschedule
from app_djcelery.models import djcelery_intervalschedule, djcelery_tasktype
from django.contrib import messages


class djcelery_periodictask_Admin(object):
    search_box_flag = True

    def show_task(self, obj):
        djcelery_tasktype_obj = djcelery_tasktype.objects.filter(id=obj.tasktype_id)
        task_type = djcelery_tasktype_obj[0].task_type if djcelery_tasktype_obj.exists() else ''
        developer = obj.developer if obj.developer else ''
        rr = u'任务名: %s<br>任务路径: %s<br>任务类型 :%s<br>开发人 :%s' % (obj.name, obj.task, task_type, developer)
        return mark_safe(rr)
    show_task.short_description = u'<span style="color: #428bca">任务</span>'


    def show_param(self, obj):
        rr = u'args: %s<br>kwargs: %s' % (obj.args, obj.kwargs)
        return mark_safe(rr)
    show_param.short_description = u'<span style="color: #428bca">参数信息</span>'


    def show_queue(self, obj):
        q = obj.queue if obj.queue else 'celery'
        e = obj.exchange if obj.exchange else 'celery'
        r = obj.routing_key if obj.routing_key else 'celery'
        rr = u'queue: %s<br>exchange: %s<br>routing_key: %s' % (q, e, r)
        return mark_safe(rr)
    show_queue.short_description = u'<span style="color: #428bca">队列信息</span>'


    def show_time(self, obj):
        try:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            crontab_id = obj.crontab_id
            interval_id = obj.interval_id
            last_run_at = obj.last_run_at
            enabled = obj.enabled
            tasktype_id = obj.tasktype_id

            if tasktype_id == 1:
                if enabled == 0:
                    rr = u'该任务处于停用状态'
                elif not isinstance(last_run_at, datetime.datetime):
                    rr = u'该任务未查到上次运行时间'
                elif (not crontab_id) and (not interval_id):
                    rr = u'该任务未配置执行计划'
                else:
                    if crontab_id:
                        result = self.cal_by_crontab(crontab_id, last_run_at)
                    else:
                        result = self.cal_by_interval(interval_id, last_run_at)

                    if result['error'] == -1:
                        rr = result['error_info']
                    else:
                        next_time = result['next_time']
                        last_time = last_run_at.strftime("%Y-%m-%d %H:%M:%S")
                        next_time = next_time.strftime("%Y-%m-%d %H:%M:%S")
                        if next_time < current_time:
                            rr = u'上次执行: %s<br>下次执行: %s<br>执行状态: <span style="color:red">%s</span>' % (last_time, next_time, u'异常')
                        else:
                            rr = u'上次执行: %s<br>下次执行: %s<br>执行状态: <span style="color:green">%s</span>' % (last_time, next_time, u'正常')
            else:
                rr = u'非定时任务,无执行计划'
        except Exception, e:
            rr = u'%s' % str(e)
        return mark_safe(rr)
    show_time.short_description = u'<span style="color: #428bca">执行信息(误差 ± 60s)</span>'


    def cal_by_crontab(self, crontab_id, last_run_at):
        """根据crontab计算下次运行时间"""
        crontab_obj = djcelery_crontabschedule.objects.filter(id=crontab_id).values(
            'minute', 'hour', 'day_of_week', 'day_of_month', 'month_of_year')
        if crontab_obj.exists():
            minute = crontab_obj[0]['minute']
            hour = crontab_obj[0]['hour']
            day_of_week = crontab_obj[0]['day_of_week']
            day_of_month = crontab_obj[0]['day_of_month']
            month_of_year = crontab_obj[0]['month_of_year']
            if month_of_year.isdigit():
                next_time = last_run_at + datetime.timedelta(days=365)
                result = {'error': 0, 'next_time': next_time}
            elif day_of_month.isdigit():
                next_time = last_run_at + datetime.timedelta(days=30)
                result = {'error': 0, 'next_time': next_time}
            elif day_of_week.isdigit():
                next_time = last_run_at + datetime.timedelta(days=7)
                result = {'error': 0, 'next_time': next_time}
            elif hour.isdigit():
                next_time = last_run_at + datetime.timedelta(hours=24)
                result = {'error': 0, 'next_time': next_time}
            elif minute.isdigit():
                next_time = last_run_at + datetime.timedelta(minutes=60)
                result = {'error': 0, 'next_time': next_time}
            else:
                result = {'error': -1, 'error_info': u'无效的crontab配置'}
        else:
            result = {'error': -1, 'error_info': u'未查到指定的crontab配置信息'}
        return result


    def cal_by_interval(self, interval_id, last_run_at):
        """根据interval计算下次运行时间"""
        period_dict = {'seconds': 'seconds', 'minutes': 'minutes', 'hours': 'hours', 'days': 'days'}
        interval_obj = djcelery_intervalschedule.objects.filter(id=interval_id).values('every', 'period')
        if interval_obj.exists():
            every = interval_obj[0]['every']
            period = interval_obj[0]['period']
            if isinstance(every, long):
                next_time = last_run_at + datetime.timedelta(**{period_dict[period]: every})
                result = {'error': 0, 'next_time': next_time}
            else:
                result = {'error': -1, 'error_info': u'无效的interval配置'}
        else:
            result = {'error': -1, 'error_info': u'未查到指定的interval配置信息'}
        return result


    list_display = (
        'id', 'show_task', 'enabled', 'show_param', 'show_queue', 'show_time', 'expires', 'total_run_count',
        'description', 'date_changed'
    )
    list_editable = ('description',)
    fields = (
        'name', 'task', 'args', 'kwargs', 'queue', 'exchange', 'routing_key', 'enabled', 'description', 'crontab',
        'interval', 'tasktype'
    )
    form_layout = (
        Fieldset(
            u'任务',
            Row('name', 'task'),
            Row('enabled', 'tasktype'),
            css_class='unsort '
        ),
        Fieldset(
            u'配置',
            Row('args', 'kwargs'),
            Row('crontab', 'interval'),
            Row('queue', 'exchange', 'routing_key'),
            css_class='unsort '
        ),
        Fieldset(
            u'描述',
            Row('description', ),
            css_class='unsort '
        )
    )


    def save_models(self):
        request = self.request
        obj = self.new_obj

        developer = request.user.first_name
        name = request.POST.get('name', '')
        task = request.POST.get('task', '')
        args = request.POST.get('args', '')
        kwargs = request.POST.get('kwargs', '')
        queue = request.POST.get('queue', '')
        exchange = request.POST.get('exchange', '')
        routing_key = request.POST.get('routing_key', '')
        enabled = request.POST.get('enabled', '')
        description = request.POST.get('description', '')
        crontab = request.POST.get('crontab', '')
        interval = request.POST.get('interval', '')
        tasktype = request.POST.get('tasktype', '')

        if (tasktype == '1') and (not crontab) and (not interval):
            messages.error(request, u'定时任务"定时执行"和"时间间隔执行"不能同时为空')
            self.request.POST['_redirect'] = "/Project/admin/app_djcelery/djcelery_periodictask/add/"
        elif (tasktype == '1') and crontab and interval:
            messages.error(request, u'定时任务"定时执行"和"时间间隔执行"不能同时都不为空')
            self.request.POST['_redirect'] = "/Project/admin/app_djcelery/djcelery_periodictask/add/"
        else:
            args = args if args else []
            kwargs = kwargs if kwargs else {}
            queue = queue if queue else 'real_time'
            exchange = exchange if exchange else 'real_time'
            routing_key = routing_key if routing_key else 'real_time'
            crontab = int(crontab) if crontab else None
            interval = int(interval) if interval else None
            tasktype = int(tasktype) if tasktype else None
            if crontab:
                crontab_obj = djcelery_crontabschedule.objects.get(id=crontab)
                crontab = crontab_obj
            if interval:
                interval_obj = djcelery_intervalschedule.objects.get(id=interval)
                interval = interval_obj
            if tasktype:
                tasktype_obj = djcelery_tasktype.objects.get(id=tasktype)
                tasktype = tasktype_obj

            if obj is None or obj.id is None or obj.id <= 0:
                self.model.objects.create(
                    name=name, task=task, args=args, kwargs=kwargs, queue=queue, exchange=exchange,
                    routing_key=routing_key, enabled=enabled, description=description, crontab=crontab,
                    interval=interval, tasktype=tasktype, total_run_count=0, date_changed=datetime.datetime.now(),
                    developer=developer
                )
            else:
                self.model.objects.filter(id=obj.id).update(
                    name=name, task=task, args=args, kwargs=kwargs, queue=queue, exchange=exchange,
                    routing_key=routing_key, enabled=enabled, description=description, crontab=crontab,
                    interval=interval, tasktype=tasktype, developer=developer
                )


    def get_list_queryset(self):
        request = self.request
        qs = super(djcelery_periodictask_Admin, self).get_list_queryset()

        enabled = request.GET.get('enabled', '').strip()
        task_name = request.GET.get('task_name', '').strip()
        developer = request.GET.get('developer', '').strip()
        task_type = request.GET.get('task_type', '').strip()

        searchList = {
            'enabled__exact': enabled, 'name__exact': task_name, 'developer__exact': developer,
            'tasktype_id__exact': task_type
        }
        sl = {}
        for k, v in searchList.items():
            if isinstance(v, list):
                if v:
                    sl[k] = v
            else:
                if v is not None and v.strip() != '':
                    sl[k] = v
        if sl:
            qs = qs.filter(**sl)
        return qs

xadmin.site.register(djcelery_periodictask, djcelery_periodictask_Admin)