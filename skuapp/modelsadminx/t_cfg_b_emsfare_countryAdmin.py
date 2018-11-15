# -*- coding: utf-8 -*-
from .t_product_Admin import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect,render


class t_cfg_b_emsfare_countryAdmin(object):
   
    list_display= ('id','country_code','logisticwaycode','BaseMoney','BeginWeight','BeginMoney','AddWeight','AddMoney','updateTime')
    list_editable = ('country_code','logisticwaycode','BaseMoney','BeginWeight','BeginMoney','AddWeight','AddMoney')

    list_filter = ('country_code','logisticwaycode','BaseMoney','BeginWeight','BeginMoney','AddWeight','AddMoney')

    search_fields = ('country_code','logisticwaycode','BaseMoney','BeginWeight','BeginMoney','AddWeight','AddMoney')

    readonly_fields = ()

    show_detail_fields = ['id']
           



            
            
            
            
            
            
            
            