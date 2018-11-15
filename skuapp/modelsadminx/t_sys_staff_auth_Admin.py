# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from skuapp.table.t_sys_staff_auth import t_sys_staff_auth

class t_sys_staff_auth_Admin(object):
    list_display=('id','StaffID','urltable','remark',)
    list_filter=('id','StaffID','urltable','remark',)
    search_fields=('id','StaffID','urltable','remark',)