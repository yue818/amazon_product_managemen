# -*- coding: utf-8 -*-
from .t_product_Admin import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect,render


class t_cfg_standard_smallAdmin(object):
   
    list_display= ('id','standard_id','standard_small_code','standard_small_name')

    show_detail_fields = ['id']
           



            
            
            
            
            
            
            
            