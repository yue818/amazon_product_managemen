# -*- coding: utf-8 -*-
from .t_product_Admin import *
from skuapp.table.t_config_ip_ext import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect,render


class t_config_ip_ext_Admin(object):
   
    list_display= ('IP','K','UpdateTime',)
    list_editable = ('K',)
    #list_editable_all = ('Keywords',)
    #list_filter = ('UpdateTime',
                   # 'Weight',
                   # 'Electrification','Powder','Liquid','Magnetism','Buyer',
                   # 'Storehouse',
                   # 'DYStaffName','JZLStaffName','PZStaffName','MGStaffName','LRStaffName',
                   # 'StaffName','DepartmentID',
                   # )

    list_filter = ('IP','K',)

    search_fields = ('IP','K',)

    readonly_fields = ()

    show_detail_fields = ['id']
    
    def save_models(self):
        obj = self.new_obj
        obj.save()
        request = self.request
        #messages.error(request,obj.IP)
        #return HttpResponseRedirect('/Project/admin/skuapp/t_config_ip/?_q_=%s'%(obj.IP))
        #render(request, '/Project/admin/skuapp/t_config_ip/?_q_=%s'%(obj.IP))
        #return redirect('/Project/admin/skuapp/t_config_ip/?_q_=%s'%(obj.IP)) 
           



            
            
            
            
            
            
            
            