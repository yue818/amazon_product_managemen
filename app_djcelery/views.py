# coding=utf-8

from app_djcelery.tasks import mix_opration, only_add
from app_djcelery.models import Add

from my_tools.db_operation import db_operation

from django.shortcuts import render_to_response
import datetime


def index(request):
    return  render_to_response('celery_index.html')

def celery_only_add(request):
    first = int(request.GET.get('first'))
    second = int(request.GET.get('second'))

    result = only_add.delay(first, second)

    dd = Add(task_id=result.id,first=first,second=second,log_date=datetime.datetime.now())
    dd.save()
    return render_to_response('celery_index.html')


def celery_mix_opration(request):
    first = int(request.GET.get('first'))
    second = int(request.GET.get('second'))

    param = {'x':first, 'y':second}

    result = mix_opration.delay(param)

    dd = Add(task_id=result.id, first=first, second=second, log_date=datetime.datetime.now())
    dd.save()
    return render_to_response('celery_index.html')



# 任务结果
def celery_results(request):
    #查询所有的任务信息
    db = db_operation()
    rows = db.get_tasksinfo()
    return render_to_response('celery_result.html',{'rows':rows})


