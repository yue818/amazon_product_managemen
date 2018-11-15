# -*- coding: utf-8 -*-
import logging
from django.contrib import messages
from datetime import datetime
from skuapp.table.t_config_paypal_account import t_config_paypal_account
from skuapp.table.t_api_schedule_ing import t_api_schedule_ing
from Project.settings import *



class t_paypal_payout_logAdmin(object):
    paypal_payout = True
    list_display = ('Payout_Account','Receipt_Account','Account','Status','Payout_Time','Log')
    list_display_links = ('id')
    search_fields = ('Payout_Account','Receipt_Account','Status','Payout_Time')
    list_filter = ('Payout_Account','Receipt_Account','Status','Payout_Time')
    fields = ('id',)


