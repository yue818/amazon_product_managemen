# coding=utf-8

from __future__ import absolute_import

import os

from celery import Celery, platforms
platforms.C_FORCE_ROOT = True # root用户启动
import time
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')

from django.conf import settings  # noqa

app = Celery('app_djcelery', include=['app_djcelery.tasks'])

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

