# -*- coding: utf-8 -*-
from .t_product_Admin import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect,render


class t_cfg_platform_countryAdmin(object):
   
    list_display= ('id','platform_country_code','platform_country_name','basefee','updatetime')

    list_filter = ('platform_country_code','platform_country_name')

    search_fields = ('platform_country_code','platform_country_name',)

    readonly_fields = ()

    show_detail_fields = ['id']
           



            
            
            
            
            
            
            
            