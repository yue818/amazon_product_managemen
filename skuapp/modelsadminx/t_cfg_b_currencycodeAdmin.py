# -*- coding: utf-8 -*-
from .t_product_Admin import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect,render
from skuapp.table.t_cfg_b_currencycode_log import t_cfg_b_currencycode_log


class t_cfg_b_currencycodeAdmin(object):
   
    list_display= ('id','CURRENCYCODE','CurrencyName','ExchangeRate','updateTime')
    list_editable = ('ExchangeRate',)

    list_filter = ('id','CURRENCYCODE','CurrencyName','ExchangeRate',)

    search_fields = ('id','CURRENCYCODE','CurrencyName','ExchangeRate',)

    readonly_fields = ()

    show_detail_fields = ['id']
    
    def save_models(self):
        obj = self.new_obj
        request = self.request
        obj.save()
        obj_log = t_cfg_b_currencycode_log()        
        obj_log.__dict__ = obj.__dict__ 
        obj_log.id = None
        obj_log.UpdateMan = request.user.first_name
        obj_log.UpdateTime = obj.updateTime
        obj_log.save()
           



            
            
            
            
            
            
            
            