# -*- coding: utf-8 -*-
from .t_product_Admin import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect,render


class t_cfg_b_countryAdmin(object):
   
    list_display= ('id','country_code','country','updatetime')
    list_editable = ('country_code','country')

    list_filter = ('country_code','country')

    search_fields = ('country_code','country')

    readonly_fields = ()

    show_detail_fields = ['id']
           



            
            
            
            
            
            
            
            