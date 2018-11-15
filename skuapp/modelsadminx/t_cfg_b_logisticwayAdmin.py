# -*- coding: utf-8 -*-
from .t_product_Admin import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect,render


class t_cfg_b_logisticwayAdmin(object):
   
    list_display= ('id','code','name','Discount','updatetime')
    list_editable = ('Discount')

    list_filter = ('code','name','Discount',)

    search_fields = ('code','name','Discount',)

    readonly_fields = ()

    show_detail_fields = ['id']
           



            
            
            
            
            
            
            
            