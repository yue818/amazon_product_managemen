# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from skuapp.table.v_hotsale_proinfo_ebay_cloth import *
from skuapp.modelsadminx.t_hotsale_proinfo_ebay_Admin import *
from skuapp.table.t_config_apiurl_asin_kf import *
from urllib import urlencode
from django.contrib import messages
from datetime import datetime
from django.forms import TextInput, Textarea
from django.contrib.admin import ModelAdmin

class v_hotsale_proinfo_ebay_cloth_Admin(t_hotsale_proinfo_ebay_Admin):
    department_desc = 'cloth'
    def show_Image(self,obj) :
        url =u'%s'%(obj.Image)
        #<style type="text/css">img:hover{height:400px; width:400px;}</style>
        rt =  '<img src="%s" width="150" height="150"  alt = "%s"  title="%s"><style type="text/css">img:hover{height:400px; width:400px;}</style></img>'%(url,url,url)
        return mark_safe(rt)
    show_Image.short_description = u'图片'
   
    def get_list_queryset(self):
        request = self.request
        #request.session.set_expiry(5)
        if request.user.is_authenticated():        
            qs = super(t_hotsale_proinfo_ebay_Admin, self).get_list_queryset()
            if request.user.is_superuser:
                return qs.filter(department = 'Cloth')
            return qs.filter(isStop = 'N', department = 'Cloth').exclude(used='D')
        else:
            return render(request,'')