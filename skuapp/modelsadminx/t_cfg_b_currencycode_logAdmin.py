# -*- coding: utf-8 -*-
from .t_product_Admin import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect,render


class t_cfg_b_currencycode_logAdmin(object):
   
    list_display= ('id','CURRENCYCODE','CurrencyName','ExchangeRate','UpdateMan','UpdateTime')

    list_filter = ('id','CURRENCYCODE','CurrencyName','ExchangeRate',)

    search_fields = ('id','CURRENCYCODE','CurrencyName','ExchangeRate',)

    readonly_fields = ()

    show_detail_fields = ['id']
           



            
            
            
            
            
            
            
            