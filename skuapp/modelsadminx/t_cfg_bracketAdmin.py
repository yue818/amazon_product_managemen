# -*- coding: utf-8 -*-
from .t_product_Admin import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect,render


class t_cfg_bracketAdmin(object):
   
    list_display= ('id','bracketid','weight','money')

    show_detail_fields = ['id']
           



            
            
            
            
            
            
            
            