# -*- coding: utf-8 -*-
from .t_product_Admin import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect,render


class t_cfg_b_emsfareAdmin(object):
   
    list_display= ('id','platform_country_code','countrycode','seq','logisticwaycode','pricelimit','pricelimit_logisticwaycode','updatetime')
    list_editable = ('platform_country_code','countrycode','seq','logisticwaycode','pricelimit','pricelimit_logisticwaycode',)

    list_filter = ('platform_country_code','countrycode','seq','logisticwaycode','pricelimit','pricelimit_logisticwaycode',)

    search_fields = ('platform_country_code','countrycode','seq','logisticwaycode','pricelimit','pricelimit_logisticwaycode',)

    readonly_fields = ()

    show_detail_fields = ['id']
           



            
            
            
            
            
            
            
            