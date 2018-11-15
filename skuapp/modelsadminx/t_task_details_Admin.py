# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from skuapp.table.t_sys_param import *
from skuapp.table.t_task_details import *
from django.contrib import messages
from django.db.models import Q
import time,datetime


class t_task_details_Admin(object):

    def show_operation(self,obj):
        rt = "<input id='so_%s' type='button' value='分解任务' />"%obj.Current_number
        rt = "%s<script>$('#so_%s').on('click',function(){layer.open({type:2,skin:'layui-layer-lan',title:'分解任务详情',fix:false,shadeClose: true,maxmin:true,area:['300px','340px'],content:'/t_task_details/details/?cur_name=%s&orgi_name=%s&cur_num=%s&orgi_num=%s',\
		      btn:['提交'],btn:['关闭页面'],end:function(){location.reload();}});});</script>"%(rt,obj.Current_number,obj.Task_name_current,obj.Task_name_original,obj.Current_number,obj.Original_number) 
        return mark_safe(rt)
    show_operation.short_description = u'操作'
             
    list_display= ('Current_number','Task_name_current','Task_name_parent','Task_name_original','Task_status','Create_man','Task_handler','Create_time','Update_time','show_operation')
    list_editable = ('Task_name','Task_status','Task_handler')

    fields = ('Task_name_original','Task_name_parent','Task_name_current','Task_status','Create_man','Task_handler')

    list_filter = ('Current_number','Original_number','Parent_number','Task_name_current','Task_name_original','Task_name_parent','Task_status','Create_man','Task_handler','Create_time','Update_time',)

    search_fields = ('Current_number','Task_name_current','Task_name_original','Task_name_parent','Task_status','Create_man','Task_handler',)

    #readonly_fields = ('Task_name_original','Task_name_parent','Create_man','Task_handler')

    #show_detail_fields = ['Original_number']
    
    def save_models(self):
         obj = self.new_obj
         request = self.request
         obj.Update_time = datetime.datetime.now()
         obj.save()
        
    





            
            
            
            
            
            
            
            