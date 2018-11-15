# -*- coding: utf-8 -*-
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field

#from skuapp.table.t_online_info_wish import t_online_info_wish
#from skuapp.table.t_sys_department_staff import t_sys_department_staff
#from skuapp.table.t_store_status import t_store_status
  
#import logging
#from django.contrib import messages
from django.contrib.auth.models import *
from skuapp.table.t_config_user_buyer_task import *
from skuapp.table.t_store_marketplan_execution_log import *
from django.utils.safestring import mark_safe
from skuapp.table.t_config_user_buyer import *
from Project.settings import *
from .t_product_Admin import * 
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from datetime import datetime

class t_store_marketplan_execution_evaluate_Admin(object):
    '''
    def get_list_queryset(self):
        request = self.request
        qs = super(t_store_marketplan_execution_evaluate_Admin, self).get_list_queryset()
        if request.user.is_superuser:
            return qs.filter(Product_evaluate='no')
        else:
            return qs.filter(StaffId=request.user.username,Product_evaluate='no')
    '''
            
    def show_person(self,obj):     
        FirstName_objs = t_config_user_buyer_task.objects.get(StaffId=obj.StaffId)
        return FirstName_objs.FirstName
    show_person.short_description=u'中文名'
    
    def show_picture(self,obj):
        return mark_safe(u'<img style="width:90px;height:90px" src=%s/>'%(obj.PicURL))
    show_picture.short_description=u'产品图片'

    def show_userid(self,obj):
        try:
            user_id_objs = t_config_user_buyer.objects.filter(BuyerAccount=obj.BuyerAccount.strip(),StaffId=obj.StaffId)[0]
            return user_id_objs.UserID
        except:
            return ''
    show_userid.short_description=u'UserID'
    
    def show_PaypalAccount(self,obj):
        try:     
            PaypalAccount_objs = t_config_user_buyer.objects.filter(BuyerAccount=obj.BuyerAccount.strip(),StaffId=obj.StaffId)[0]
            return PaypalAccount_objs.PaypalAccount
        except:
            return ''
    show_PaypalAccount.short_description=u'卡号'        
     
    list_display =('id','show_picture','BuyerAccount','show_userid','ProductID','show_PaypalAccount','Status','Exetime','ShopName','ShopSKU','StaffId','show_person','Price','Price2','Result','Product_evaluate')
#    search_fields = ('id','BuyerAccount','ProductID','Status','Exetime','ShopName','ShopSKU','StaffId','Price','Price2','Result','Product_evaluate')
    list_filter =('id','BuyerAccount','ProductID','Status','Exetime','ShopName','ShopSKU','StaffId','Price','Price2','Result','Product_evaluate')
    list_display_links = ('id')
    list_editable = ('Product_evaluate')            
    #readonly_fields = ('id','PicURL','BuyerAccount','ProductID','Status','Exetime','ShopName','ShopSKU','StaffId','Price','Price2','Result','Pid')
    search_fields =None




