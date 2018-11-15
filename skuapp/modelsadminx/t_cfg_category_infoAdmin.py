# -*- coding: utf-8 -*-
from .t_product_Admin import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect,render


class t_cfg_category_infoAdmin(object):
    search_box2_flag = True
    list_display= ('id','CategoryName','CategoryId','show_operation')
    list_filter= ('id','CategoryName','CategoryId')
    list_editable= ('CategoryName','CategoryId')
    fields = ('CategoryId','CategoryName',)
    
    def show_operation(self,obj):
        rt = u'<input type="button" value="新增子品类" onclick="if(confirm(\'是否在当前本级品类目录下新增子品类？\')) {window.open(\'/category_info_add?id=%s \')}" target="_blank" />'%(obj.id)
        return mark_safe(rt)
    show_operation.short_description = u'操作'
           



            
            
            
            
            
            
            
            