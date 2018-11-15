# -*- coding: utf-8 -*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from datetime import datetime
from skuapp.table.t_online_info_wish import t_online_info_wish
from skuapp.table.t_sys_department_staff import t_sys_department_staff


import logging
from django.contrib import messages


class t_config_logistic_expressAdmin(object):
    list_display =('id','ExpressID','KeyInfo1','KeyInfo2','Url',)
    search_fields = ('ExpressID','KeyInfo1','Url','KeyInfo2')
    list_filter =('ExpressID','KeyInfo1','Url','KeyInfo2')
    list_display_links = ('id')
    list_editable = ('ExpressID','KeyInfo1','Url','KeyInfo2')
    fields = ('ExpressID','KeyInfo1','KeyInfo2','Url',)







