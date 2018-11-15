# -*- coding: utf-8 -*-
import xadmin
import logging
from xadmin.views import BaseAdminPlugin, ListAdminView,ModelFormAdminView,CommAdminView,BaseAdminView
from django.template import loader
from skuapp.table.t_task_trunk import *
from django.contrib.auth.models import User
from skuapp.table.t_task_operation_log import *
from skuapp.table.t_task_trunk_case import t_task_trunk_case
import traceback


class t_task_trunkPlugin(BaseAdminPlugin):
    show_task_details = False
    def init_request(self, *args, **kwargs):     
        return bool(self.show_task_details)

    def block_before_fieldsets(self, context, nodes):
        #if context['original']  is  not None :
        models_objs = (u'%s'%context['request']).split('/')
        if models_objs[1] == 'Project' and models_objs[2] == 'admin':
            task_id = models_objs[5]
        elif models_objs[1] == 'xadmin':
            task_id = models_objs[4]
        try:
            user_obj = self.request.user.username
            task_id = int(task_id)
            t_task_trunk_obj = t_task_trunk.objects.get(Original_number=task_id)
            t_task_operation_log_objs = t_task_operation_log.objects.filter(Original_number=task_id)
            fs = t_task_trunk_obj.Flow_Status
            flow_status = t_sys_param.objects.values_list('VDesc').filter(Type=232,V=t_task_trunk_obj.Flow_Status)[0][0]
            last_update_time = t_task_trunk_obj.Update_time
            Current_chargeman = User.objects.values_list('first_name').filter(username=t_task_trunk_obj.Current_chargeman)[0][0]
        except Exception as e:
            #traceback.print_exc(file=open('/tmp/cc.log', 'a'))
            task_id = int(t_task_trunk.objects.latest('Original_number').Original_number)+1
            flow_status = ''
            last_update_time = ''
            Current_chargeman = ''
            fs = ''
            t_task_operation_log_objs = ''
            t_task_trunk_obj=''
        t_task_trunk_case_objs = t_task_trunk_case.objects.filter(Original_number=task_id)    
            
        nodes.append(loader.render_to_string('t_task_trunkPlugin.html',{'fs':fs,'flow_status':flow_status,'Current_chargeman':Current_chargeman,'last_update_time':last_update_time,'t_task_operation_log_objs':t_task_operation_log_objs,'t_task_trunk_case_objs':t_task_trunk_case_objs,'t_task_trunk_obj':t_task_trunk_obj,'user_obj':user_obj,'task_id':task_id}))
