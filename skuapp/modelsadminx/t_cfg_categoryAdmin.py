# -*- coding: utf-8 -*-
from .t_product_Admin import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect,render


class t_cfg_categoryAdmin(object):
   
    list_display= ('id','category_id','category_code','category_name','logisticwaycode','logisticwaycode_desc','updatetime')
           



            
            
            
            
            
            
            
            