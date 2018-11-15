# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from datetime import datetime

class t_sensitive_sku_info_Admin(object):
    show_tort = True
    list_display = ('id','sensitive_sku','Input_man','Input_time')
    search_fields = ('id','sensitive_sku','Input_man')
    list_filter = ('sensitive_sku','Input_man','Input_time')
    readonly_fields = ('Input_man','Input_time')
    
    def save_models(self):
        obj = self.new_obj
        request = self.request
        obj.Input_man = request.user.first_name
        obj.Input_time = datetime.now()
        obj.save()
    
    
    
           
    
