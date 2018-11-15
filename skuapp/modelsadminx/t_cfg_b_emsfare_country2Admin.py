# -*- coding: utf-8 -*-
from .t_product_Admin import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect,render


class t_cfg_b_emsfare_country2Admin(object):
   
    list_display= ('id','country_code','logisticwaycode','getprice','getprice_desc','Bracketid','updatetime')
    #list_editable = ('logisticwaycode',)
    list_filter = ('id','country_code','logisticwaycode','getprice','getprice_desc','Bracketid')
    search_fields = ('id','country_code','logisticwaycode','getprice','getprice_desc','Bracketid')
    #readonly_fields = ('country_code','logisticwaycode','getprice','getprice_desc','Bracketid')




            
            
            
            
            
            
            
            