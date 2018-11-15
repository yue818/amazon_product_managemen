# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)
from django.contrib import admin
from django.core import serializers
from django.db import transaction,connection
# Register your models here.
from django.db.models import Count




import json

import logging
import django.utils.log
import logging.handlers
from Project.settings import *
import os,errno,sys
#def decode(info):
#      return info.decode('utf-8')
from datetime import datetime

import time

import re
import math
from django.utils.timezone import utc
import oss2
from urllib2 import *
import urllib2
import socket
socket.setdefaulttimeout(10.0)
from bs4 import BeautifulSoup

from django.forms import TextInput, Textarea
import copy
from multiprocessing import Process,cpu_count
import multiprocessing
from django.utils.safestring import mark_safe
import xadmin
from django.db.models import F ,Q


from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader

from xml.dom.minidom import Document

from skuapp.table.t_config_apiurl import *
class t_config_apiurlAdmin(object):
    list_per_page=10
    list_display   =('id','URL','Status','runStatus','RefreshTimeB','RefreshTimeE','pageAllCount','RefreshCount','oldAllCount','UpdateTime','StaffID','group1','group2','group3','group4','group5',)
    search_fields   =('id','URL','Status','runStatus','StaffID','pageAllCount','RefreshCount','oldAllCount','group1','group2','group3','group4','group5',)
    list_filter   =('URL','Status','runStatus','RefreshTimeB','UpdateTime','StaffID','RefreshTimeE','pageAllCount','RefreshCount','oldAllCount','group1','group2','group3','group4','group5',)
    list_display_links = ('id',)
    list_editable = ('URL','Status',)
    #readonly_fields = ('id','runStatus','RefreshTimeB','pageAllCount','RefreshCount','oldAllCount','UpdateTime','StaffID','group1','group2','group3','group4','group5',)
    
    actions =  ['to_die','to_yes',]

    def to_die(self, request, queryset):
        for querysetid in queryset.all():
            t_config_apiurl.objects.filter(id = querysetid.id).update(Status = '0')
    to_die.short_description = u'不在启用'
    
    def to_yes(self, request, queryset):
        for querysetid in queryset.all():
            t_config_apiurl.objects.filter(id = querysetid.id).update(Status = '1')
    to_yes.short_description = u'启用'
    
    def save_models(self):
        obj = self.new_obj
        request = self.request
        obj.StaffID = request.user.username
        obj.save()

xadmin.site.register(t_config_apiurl,t_config_apiurlAdmin)