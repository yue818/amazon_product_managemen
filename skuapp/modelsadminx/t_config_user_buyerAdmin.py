# -*- coding: utf-8 -*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from datetime import datetime
from skuapp.table.t_online_info_wish import t_online_info_wish
from skuapp.table.t_sys_department_staff import t_sys_department_staff


import logging
from django.contrib import messages


class t_config_user_buyerAdmin(object):
    list_display =('StaffId','UserID','BuyerAccount','Status','PaypalAccount','Balance','CreateTime','UpdateTime')
    search_fields = ('StaffId','UserID','BuyerAccount','CreateTime','UpdateTime','Status','PaypalAccount','Balance')
    list_filter =('StaffId','UserID','BuyerAccount','CreateTime','UpdateTime','Status','PaypalAccount','Balance')
    list_display_links = ('id')
    list_editable = ('StaffId','UserID','BuyerAccount','Status','PaypalAccount')
    fields = ('StaffId','BuyerAccount','Status','PaypalAccount','Balance')

    def get_list_queryset(self):
        request = self.request
        qs = super(t_config_user_buyerAdmin, self).get_list_queryset()
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(StaffId=request.user.username)





