# -*- coding: utf-8 -*-
from os import path
from django.apps import AppConfig



import logging
import django.utils.log
import logging.handlers

VERBOSE_APP_NAME = u"产品调研开发流程"
#lalalalalal


def get_current_app_name(file):
    return path.dirname(file).replace('\\', '/').split('/')[-1]


class AppVerboseNameConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = VERBOSE_APP_NAME


default_app_config = get_current_app_name(__file__) + '.__init__.AppVerboseNameConfig'



