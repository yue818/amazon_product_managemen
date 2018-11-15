# -*- coding: utf-8 -*-
from .t_product_Admin import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect,render


class t_cfg_b_emsfare2Admin(object):
   
    list_display= ('id','platform_country_code','countrycode','standard_id','category_id','extra_id','kickback','price_point','logisticwaycode','logisticwaycode_desc','updatetime')
    #list_editable = ('logisticwaycode',)
    list_filter = ('id','platform_country_code','countrycode','standard_id','category_id','extra_id','kickback','logisticwaycode','logisticwaycode_desc')
    search_fields = ('id','platform_country_code','countrycode','standard_id','category_id','extra_id','kickback','logisticwaycode','logisticwaycode_desc')
    #readonly_fields = ('platform_country_code','countrycode','standard_id','category_id','extra_id','kickback',)
           



            
            
            
            
            
            
            
            