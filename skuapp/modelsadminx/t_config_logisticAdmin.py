# -*- coding: utf-8 -*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from datetime import datetime
from skuapp.table.t_online_info_wish import t_online_info_wish
from skuapp.table.t_sys_department_staff import t_sys_department_staff


import logging
from django.contrib import messages


class t_config_logisticAdmin(object):
    list_display =('id','LogisticName','ExpressID','ServiceID','Oversea',)
    search_fields = ('LogisticName','ExpressID','ServiceID','Oversea',)
    list_filter =('LogisticName','ExpressID','ServiceID','Oversea',)
    list_display_links = ('id')
    list_editable = ('LogisticName','ExpressID','ServiceID','Oversea',)
    fields = ('LogisticName','ExpressID','ServiceID','Oversea',)






