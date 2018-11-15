# -*- coding: utf-8 -*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from datetime import datetime
from skuapp.table.t_online_info_wish import t_online_info_wish
from skuapp.table.t_sys_department_staff import t_sys_department_staff
import logging
from django.contrib import messages
from skuapp.table.t_config_user_buyer import *
from skuapp.table.t_store_marketplan_execution import *
from skuapp.table.t_store_marketplan_execution_log import t_store_marketplan_execution_log
from django.db.models import F
from skuapp.table.t_store_marketplan_execution  import *


class t_config_user_buyer_taskAdmin(object):
    show_user_buyer=True
    def show_status(self,obj) :
        return t_config_user_buyer.objects.get(BuyerAccount=obj.BuyerAccount).Status
    show_status.short_description = u'执行状态'
    
    def show_count(self,obj):
        Quantity_objs = t_store_marketplan_execution.objects.values_list('Quantity',flat=True)
        t1=0
        for Quantity_obj in Quantity_objs:
            t1+=Quantity_obj
        Demand_objs = t_store_marketplan_execution.objects.values_list('Demand',flat=True)
        t2=0
        for Demand_obj in Demand_objs:
            t2+=Demand_obj
        return t2-t1
        
    show_count.short_description = u'总剩余刷单数'      
    list_display =('StaffId','FirstName','Updatetime','show_count')
    list_display_links = ('StaffId')
    list_editable = ()
    
    readonly_fields = ()
    fields = ('StaffId','FirstName')
              


    form_layout = (
        Fieldset(u'员工信息',
                    Row('StaffId','FirstName'),
                    css_class = 'unsort'
                ),
                  )
    
    def save_models(self):
        obj = self.new_obj
        request = self.request
        
        obj.save()
        
        #messages.error(request,'username===%s'%(request.user.username))
        
        t_store_marketplan_execution_log_objs = t_store_marketplan_execution_log.objects.filter(Status='EXEING',StaffId = request.user.username )
        #messages.error(request,'t_store_marketplan_execution_log_objs===%s'%t_store_marketplan_execution_log_objs)
        count = t_store_marketplan_execution_log_objs.count()
        #messages.error(request,'count===%s'%count)
        for i in range(0,count) :
            Remark = request.POST.get('Remark_%d'%i,'')
            
            if Remark is None or Remark =='' or Remark=='None' or Remark ==0 or Remark.strip() =='':
                continue
                
            xid = request.POST.get('id_%d'%i,''  )
            
            Remark = request.POST.get('Remark_%d'%i,'')
            
            Price = request.POST.get('Price_%d'%i,'')
            
            if Price is None or Price =='' or Price=='None' or Price ==0 or Price.strip() =='':
                continue
                
            xid = request.POST.get('id_%d'%i,''  )
            
            Price = request.POST.get('Price_%d'%i,'')
            
            Result = request.POST.get('Result_%d'%i,'')
            
            if Result is None or Result =='' or Result=='None' or Result ==0 or Result.strip() =='':
                continue
                
            xid = request.POST.get('id_%d'%i,''  )
            
            Result = request.POST.get('Result_%d'%i,'')   
            
            #Status = request.POST.get('Status_%d'%i,'')  
                
            
            #messages.error(request,'%s===%s'%(Remark,id))
            ProductID = request.POST.get('ProductID_%d'%i,'' )
            t_store_marketplan_execution.objects.filter(ProductID=ProductID).update(Quantity=F('Quantity')+1)
            t_store_marketplan_execution_log.objects.filter(id = xid).update(Result=Result,Price=Price,Remark = Remark,Status='FINISHED')
        
    def get_list_queryset(self):
        request = self.request
        qs = super(t_config_user_buyer_taskAdmin, self).get_list_queryset()
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(StaffId=request.user.username)

            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            







