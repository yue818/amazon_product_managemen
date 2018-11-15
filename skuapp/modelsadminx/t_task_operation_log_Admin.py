# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from skuapp.table.t_sys_param import *
from skuapp.table.t_task_trunk import *
from skuapp.table.t_task_details import *
from django.contrib import messages
from django.db.models import Q
import time,datetime
import oss2
from Project.settings import *
from skuapp.table.t_sys_param import *
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field, Div, FormActions, Submit, Button, ButtonHolder, InlineRadios, Reset, StrictButton, HTML, Hidden, Alert
import logging

class t_task_operation_log_Admin(object):

    list_display= ('Original_number','Flow_way_status','Flow_handle_result','Flow_handle_remark','Flow_handle_man','Flow_handle_time')

    list_filter = ()

    search_fields = ()
    

    





            
            
            
            
            
            
            
            