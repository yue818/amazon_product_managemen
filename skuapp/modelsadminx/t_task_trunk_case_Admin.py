# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.db.models import Q
import time,datetime


class t_task_trunk_case_Admin(object):
    
    def save_models(self):
         obj = self.new_obj
         request = self.request
         obj.Test_verifier_time = datetime.datetime.now()
         obj.save()
        
    





            
            
            
            
            
            
            
            